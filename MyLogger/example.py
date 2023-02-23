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


class MyEvent(LogEvent):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ALERT = auto()
    OPEN = auto()


# BASIC USAGE for anyone !
logger = Logger()
logger.addToEvent(MyEvent.INFO, ConsoleHandler())

logger.log(MyEvent.INFO, "First logging")

# LET'S SEE FILES
logger.addToEvent([MyEvent.WARNING, MyEvent.ALERT, MyEvent.OPEN],
                  [FileHandler(CountFifoRotator(file_path="test_file.log", max_files=3)),
                   FileHandler(TimedFifoRotator(file_path="test_file_2.log", max_days=10, min_files=3))
                   ])

# OH, THERE IS CUSTOMIZATION
logger.associateEvent(MyEvent.INFO, MyEvent.WARNING)
logger.addToEvent("NOTIF", NotificationHandler())  # Using non-enums (note : ugly but works)

# OK, ENOUGH DEFINITION, TIME TO LOG
logger.log(MyEvent.INFO, "Second logging")
logger.log([MyEvent.WARNING, "NOTIF"], "Log to multiple different places")  # This will also log to INFO if you follow
logger.log(MyEvent.DEBUG, "This will not be shown")  # Because debug is not defined, but it's useful to have some !

# SPECIAL LOGGING WAY : as a file !
with logger.open([MyEvent.OPEN, MyEvent.WARNING]) as f:
    f.write("This is a direct log writing")
    subprocess.run(["echo", "Hello log"], stdout=f, stderr=subprocess.STDOUT)

# Extend customization by defining child logger
logger2 = logger.copy()
logger2.clearEvent(MyEvent.INFO)
logger2.addToEvent(MyEvent.INFO, ConsoleHandler(formatter=Formatter("LOGGER2 - {event} - {time} - {message}")))
logger2.log(MyEvent.INFO, "last logging")


# DECORATOR TO CATCH EXCEPTIONS or replace print method
@LogCatcher(logger, MyEvent.INFO, message_format="Here is a special exception:\n---\n{exception}\n---\n")
def failure_func():
    raise Exception("Ouch")


@PrintCatcher(logger, MyEvent.INFO, message_format="Here are print args:\n---\n{print_arg}\n---\n")
def printer():
    print("Catch this if you can", "and this", sep='\n')
    print("and again")


failure_func()
printer()
