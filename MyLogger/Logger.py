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

from MyLogger.Context_interface import Context
from MyLogger.LogHandler import _BaseHandler
from MyLogger.FileFaker import MultipleFileFaker
from typing import Union


class Logger:
    def __init__(self, context: dict[Context, list[_BaseHandler]] = None) -> None:
        self._contexts = context if context else {}
        self._context_association = {}

    def addToContext(self, context_name: Union[Context, list[Context]],
                     handler: Union[_BaseHandler, list[_BaseHandler]]):
        context_namelist = context_name if type(context_name) == list else [context_name]
        handler_list = handler if type(handler) == list else [handler]

        for name in context_namelist:
            if name not in self._contexts:
                self._contexts[name] = handler_list.copy()
            else:
                for handler in handler_list:
                    self._contexts[name].append(handler)

    def clearContext(self, context_name: Union[Context, list[Context]]):
        context_namelist = context_name if type(context_name) == list else [context_name]

        for context in context_namelist:
            if context in self._contexts:
                self._contexts[context] = []

    def associateContext(self, context_target: Union[Context, list[Context]],
                         context_source: Union[Context, list[Context]]):
        """context_target will be called each time context_source will be used"""
        target_namelist = context_target if type(context_target) == list else [context_target]
        source_namelist = context_source if type(context_source) == list else [context_source]

        for source in source_namelist:
            if source not in self._context_association:
                self._context_association[source] = target_namelist
            else:
                for target in target_namelist:
                    self._context_association[source].append(target)

    def _populateContextWithAssociation(self, context_name: Union[Context, list[Context]])\
            -> tuple[list[Context], list[Context]]:
        context_namelist = context_name if type(context_name) == list else [context_name]

        context_referent = context_namelist.copy()

        i = 0
        while i < len(context_namelist):
            search_context = context_namelist[i]
            for new_context in self._context_association.get(search_context, []):
                if new_context not in context_namelist:
                    context_namelist.append(new_context)
                    context_referent.append(context_referent[i])

            i += 1

        return context_namelist, context_referent

    def copy(self) -> 'Logger':
        new_context = self._contexts.copy()
        for key in new_context:
            new_context[key] = self._contexts[key].copy()
        return Logger(new_context)

    def log(self, context_name: Union[Context, list[Context]], message: str) -> None:
        context_namelist, context_referent = self._populateContextWithAssociation(context_name)

        for name, referent in zip(context_namelist, context_referent):
            for handler in self._contexts.get(name, []):
                handler.emit(message, formatter_dict={"context": str(referent)})

    def open(self, context_name: Union[Context, list[Context]], mode: str = 'a') -> MultipleFileFaker:
        """With this function, logging will not be formatted.
        File writing will be optimized."""
        context_namelist = self._populateContextWithAssociation(context_name)[0]

        return MultipleFileFaker([handler.open(mode)
                                  for name in context_namelist
                                  for handler in self._contexts.get(name, [])])
