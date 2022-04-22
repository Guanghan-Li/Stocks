import holidays
from datetime import datetime

h = holidays.US()
print(h.get("2022-04-17=5"))
print("04-1-2022" in h)

for hd in holidays(years=2022).items():
  print(hd)