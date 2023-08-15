#!/usr/bin/env python3

from datetime import datetime, timedelta
from ics import Calendar, Event, alarm, Attendee

c = Calendar()
e = Event()
e.name = "哈哈"
e.description = "A meaningful description"
e.begin = datetime.fromisoformat("2023-08-14T12:05:23+08:00")
e.end = datetime.fromisoformat("2023-08-14T13:05:23+08:00")
e.created = datetime.now()
e.alarms.append(alarm.EmailAlarm(trigger=timedelta(hours=-2), subject='subject', body='body', recipients=[Attendee('x@x.com')]))
c.events.add(e)

print(c.serialize())