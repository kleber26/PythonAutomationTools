import time
from typing import Callable


class Poller:

    @staticmethod
    def until_true(condition_callback: Callable[[], bool], timeout: float, polling_rate: float = 0.01) -> bool:
        start = time.time()
        while not condition_callback() and time.time() - start < timeout:
            time.sleep(polling_rate)

        if time.time() - start > timeout:
            return False
        return True
