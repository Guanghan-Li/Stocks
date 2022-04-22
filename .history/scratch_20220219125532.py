import holidays
from datetime import datetime
from dateutil.easter import *
from dateutil.relativedelta import relativedelta

good_friday = easter(2022) - relativedelta(days=2)

h = holidays.US()
print(h.get("2022-04-15"))
print("04-15-2022" in h)

# for hd in holidays(years=2022).items():
#   print(hd)

holiday_names = [
  "N"
]

start = datetime(2022, 1, 1)
dates = []

hdays = []

hdays.append(h.get_named("Martin Luther King Jr. Day"))
hdays.append(h.get_named("Juneteenth National Independence Day"))
hdays.append(h.get_named("Washington's Birthday"))
hdays.append(h.get_named("Independence Day"))
hdays(h.get_named("Labor Day"))
hdays(h.get_named("Thanksgiving"))
hdays.append(h.get_named("Christmas Day"))

print(hdays)

# while start != datetime(2023, 1, 1):
#   if start in h and h.get(start) == []