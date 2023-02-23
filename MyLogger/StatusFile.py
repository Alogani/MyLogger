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

import csv


class StatusFile:
    """This code is standalone and is not part of MyLogger. But I find its usage close, so here it is"""
    def __init__(self, file_path: str, sep: str = ';'):
        self.file_path = file_path
        self.sep = sep

    def update(self, identifier: str, success: bool, time: str):
        save_date = time if success else ""
        status = "success" if success else "fail"

        with open(self.file_path, "r") as file:
            data = list(csv.reader(file, delimiter=self.sep))

        matched = False
        for row in data:
            if row[0] == identifier:
                row[1] = save_date if success else row[1]
                row[2] = status
                matched = True

        if not matched:
            data.append([identifier, save_date, status])

        with open(self.file_path, "w") as file:
            csv.writer(file, delimiter=";").writerows(data)
