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
import subprocess
from io import TextIOWrapper
from typing import Union

from MyLogger.Formatter import Formatter
from MyLogger.FileFaker import FileFaker
from MyLogger.FileRotator import _FileRotator


class _BaseHandler:
    def __init__(self, formatter: Formatter = Formatter()) -> None:
        if self.__class__ == _BaseHandler:
            raise TypeError("BaseClass is not meant to be instantiated directly")
        self.format = formatter

    def emit(self, message: str, formatter_dict: dict[str, str]) -> None:
        self._emit(self.format(message, formatter_dict))

    def _emit(self, message: str) -> None:
        raise NotImplementedError("Subclass must implement abstract method")

    def open(self, open_mode: str = 'a') -> Union[FileFaker, TextIOWrapper]:
        return FileFaker(lambda content: self._emit(content))


class NoneHandler(_BaseHandler):
    def _emit(self, *args) -> None:
        pass


class ConsoleHandler(_BaseHandler):
    def __init__(self, formatter: Formatter = Formatter("{context} - {time} - {message}")) -> None:
        super().__init__(formatter)

    def _emit(self, message: str) -> None:
        print(message)


class NotificationHandler(_BaseHandler):
    def __init__(self, title: str = "MyLogger", isCritical: bool = False,
                 formatter: Formatter = Formatter("{message}")) -> None:
        super().__init__(formatter)
        self.title = title
        self.isCritical = isCritical

    def _emit(self, message: str) -> None:
        if self.isCritical:
            option = "--urgency=critical"
        else:
            option = "--urgency=normal"

        has_gui = os.getenv("DISPLAY") != ""
        if not has_gui:
            return

        who_output = subprocess.run(["who"], stdout=subprocess.PIPE).stdout.decode("utf-8")
        users = set([line.split(" ")[0] for line in who_output.split("\n") if line])
        for user in users:
            user_id = subprocess.run(["id", "-u", user], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
            subprocess.run(
                ["sudo", "-u", user, "DISPLAY=:0", f"DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{user_id}/bus",
                 "notify-send", option, self.title, message])


class SystemHandler(_BaseHandler):
    def __init__(self, title: str = "MyLogger", formatter: Formatter = Formatter("{context} - {message}")) -> None:
        super().__init__(formatter)
        self.title = title

    def _emit(self, message: str) -> None:
        subprocess.run(["logger", "-t", self.title, message])


class FileHandler(_BaseHandler):

    def __init__(self, file_rotator: _FileRotator,
                 formatter: Formatter = Formatter("{time} - {context} - {message}")) -> None:
        super().__init__(formatter)
        self.file_rotator = file_rotator

    def _emit(self, message: str) -> None:

        with self.open('a') as f:
            f.write(f"{message}\n")

    def open(self, open_mode: str = 'a') -> TextIOWrapper:
        return open(self.file_rotator.getPath(), open_mode)
