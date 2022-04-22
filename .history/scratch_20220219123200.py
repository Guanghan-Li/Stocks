import holidays
from datetime import datetime

h = holidays.US()
print(h.get("2022-01-17"))
print("01-17-2022" in h)

