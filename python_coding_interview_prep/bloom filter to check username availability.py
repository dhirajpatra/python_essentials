"""
[ New Signup Request ]
          │
          ▼
┌──────────────────┐  Says "No" (Definitely Available) ──► [ Approve Username ]
│ 1. Bloom Filter  ├─────────────────────────────────────────────────┐
└─────────┬────────┘                                                 │
          │ Says "Yes" (Might be taken)                              │
          ▼                                                          │
┌──────────────────┐  Found (Definitely Taken) ─────────────────────┼──► [ Reject ]
│   2. Redis Cache ├─────────────────────────────────────────┐       │
└─────────┬────────┘                                         │       │
          │ Cache Miss (Not found in cache)                  │       │
          ▼                                                  ▼       ▼
┌──────────────────┐  Found ────────────────────────────────► [ Reject & Update Cache ]
│ 3. Main Database │
└──────────────────┘  Not Found ────────────────────────────► [ Save to DB & Update Filter ]

Three ways to parameterised:

# (a) Auto-optimize from expected count + FP rate
BloomFilter(expected_items=10_000, false_positive_rate=0.01)

# (b) Bits per item — your "7 bit" example
BloomFilter(expected_items=1_000, bits_per_item=7)

# (c) Full manual control
BloomFilter(expected_items=5_000, size_bits=65_536, num_hashes=5)

2. Optimal parameters formulas
Bit array size: m = -(n · ln p) / (ln 2)²

Hash count: k = (m / n) · ln 2

For 7 bits/item, k = round(7 × 0.693) ≈ 5 hashes → ~1% FP rate.

3. Double hashing trick
Instead of running k independent hashes, we compute two (SHA-256 + MD5) and derive k positions via:

text
h_i(x) = (h1(x) + i · h2(x)) mod m
Fast and statistically sound.

4. Correctness guarantee
False → definitely not registered

True → possibly registered (may be false positive)

5. Built-in diagnostics
bf.stats() gives size, hashes, load factor, and estimated current FP rate.
"""

import hashlib
import math
import mmap
import os


class BloomFilter:
    """
    A pure Python Bloom Filter implementation for checking username existence.
    
    A Bloom filter is a probabilistic data structure that can tell you:
      - "definitely not in the set" (100% accurate)
      - "possibly in the set" (may have false positives)
    
    It never returns false negatives.
    """

    def __init__(self, expected_items: int = 10000, false_positive_rate: float = 0.01,
                 num_hashes: int = None, bits_per_item: int = None, size_bits: int = None):
        """
        Initialize the Bloom Filter.

        You can parameterize in three ways:
          1. By expected_items + false_positive_rate (auto-computes optimal size & hashes)
          2. By size_bits + num_hashes (explicit control)
          3. By bits_per_item + num_hashes (e.g., 7 bits, 10 bits per item)

        Args:
            expected_items (int): Number of items expected to be inserted.
            false_positive_rate (float): Desired false positive probability (0 < p < 1).
            num_hashes (int): Number of hash functions to use.
            bits_per_item (int): Number of bits allocated per item (e.g., 7, 10, 12).
            size_bits (int): Total size of the bit array in bits.
        """
        self.expected_items = expected_items
        self.false_positive_rate = false_positive_rate

        # --- Parameter calculation ---
        if bits_per_item is not None:
            # Mode 3: bits per item directly
            self.size_bits = expected_items * bits_per_item
            self.num_hashes = num_hashes or self._optimal_hashes_for_bits_per_item(bits_per_item)
        elif size_bits is not None:
            # Mode 2: explicit size
            self.size_bits = size_bits
            self.num_hashes = num_hashes or self._optimal_hashes(self.size_bits, expected_items)
        else:
            # Mode 1: derive from expected items + FP rate
            self.size_bits, self.num_hashes = self._optimal_params(
                expected_items, false_positive_rate
            )

        self.size_bits = max(self.size_bits, 1)
        self.num_hashes = max(self.num_hashes, 1)

        # Byte array to store bits (rounded up to nearest byte)
        self.num_bytes = (self.size_bits + 7) // 8
        self.bit_array = bytearray(self.num_bytes)
        self.item_count = 0  # number of items inserted (approx, for stats)

    # ------------------- Parameter helpers -------------------

    @staticmethod
    def _optimal_params(n: int, p: float):
        """Compute optimal bit array size (m) and number of hashes (k)."""
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        k = (m / n) * math.log(2)
        return int(math.ceil(m)), int(math.ceil(k))

    @staticmethod
    def _optimal_hashes(m: int, n: int) -> int:
        """Given m bits and n items, compute optimal k."""
        if n <= 0:
            return 1
        return max(1, int(round((m / n) * math.log(2))))

    @staticmethod
    def _optimal_hashes_for_bits_per_item(bits_per_item: int) -> int:
        """For a given bits-per-item (m/n), optimal k = (m/n) * ln(2)."""
        return max(1, int(round(bits_per_item * math.log(2))))

    # ------------------- Hashing -------------------

    def _hashes(self, item: str):
        """
        Generate `num_hashes` hash positions using the double-hashing trick:
            h_i(x) = (h1(x) + i * h2(x)) mod m
        This gives us k independent-ish hash values from just 2 hash computations.
        """
        if isinstance(item, str):
            data = item.encode("utf-8")
        else:
            data = bytes(item)

        h1 = int.from_bytes(hashlib.sha256(data).digest()[:8], "big")
        h2 = int.from_bytes(hashlib.md5(data).digest()[:8], "big")

        # Ensure h2 is odd so we don't get stuck in a cycle when m is a power of 2
        h2 |= 1

        for i in range(self.num_hashes):
            yield (h1 + i * h2) % self.size_bits

    # ------------------- Bit operations -------------------

    def _set_bit(self, pos: int):
        byte_index = pos >> 3
        bit_index = pos & 7
        self.bit_array[byte_index] |= (1 << bit_index)

    def _get_bit(self, pos: int) -> bool:
        byte_index = pos >> 3
        bit_index = pos & 7
        return bool(self.bit_array[byte_index] & (1 << bit_index))

    # ------------------- Public API -------------------

    def add(self, item: str):
        """Add a username to the filter."""
        for pos in self._hashes(item):
            self._set_bit(pos)
        self.item_count += 1

    def __contains__(self, item: str) -> bool:
        """Check if username is possibly present."""
        return all(self._get_bit(pos) for pos in self._hashes(item))

    def check(self, item: str) -> bool:
        """Alias for `item in bloom`. Returns True = possibly exists, False = definitely not."""
        return item in self

    def exists(self, item: str) -> bool:
        """Semantic alias — 'possibly exists'."""
        return self.check(item)

    def add_many(self, items):
        for item in items:
            self.add(item)

    def __len__(self):
        return self.item_count

    # ------------------- Diagnostics -------------------

    def current_false_positive_rate(self) -> float:
        """Estimate the current false positive rate based on inserted items."""
        n = self.item_count
        m = self.size_bits
        k = self.num_hashes
        if n == 0:
            return 0.0
        return (1 - math.exp(-k * n / m)) ** k

    def stats(self) -> dict:
        set_bits = sum(bin(b).count("1") for b in self.bit_array)
        return {
            "expected_items": self.expected_items,
            "target_fp_rate": self.false_positive_rate,
            "size_bits": self.size_bits,
            "size_bytes": self.num_bytes,
            "num_hashes": self.num_hashes,
            "bits_per_item": round(self.size_bits / self.expected_items, 2),
            "items_inserted": self.item_count,
            "bits_set": set_bits,
            "load_factor": round(set_bits / self.size_bits, 4),
            "estimated_current_fp": round(self.current_false_positive_rate(), 6),
        }

    def __repr__(self):
        s = self.stats()
        return (f"BloomFilter(size={s['size_bits']} bits, hashes={s['num_hashes']}, "
                f"items={s['items_inserted']}, fp≈{s['estimated_current_fp']})")


