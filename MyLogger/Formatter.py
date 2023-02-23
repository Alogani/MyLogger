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

from datetime import datetime


class _DefaultDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


class Formatter:
    def __init__(self, message_format: str = "{message}", time_format: str = "%Y-%m-%d %H:%M:%S") -> None:
        """message_format -- available variables : time, message, event\n
        time_format -- every_format accepted by datetime.strftime"""
        self.message_format = message_format
        self.time_format = time_format

    def __call__(self, formatter_dict: dict[str, str]) -> str:
        formatter_dict["time"] = datetime.now().strftime(self.time_format)
        return self.message_format.format_map(_DefaultDict(**formatter_dict))
