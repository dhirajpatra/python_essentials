"""
When transforming developer teams from monolithic applications to microservices,
teams often implement ad-hoc retry loops that cause cascading database failures under load.

Build a reusable Circuit Breaker and Token Bucket Rate Limiter module in Python
that developers can apply as a decorator to their microservice endpoints to handle
external service degradation gracefully.
"""
import time
import functools
import logging
from typing import Callable, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ChassisResilience")


class CircuitBreakerOpenException(Exception):
    """Raised when the circuit breaker is in OPEN state."""
    pass


class ServiceChassisResilience:
    def __init__(self, failure_threshold: int = 3, recovery_time_sec: float = 5.0):
        """
        Circuit Breaker States:
        - CLOSED: Normal operation.
        - OPEN: Tripped due to failures; rejects requests immediately.
        - HALF-OPEN: Testing downstream recovery after recovery_time_sec.
        """
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_state_change = time.time()

    def circuit_breaker(self, fallback_function: Callable = Any):
        """
        Reusable decorator for developer endpoints.
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
                        if fallback_function:
                            return fallback_function(*args, **kwargs)
                        raise CircuitBreakerOpenException("Service downstream is unavailable.")

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
                        return fallback_function(*args, **kwargs)
                    raise e

            return wrapper

        return decorator


# ==========================================
# VERIFICATION & TEST HARNESS
# ==========================================
def CachedFallbackResponse(*args, **kwargs):
    return {"status": "degraded", "data": "Serving cached static response.", "from_cache": True}


# Instantiate shared resilience Chassis component
resilience_guard = ServiceChassisResilience(failure_threshold=2, recovery_time_sec=3.0)


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
    print(unstable_downstream_service(should_fail=False))  # Blocked automatically without touching DB!

    print("\n--- 4. WAITING FOR RECOVERY WINDOW (3 Sec) ---")
    time.sleep(3.2)

    print("\n--- 5. HALF-OPEN STATE RECOVERY TEST ---")
    print(unstable_downstream_service(should_fail=False))  # Recovers to CLOSED!