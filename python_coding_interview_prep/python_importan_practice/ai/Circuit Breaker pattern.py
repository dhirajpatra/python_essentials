"""
Key Features:
Three States:
CLOSED: Normal operation, requests flow through
OPEN: Failures exceeded threshold, fast-fail
HALF_OPEN: Testing recovery with limited requests
Configurable Parameters:
failure_threshold: Failures before opening circuit
recovery_timeout: Wait time before testing recovery
half_open_max_calls: Successful calls needed to close
Thread-Safe: Uses locks for concurrent access
Monitoring: Callback for state change notifications
Two Usage Patterns: Decorator and class-based
"""
import time
from enum import Enum
from functools import wraps
from threading import Lock


class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation, requests flow through
    OPEN = "open"  # Circuit is tripped, requests fail fast
    HALF_OPEN = "half_open"  # Testing if service has recovered


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open"""
    pass


class CircuitBreaker:
    """
    Circuit Breaker implementation to prevent cascading failures.

    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Failures exceeded threshold, requests fail immediately
    - HALF_OPEN: Testing recovery, limited requests allowed
    """

    def __init__(
            self,
            failure_threshold=5,
            recovery_timeout=30,
            half_open_max_calls=1,
            expected_exceptions=(Exception,),
            monitor_callback=None
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before trying half-open
            half_open_max_calls: Max calls allowed in half-open state
            expected_exceptions: Exceptions that count as failures
            monitor_callback: Optional callback for state changes
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.expected_exceptions = expected_exceptions
        self.monitor_callback = monitor_callback

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0
        self._last_failure_time = None
        self._lock = Lock()

    @property
    def state(self):
        """Get current circuit state, checking for timeout transitions"""
        with self._lock:
            if self._state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self._transition_to(CircuitState.HALF_OPEN)
            return self._state

    def _should_attempt_reset(self):
        """Check if enough time has passed to attempt reset"""
        if self._last_failure_time is None:
            return False
        elapsed = time.time() - self._last_failure_time
        return elapsed >= self.recovery_timeout

    def _transition_to(self, new_state):
        """Transition to a new state"""
        old_state = self._state
        self._state = new_state

        if new_state == CircuitState.CLOSED:
            self._failure_count = 0
            self._success_count = 0
            self._half_open_calls = 0
        elif new_state == CircuitState.HALF_OPEN:
            self._half_open_calls = 0
            self._success_count = 0

        if self.monitor_callback:
            self.monitor_callback(old_state, new_state)

        print(f"Circuit breaker: {old_state.value} -> {new_state.value}")

    def call(self, func, *args, **kwargs):
        """
        Execute function through circuit breaker.

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result of function execution

        Raises:
            CircuitBreakerError: If circuit is open
        """
        current_state = self.state

        if current_state == CircuitState.OPEN:
            raise CircuitBreakerError(
                f"Circuit breaker is OPEN. Service unavailable. "
                f"Will retry after {self.recovery_timeout}s"
            )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise

    def _on_success(self):
        """Handle successful call"""
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.half_open_max_calls:
                    self._transition_to(CircuitState.CLOSED)
            elif self._state == CircuitState.CLOSED:
                # Reset failure count on success
                self._failure_count = 0

    def _on_failure(self):
        """Handle failed call"""
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == CircuitState.HALF_OPEN:
                # Any failure in half-open goes back to open
                self._transition_to(CircuitState.OPEN)
            elif self._state == CircuitState.CLOSED:
                if self._failure_count >= self.failure_threshold:
                    self._transition_to(CircuitState.OPEN)


# Decorator for easy usage
def circuit_breaker(
        failure_threshold=5,
        recovery_timeout=30,
        half_open_max_calls=1,
        expected_exceptions=(Exception,),
        monitor_callback=None
):
    """
    Decorator to apply circuit breaker to a function.

    Args:
        failure_threshold: Number of failures before opening circuit
        recovery_timeout: Seconds to wait before trying half-open
        half_open_max_calls: Max calls allowed in half-open state
        expected_exceptions: Exceptions that count as failures
        monitor_callback: Optional callback for state changes
    """

    def decorator(func):
        cb = CircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            half_open_max_calls=half_open_max_calls,
            expected_exceptions=expected_exceptions,
            monitor_callback=monitor_callback
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            return cb.call(func, *args, **kwargs)

        # Expose circuit breaker instance for monitoring
        wrapper.circuit_breaker = cb
        return wrapper

    return decorator


# Example usage with monitoring
def state_change_monitor(old_state, new_state):
    """Monitor circuit breaker state changes"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] State change: {old_state.value} → {new_state.value}")


@circuit_breaker(
    failure_threshold=3,
    recovery_timeout=10,
    half_open_max_calls=2,
    expected_exceptions=(ConnectionError, TimeoutError),
    monitor_callback=state_change_monitor
)
def unreliable_service_call(data):
    """Simulates an unreliable external service call"""
    import random

    # Simulate occasional failures
    if random.random() < 0.7:  # 70% failure rate for demo
        raise ConnectionError("Service temporarily unavailable")

    return {"status": "success", "data": data}


# Class-based usage example
class ServiceClient:
    """Example service client with circuit breaker"""

    def __init__(self):
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=30,
            expected_exceptions=(ConnectionError, TimeoutError)
        )

    def make_request(self, url):
        """Make HTTP request with circuit breaker protection"""
        import requests

        def do_request():
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()

        return self.circuit_breaker.call(do_request)

    def get_circuit_state(self):
        """Get current circuit breaker state"""
        return self.circuit_breaker.state


if __name__ == "__main__":
    print("=== Testing Circuit Breaker ===\n")

    # Test 1: Using decorator
    print("Test 1: Decorator approach")
    print("-" * 40)

    for i in range(10):
        try:
            result = unreliable_service_call(f"request_{i}")
            print(f"Request {i}: SUCCESS - {result}")
        except CircuitBreakerError as e:
            print(f"Request {i}: CIRCUIT OPEN - {e}")
        except ConnectionError as e:
            print(f"Request {i}: FAILED - {e}")

        time.sleep(1)

    print("\n" + "=" * 50 + "\n")

    # Test 2: Using class-based approach
    print("Test 2: Class-based approach")
    print("-" * 40)

    client = ServiceClient()

    for i in range(8):
        try:
            # Simulate failures
            if i < 6:
                raise ConnectionError("Simulated failure")

            result = client.make_request("https://api.example.com/data")
            print(f"Request {i}: SUCCESS")
        except CircuitBreakerError as e:
            print(f"Request {i}: CIRCUIT OPEN - {e}")
        except ConnectionError as e:
            print(f"Request {i}: FAILED - {e}")

        time.sleep(1)

    print(f"\nFinal circuit state: {client.get_circuit_state().value}")
