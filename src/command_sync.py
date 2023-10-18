import functools
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable


class MockAPI:

    def mock_wait_action_completion(self) -> bool:
        """
        Simulation of an API call that will only return when a given action is completed.
        """
        return True


def sync_command(action_name: str, timeout_sec: float = 10) -> Callable[..., Callable[..., bool]]:
    """
    Triggers a concurrent future method that will keep running until a given action from an external API is completed.

    :param action_name: Name of the service that the API is supposed to wait its completion.
    :param timeout_sec: Time in seconds to raise an error, if the service is not finished until the timeout is reached.
    :return: The result from the API called.
    """
    def decorator(callback: Callable[..., Any]) -> Callable[..., bool]:

        @functools.wraps(callback)
        def execute_and_sync(self: MockAPI, *args: Any, **kwargs: Any) -> bool:
            wait_command: Callable[[], bool] = lambda: self.mock_wait_action_completion()
            with ThreadPoolExecutor(max_workers=1) as executor:
                future: Future[Any] = executor.submit(wait_command)
                callback(self, *args, **kwargs)
                try:
                    result: bool = future.result(timeout_sec)
                    return result
                except Exception:
                    raise TimeoutError(f'Could not get a response from {action_name=} after waiting {timeout_sec=}')

        return execute_and_sync

    return decorator
