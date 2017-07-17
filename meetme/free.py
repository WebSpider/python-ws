#!/usr/bin/env python
from config import mypass
from pytz import timezone
from datetime import datetime, timedelta
from exchangelib import DELEGATE, IMPERSONATION, Account, Credentials, ServiceAccount, \
    EWSDateTime, EWSTimeZone, Configuration, NTLM, CalendarItem, Message, \
    Mailbox, Attendee, Q, ExtendedProperty, FileAttachment, ItemAttachment, \
    HTMLBody, Build, Version

# Username in WINDOMAIN\username format. Office365 wants usernames in PrimarySMTPAddress
# ('myusername@example.com') format. UPN format is also supported.
credentials = Credentials(username='AD\\nils', password=mypass)
config = Configuration(server='mail.surfnet.nl', credentials=credentials)

rooms = [ 'kamer3.1@surf.nl', 'kamer3.5@surf.nl' ]

accounts = []
for room in rooms:
  roomacct = Account(primary_smtp_address=room, config=config, autodiscover=False, access_type=DELEGATE)
  accounts.append(roomacct)

#for room in accounts:
#  tz = timezone("Europe/Amsterdam")
#  cal_items = room.calendar.filter(start__lt=tz.localize(EWSDateTime(2017,7,18)), end__gt=tz.localize(EWSDateTime(2017,7,17)))
#  for appt in cal_items.all():
#    print appt.subject, appt.location, appt.start, appt.end

tz = timezone("Europe/Amsterdam")
for room in accounts:

  begin = datetime.now()
  end = begin + timedelta(hours=1)
  cal_items_now = room.calendar.filter(start__lt=tz.localize(EWSDateTime.from_datetime(end)), end__gt=tz.localize(EWSDateTime.from_datetime(begin)))
  if cal_items_now.exists():
    for appt in cal_items_now:
      print "KAMER BEZET: ", appt.subject, appt.location, appt.start, appt.end
  else:
    print "Geen afspraken voor", room.primary_smtp_address, "tussen ", begin, "en ", end
