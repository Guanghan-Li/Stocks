import holidays
from datetime import datetime
from dateutil.easter import *

print(easter(2022))

h = holidays.US()
print(h.get("2022-04-15"))
print("04-15-2022" in h)

# for hd in holidays(years=2022).items():
#   print(hd)