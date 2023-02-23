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

import _io
from typing import Union


class FileFaker:
    def __init__(self, exit_callback=lambda content: None):
        self.content = ""
        self._exit_callback = exit_callback

        self._fileno = -1

    def write(self, string: str) -> None:
        self.content += string

    def read(self) -> str:
        return self.content

    def close(self):
        pass

    def fileno(self):
        return self._fileno

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._exit_callback(self.content)


class MultipleFileFaker:
    def __init__(self, file_fakers: list[Union[FileFaker, _io.TextIOWrapper]]):
        self.file_fakers = file_fakers
        self.mode = ''

        self._fileno = -1

    def write(self, string: str) -> None:
        for file_faker in self.file_fakers:
            file_faker.write(string)

    def read(self) -> list[str]:
        return [file_faker.read() for file_faker in self.file_fakers]

    def close(self):
        for file_faker in self.file_fakers:
            file_faker.close()

    def fileno(self):
        return self._fileno

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for file_faker in self.file_fakers:
            file_faker.__exit__(exc_type, exc_value, traceback)