# =====================================================================
# DEMO
# =====================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("Bloom Filter — Username Availability Checker Demo")
    print("=" * 65)

    # Example 1: Parameterize with expected items + FP rate
    print("\n[1] Auto params: 10,000 users, 1% false positive rate")
    bf = BloomFilter(expected_items=10_000, false_positive_rate=0.01)
    print("   ", bf)

    # Example 2: Parameterize with bits-per-item (e.g., 7 bits)
    print("\n[2] Explicit: 7 bits per item for 1,000 users")
    bf7 = BloomFilter(expected_items=1_000, bits_per_item=7)
    print("   ", bf7, "| k =", bf7.num_hashes)

    # Example 3: Explicit size_bits + num_hashes
    print("\n[3] Explicit: 65536 bits, 5 hashes")
    bf3 = BloomFilter(expected_items=5_000, size_bits=65_536, num_hashes=5)
    print("   ", bf3)

    # ---- Use one of them ----
    bf = BloomFilter(expected_items=5_000, false_positive_rate=0.001)

    # Register a bunch of usernames
    taken = [
        "alice", "bob", "charlie", "diana", "eve",
        "frank", "grace", "heidi", "ivan", "judy",
        "admin", "root", "user123", "john_doe", "jane_doe",
    ]
    bf.add_many(taken)

    print("\nRegistered usernames:", taken)

    # Check some usernames
    print("\nChecking usernames:")
    test_names = ["alice", "bob", "zach", "newuser", "admin", "unknown_guy", "eve"]
    for name in test_names:
        if bf.check(name):
            print(f"   ❌ '{name}' -> MAY BE TAKEN (possibly exists)")
        else:
            print(f"   ✅ '{name}' -> AVAILABLE (definitely not registered)")

    # Show stats
    print("\nFilter stats:")
    for k, v in bf.stats().items():
        print(f"   {k:>22}: {v}")

    # Demonstrate false positive behavior with 7-bit configuration
    print("\n[False Positive Measurement — 7 bits/item]")
    bf_small = BloomFilter(expected_items=1000, bits_per_item=7)
    real_users = [f"user_{i}" for i in range(1000)]
    bf_small.add_many(real_users)

    fp = 0
    trials = 10_000
    for i in range(trials):
        if bf_small.check(f"nonexistent_{i}"):
            fp += 1
    print(f"   Actual FP rate (7 bits/item): {fp/trials:.4f}  "
          f"(theoretical ≈ {(1 - math.exp(-math.log(2)))**(7*math.log(2)):.4f})")