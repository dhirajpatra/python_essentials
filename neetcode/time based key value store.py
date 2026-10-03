"""
Design a time-based key-value data structure that can store multiple values for the same key at different time stamps
and retrieve the key's value at a certain timestamp.

Implement the TimeMap class:

TimeMap() Initializes the object of the data structure.
void set(String key, String value, int timestamp) Stores the key with the value at the given time timestamp.
String get(String key, int timestamp) Returns a value such that set was called previously,
with timestamp_prev <= timestamp. If there are multiple such values,
it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".
Example 1:

Input:
["TimeMap", "set", ["alice", "happy", 1], "get", ["alice", 1], "get", ["alice", 2],
"set", ["alice", "sad", 3], "get", ["alice", 3]]

Output:
[null, null, "happy", "happy", null, "sad"]

Explanation:
TimeMap timeMap = new TimeMap();
timeMap.set("alice", "happy", 1);  // store the key "alice" and value "happy" along with timestamp = 1.
timeMap.get("alice", 1);           // return "happy"
timeMap.get("alice", 2);           // return "happy", there is no value stored for timestamp 2,
thus we return the value at timestamp 1.
timeMap.set("alice", "sad", 3);    // store the key "alice" and value "sad" along with timestamp = 3.
timeMap.get("alice", 3);           // return "sad"

Constraints:
1 <= key.length, value.length <= 100
key and value only include lowercase English letters and digits.
0 <= timestamp <= 10^7
All the timestamps of set are strictly increasing.
At most 2 * 10^5 calls will be made to set and get.

Time complexity for set and get operations is O(log n) where n is the number of entries for a given key.
"""

class TimeMap:

    def __init__(self):
        # Initialize a dictionary to store lists of [value, timestamp] pairs for each key
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if len(key) < 1 or len(key) > 100:
            raise ValueError("Key must be between 1 and 100 characters long")
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Value must be between 1 and 100 characters long")
        if timestamp < 0 or timestamp > 10**7:
            raise ValueError("Timestamp must be between 0 and 10^7")

        # If the key doesn't exist in the dictionary, initialize it with an empty list
        if key not in self.store:
            self.store[key] = []

        # Append the [value, timestamp] pair to the list for the given key
        self.store[key].append([value, timestamp])

    def get(self, key: str, timestamp: int) -> str:
        if len(key) < 1 or len(key) > 100:
            raise ValueError("Key must be between 1 and 100 characters long")
        if timestamp < 0 or timestamp > 10**7:
            raise ValueError("Timestamp must be between 0 and 10^7")

        # If the key doesn't exist, return an empty string
        if key not in self.store:
            return ""

        # Get the list of [value, timestamp] pairs for the given key
        values = self.store[key]

        # Binary search to find the appropriate value
        left, right = 0, len(values) - 1
        result = ""

        # Standard binary search logic
        while left <= right:
            mid = (left + right) // 2
            if values[mid][1] <= timestamp:
                result = values[mid][0]  # Store the value
                left = mid + 1          # Look for a larger timestamp
            else:
                right = mid - 1         # Look for a smaller timestamp

        return result


if __name__=="__main__":
    timeMap = TimeMap()

    timeMap.set("alice", "happy", 1)

    print(timeMap.get("alice", 1))

    print(timeMap.get("alice", 2))

    timeMap.set("alice", "sad", 3)

    print(timeMap.get("alice", 3))
