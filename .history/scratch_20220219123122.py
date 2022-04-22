import holidays
from datetime import datetime

h = holidays.US()
print(h.get("2022-06-19"))
print("06-19-2022" in h)

