"""
MIT License

MyLogger
Copyright (c) 2023 Alogani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import time


def _touch_file(file_path: str) -> None:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('')


class _FileRotator:
    rotated_files: list[str] = []

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path

    def getPath(self):
        if self.should_rollover():
            self.rollover()
        return self.file_path

    def should_rollover(self) -> bool:
        if self.file_path in _FileRotator.rotated_files:
            return False
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            _FileRotator.rotated_files.append(self.file_path)
            return False
        else:
            _FileRotator.rotated_files.append(self.file_path)
            return True

    def rollover(self) -> None:
        raise NotImplementedError("Subclass must implement abstract method")


class CountFifoRotator(_FileRotator):
    def __init__(self, file_path: str, max_files: int) -> None:
        super().__init__(file_path)
        self.max_files = max_files

    def rollover(self) -> None:
        rotation_order = [self.file_path]
        remove_last = True
        for i in range(1, self.max_files + 1):
            next_file = "%s.%d" % (self.file_path, i)
            rotation_order.append(next_file)
            if not os.path.exists(next_file):
                remove_last = False
                break

        if remove_last:
            os.remove(rotation_order[-1])
        for i in range(len(rotation_order)-1, 0, -1):
            source = rotation_order[i - 1]
            destination = rotation_order[i]
            os.rename(source, destination)


class TimedFifoRotator(_FileRotator):
    def __init__(self, file_path: str, max_days: int, min_files: int) -> None:
        super().__init__(file_path)
        self.max_days = max_days
        self.min_files = min_files

    def rollover(self) -> None:
        current_time = time.time()
        remove_last = True

        rotation_order = [self.file_path]
        i = 1
        while True:
            next_file = "%s.%d" % (self.file_path, i)
            i += 1
            rotation_order.append(next_file)
            if not os.path.exists(next_file):
                remove_last = False
                break
            if (i > self.min_files and
                    current_time - os.path.getctime(next_file) >= self.max_days * 24 * 3600):
                break

        if remove_last:
            os.remove(rotation_order[-1])
        for i in range(len(rotation_order)-1, 0, -1):
            source = rotation_order[i - 1]
            destination = rotation_order[i]
            os.rename(source, destination)
