#!/usr/bin/env python

from i3ipc.aio import Connection
from i3ipc import Event
from collections import namedtuple
import asyncio
import time

i3 = await Connection().connect()

#EventHandler = namedtuple('EventHandler', ['event', 'handler'])
#
#
#def OnWindowFocus(i3, e):
#    print(f'{time.time()} : Window Focus Event: {e.name}')
#
#
#WindowFocusEvent = EventHandler(event=Event.WINDOW_FOCUS.value,
#                                handler=OnWindowFocus)
#
#i3.on(WindowFocusEvent.event, WindowFocusEvent.handler)
#
#await i3.main()
