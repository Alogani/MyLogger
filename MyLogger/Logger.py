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

from MyLogger.LogEvent_interface import LogEvent
from MyLogger.LogHandler import _BaseHandler
from MyLogger.FileFaker import MultipleFileFaker
from typing import Union


class Logger:
    def __init__(self, event: dict[LogEvent, list[_BaseHandler]] = None) -> None:
        self._events = event if event else {}
        self._event_association = {}

    def addToEvent(self, event_name: Union[LogEvent, list[LogEvent]],
                   handler: Union[_BaseHandler, list[_BaseHandler]]):
        event_namelist = event_name if type(event_name) == list else [event_name]
        handler_list = handler if type(handler) == list else [handler]

        for name in event_namelist:
            if name not in self._events:
                self._events[name] = handler_list.copy()
            else:
                for handler in handler_list:
                    self._events[name].append(handler)

    def clearEvent(self, event_name: Union[LogEvent, list[LogEvent]]):
        event_namelist = event_name if type(event_name) == list else [event_name]

        for event in event_namelist:
            if event in self._events:
                self._events[event] = []

    def associateEvent(self, event_target: Union[LogEvent, list[LogEvent]],
                       event_source: Union[LogEvent, list[LogEvent]]):
        """event_target will be called each time event_source will be used"""
        target_namelist = event_target if type(event_target) == list else [event_target]
        source_namelist = event_source if type(event_source) == list else [event_source]

        for source in source_namelist:
            if source not in self._event_association:
                self._event_association[source] = target_namelist
            else:
                for target in target_namelist:
                    self._event_association[source].append(target)

    def _populateEventWithAssociation(self, event_name: Union[LogEvent, list[LogEvent]]) \
            -> tuple[list[LogEvent], list[LogEvent]]:
        event_namelist = event_name if type(event_name) == list else [event_name]

        event_referent = event_namelist.copy()

        i = 0
        while i < len(event_namelist):
            search_event = event_namelist[i]
            for new_event in self._event_association.get(search_event, []):
                if new_event not in event_namelist:
                    event_namelist.append(new_event)
                    event_referent.append(event_referent[i])

            i += 1

        return event_namelist, event_referent

    def copy(self) -> 'Logger':
        new_event = self._events.copy()
        for key in new_event:
            new_event[key] = self._events[key].copy()
        return Logger(new_event)

    def log(self, event_name: Union[LogEvent, list[LogEvent]], message: str) -> None:
        event_namelist, event_referent = self._populateEventWithAssociation(event_name)

        for name, referent in zip(event_namelist, event_referent):
            for handler in self._events.get(name, []):
                handler.emit(formatter_dict={"message": message, "event": str(referent)})

    def open(self, event_name: Union[LogEvent, list[LogEvent]], mode: str = 'a') -> MultipleFileFaker:
        """With this function, logging will not be formatted.
        File writing will be optimized."""
        event_namelist = self._populateEventWithAssociation(event_name)[0]

        return MultipleFileFaker([handler.open(mode)
                                  for name in event_namelist
                                  for handler in self._events.get(name, [])])
