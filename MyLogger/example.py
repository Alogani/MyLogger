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

from enum import auto

from __init__ import *


class MyContext(Context):
    NOTIF = auto()
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ALERT = auto()
    OPEN = auto()


logger = Logger()
logger.addToContext(MyContext.INFO, ConsoleHandler())
logger.addToContext([MyContext.WARNING, MyContext.ALERT, MyContext.OPEN],
                    FileHandler(CountFifoRotator(file_path="test_file.log", max_files=3)))
logger.associateContext(MyContext.INFO, MyContext.WARNING)
logger.addToContext("NOTIF", NotificationHandler())


logger2 = logger.copy()
logger2.clearContext(MyContext.INFO)
logger2.addToContext(MyContext.INFO, ConsoleHandler(formatter=Formatter("LOGGER2 - {context} - {time} - {message}")))

logger.log(MyContext.INFO, "First logging")
logger.log([MyContext.WARNING, "NOTIF"], "Log to multiple levels")
logger.log(MyContext.DEBUG, "This will not be shown")

with logger.open([MyContext.OPEN, MyContext.WARNING]) as f:
    f.write("This is a direct log writing")

with logger.open(MyContext.OPEN) as f:
    subprocess.run(["echo", "Hello log"], stdout=f, stderr=subprocess.STDOUT)

logger2.log(MyContext.INFO, "test")
