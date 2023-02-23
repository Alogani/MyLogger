from typing import Union

from MyLogger import Logger, LogEvent, Formatter, FileFaker


def LogCatcher(logger: Logger, event: Union[LogEvent, list[LogEvent]], message_format: str = "{exception}"):
    """Usage @LogCatcher(logger_instance, event, message)"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                message = Formatter(message_format)({"exception": str(e)})
                logger.log(event, message)
                raise e

        return wrapper

    return decorator


def PrintCatcher(logger: Logger, event: Union[LogEvent, list[LogEvent]], message_format: str = "{print_arg}"):
    """Usage @PrintCatcher(logger_instance, event, message)"""

    def _print(*args, **kwargs):
        fifo = FileFaker()
        kwargs["file"] = fifo
        print(*args, **kwargs)
        message = Formatter(message_format)({"print_arg": fifo.read()})
        logger.log(event, message)

    def decorator(func):
        def wrapper(*args, **kwargs):
            func.__globals__["print"] = _print
            return func(*args, **kwargs)

        return wrapper

    return decorator
