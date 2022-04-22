from datetime import datetime
from dateutil.easter import *
from dateutil import rrule
from dateutil.relativedelta import relativedelta
#https://gist.github.com/adamJLev/7535869
start = datetime(2021, 1, 1)

def get_schedule_holidays_rrules():
  return [
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, bymonth=1, bymonthday=1),              # New Years
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, bymonth=5, byweekday=rrule.MO(-1)),    # Memorial
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, bymonth=7, bymonthday=4),              # Independence
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, bymonth=11, byweekday=rrule.TH(4)),    # Thanksgiving
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, bymonth=12, bymonthday=25),            # Christmas
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, bymonth=6, bymonthday=19),
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, bymonth=9, byweekday=rrule.MO(1)),
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, bymonth=2, bymonthday=21),
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, bymonth=1, bymonthday=17),
    rrule.rrule(rrule.YEARLY, dtstart=start, count=1, byeaster=1),
  ]

hdays = get_schedule_holidays_rrules()
holidays = []
for holiday in hdays:
  holidays += list(holiday)

holidays[-1] = holidays[-1] - relativedelta(days=3)

for holiday in holidays:
  print(holiday)

all_days = rrule.rrule(rrule.DAILY, dtstart=start, count=1)
print(len(list(all_days)))
# while start != datetime(2023, 1, 1):
#   if start in h and h.get(start) == []