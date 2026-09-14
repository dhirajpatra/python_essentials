"""
Think of a circuit breaker like an automatic safety switch for your service calls:
it watches for failures, and if too many happen, it “trips” to stop more requests from making things worse.

## The three states (beginner-friendly)

- **CLOSED (normal mode)**
  - Everything is working as expected.
  - Requests go through to the downstream service (e.g., payment API, database, another microservice).
  - The breaker quietly counts recent failures.

- **OPEN (tripped / protective mode)**
  - Too many failures happened in a short time, so the breaker “trips”.
  - It **rejects new requests immediately** without even calling the failing service.
  - This protects your system from:
    - Wasting time waiting on timeouts
    - Overloading an already-failing dependency
    - Cascading failures across your architecture

- **HALF-OPEN (testing recovery)**
  - After a configured wait time (`recovery_time_sec` or similar), the breaker moves to HALF-OPEN.
  - It allows **a small number of test requests** through to see if the downstream service has recovered.
  - Outcomes:
    - If test requests **succeed** → breaker assumes recovery and goes back to **CLOSED**.
    - If test requests **fail** → breaker goes back to **OPEN** and waits again.

## Simple mental model

- **CLOSED** = “All good, keep calling.”
- **OPEN** = “Something’s broken; stop calling and fail fast.”
- **HALF-OPEN** = “Maybe it’s fixed; let’s try a few calls carefully.”

CLOSED ──(failures >= threshold)──► OPEN
  ▲                                   │
  │                              (recovery_time_sec passes)
  │                                   ▼
  └────(test call succeeds)────── HALF-OPEN

This pattern is widely used in microservices and cloud architectures (including on AWS)
to make systems more resilient to failures and latency spikes, especially when dependencies are unreliable.

When transforming developer teams from monolithic applications to microservices,
teams often implement ad-hoc retry loops that cause cascading database failures under load.

Build a reusable Circuit Breaker and Token Bucket Rate Limiter module in Python
that developers can apply as a decorator to their microservice endpoints to handle
external service degradation gracefully.
"""
import functools
import logging
import time
from typing import Callable, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ChassisResilience")


class CircuitBreakerOpenException(Exception):
    """Raised when the circuit breaker is in OPEN state."""

    def __init__(self, service_name: str, tripped_at: float, recovery_time_sec: float, failure_count: int):
        self.service_name = service_name
        self.tripped_at = tripped_at
        self.recovery_time_sec = recovery_time_sec
        self.failure_count = failure_count
        self.retry_after_sec = max(0.0, round(recovery_time_sec - (time.time() - tripped_at), 2))
        super().__init__(
            f"[{service_name}] Circuit OPEN — {failure_count} failures. "
            f"Retry after {self.retry_after_sec}s."
        )


class ServiceChassisResilience:
    def __init__(self, service_name: str = "downstream", failure_threshold: int = 3, recovery_time_sec: float = 5.0):
        """
        Circuit Breaker States:
        - CLOSED: Normal operation.
        - OPEN: Tripped due to failures; rejects requests immediately.
        - HALF-OPEN: Testing downstream recovery after recovery_time_sec.
        """
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_state_change = time.time()

    def circuit_breaker(self, fallback_function: Callable = Any) -> Callable[[Any], Any]:
        """
        Reusable decorator for developer endpoints.
        circuit_breaker(fallback_function)  ← accepts a fallback
        └── decorator(func)                 ← wraps your actual function
            └── wrapper(*args)              ← runs on every call
        """

        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                now = time.time()

                # Check if OPEN state has expired -> Transition to HALF-OPEN
                if self.state == "OPEN":
                    if now - self.last_state_change >= self.recovery_time_sec:
                        self.state = "HALF-OPEN"
                        self.last_state_change = now
                        logger.info("⚡ [CIRCUIT HALF-OPEN] Testing downstream service health...")
                    else:
                        logger.warning("🚨 [CIRCUIT OPEN] Request blocked immediately to prevent cascading overload.")
                        exc = CircuitBreakerOpenException(
                            self.service_name, self.last_state_change,
                            self.recovery_time_sec, self.failure_count
                        )
                        if fallback_function:
                            return fallback_function(*args, exception=exc, **kwargs)
                        raise exc

                try:
                    result = func(*args, **kwargs)

                    # Success path: Reset on successful invocation
                    if self.state in ["HALF-OPEN", "CLOSED"]:
                        self.failure_count = 0
                        self.state = "CLOSED"
                    return result

                except Exception as e:
                    self.failure_count += 1
                    logger.error(f"Execution error (Failure {self.failure_count}/{self.failure_threshold}): {str(e)}")

                    if self.failure_count >= self.failure_threshold:
                        self.state = "OPEN"
                        self.last_state_change = time.time()
                        logger.critical(f"🔥 [CIRCUIT TRIPPED to OPEN] Failure threshold reached.")

                    if fallback_function:
                        return fallback_function(*args, exception=e, **kwargs)
                    raise e

            return wrapper

        return decorator


# ==========================================
# VERIFICATION & TEST HARNESS
# ==========================================
def CachedFallbackResponse(*args, exception: Exception = None, **kwargs) -> dict:
    if isinstance(exception, CircuitBreakerOpenException):
        return {
            "status": "degraded",
            "data": "Serving cached static response.",
            "from_cache": True,
            "service": exception.service_name,
            "failures": exception.failure_count,
            "retry_after_sec": exception.retry_after_sec,
        }
    return {
        "status": "error",
        "data": "Serving cached static response.",
        "from_cache": True,
        "reason": str(exception) if exception else "Unknown error",
    }


# Instantiate shared resilience Chassis component
resilience_guard = ServiceChassisResilience(service_name="payment-db", failure_threshold=2, recovery_time_sec=3.0)


@resilience_guard.circuit_breaker(fallback_function=CachedFallbackResponse)
def unstable_downstream_service(should_fail: bool):
    if should_fail:
        raise ConnectionError("Database Connection Timeout (504)")
    return {"status": "success", "data": "Fresh DB query payload"}


if __name__ == "__main__":
    print("\n--- 1. SUCCESSFUL INVOCATION ---")
    print(unstable_downstream_service(should_fail=False))

    print("\n--- 2. ENCOUNTERING DOWNSTREAM FAILURES ---")
    print(unstable_downstream_service(should_fail=True))  # Failure 1
    print(unstable_downstream_service(should_fail=True))  # Failure 2 -> Trips Circuit to OPEN!

    print("\n--- 3. CALLING WHILE CIRCUIT IS OPEN (Instant Fallback) ---")
    try:
        print(unstable_downstream_service(should_fail=False))  # Blocked automatically without touching DB!
    except CircuitBreakerOpenException as e:
        print(f"Caught: {e}")
        print(f"  → service     : {e.service_name}")
        print(f"  → failures    : {e.failure_count}")
        print(f"  → retry after : {e.retry_after_sec}s")

    print("\n--- 4. WAITING FOR RECOVERY WINDOW (3 Sec) ---")
    time.sleep(3.2)

    print("\n--- 5. HALF-OPEN STATE RECOVERY TEST ---")
    print(unstable_downstream_service(should_fail=False))  # Recovers to CLOSED!
