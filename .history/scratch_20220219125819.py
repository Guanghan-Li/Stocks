import holidays
from datetime import datetime
from dateutil.easter import *
from dateutil.relativedelta import relativedelta

start = datetime(2022, 1, 1)
dates = []

hdays = []
year = 2022
h = holidays.US(years=year)
good_friday = easter(2022) - relativedelta(days=2)
hdays.append(good_friday)
hdays.append(h.get_named("Martin Luther King Jr. Day"))
hdays.append(h.get_named("Juneteenth National Independence Day"))
hdays.append(h.get_named("Washington's Birthday"))
hdays.append(h.get_named("Independence Day"))
hdays.append(h.get_named("Labor Day"))
hdays.append(h.get_named("Thanksgiving"))
hdays.append(h.get_named("Christmas Day"))
hdays.append(datetime(year, 1, 1))

print(hdays)

# while start != datetime(2023, 1, 1):
#   if start in h and h.get(start) == []