from typing import Sized

import sys


class ListChunker:
    """
    Wrapper to iterate over potentially large lists in chunks.  We use this to commit large volumes of data in
    batches.
    """
    def __init__(self, lst: Sized, interval: int, print_progress: bool = True) -> None:
        """
        Iterator that returns elements of lst in chunks of size interval or less
        :param lst: List to be returned in batches
        :param interval: chunk size
        :param print_progress: True means print a '.' on stdout per chunk
        """
        self.input = lst
        self.interval = interval
        self._pos = 0
        self._dotted = False
        self._print_progress = print_progress

    def __iter__(self):
        return self

    def __next__(self) -> Sized:
        if self._pos < len(self.input):
            start = self._pos
            self._pos = self._pos + self.interval
            if self._pos < len(self.input) and self._print_progress:
                print('.', end='')
                sys.stdout.flush()
                self._dotted = True
            return self.input[start:self._pos]
        else:
            if self._dotted:
                print()
            raise StopIteration
