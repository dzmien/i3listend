#!/usr/bin/env python

# i3listend is a configurable i3wm event listener

from i3ipc.aio import (Con, Connection)
from i3ipc import Event
# import i3ipc


from collections import (OrderedDict, namedtuple)
from dataclasses import dataclass
import asyncio
import time


def timestamp(fmt='%Y-%m-%dT%H:%M:%S'):
    return time.strftime(fmt, time.localtime())


I3EventHandler = namedtuple('I3EventHandler', ['event', 'handler'])


@dataclass
class I3StateVars():
    """Class to store relevant wm state variables
    all containers are stored by their id.
    """
    focused_window: int
    focused_workspace: int
    focus_stack: OrderedDict


@dataclass
class SimpleCon():
    con_id: int
    name: str


class I3SimpleTree():
    def __init__(self):
        self.focused = {'output': None,
                        'workspace': None,
                        'window': None}


class I3ListenDaemon():
    def __init__(self):
        self.i3 = None
        self.first_run = True
        self.registered_handlers = []
        self.tree = None
        self.wm_focused = {'window': None, 'workspace': None}
        self.wm_focus_stack = OrderedDict()
        self.wm_state = I3StateVars()

    async def connect(self):
        self.i3 = await Connection().connect()
        await self.update_tree()
        self.first_run = False

    async def update_state(self):
        self.tree = await self.i3.get_tree()
        self.wm_state.focused_window = self.tree.find_focused()

    async def register_event_handler(self, event_handler: I3EventHandler):
        event, handler = event_handler
        if self.registered_handlers.count(event_handler):
            print(f'Event {event.value} and handler \
                  {handler.__name__} already registered')
            return
        else:
            self.i3.on(event.value, handler)
            self.registered_handlers.append(event_handler)

    async def unregister_event_handler(self, event_handler: I3EventHandler):
        event, handler = event_handler
        try:
            self.registered_handlers.remove(event_handler)
        except ValueError:
            print(f'Handler {handler.__name__} not registered')
            return
        self.i3.off(handler)

    async def run(self):
        await self.i3.main()


async def listen_daemon():
    async def OnWindowFocus(i3, e):
        parent = e.container
        parent_info = parent.name
        print(
            f'{timestamp()} : {parent_info}')

    WindowFocusEvent = I3EventHandler(event=Event.WINDOW_FOCUS,
                                      handler=OnWindowFocus)
    listend = I3ListenDaemon()
    await listend.connect()
    await listend.update_tree()
    await listend.register_event_handler(WindowFocusEvent)
    await listend.run()


if __name__ == '__main__':
    try:
        asyncio.run(listen_daemon())
    except KeyboardInterrupt:
        print('\ngot KeyboardInterrupt, stopping daemon')
