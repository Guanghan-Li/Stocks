import holidays

h = holidays.US()
print(h.get("06-19-2022"))
print("06-19-2022" in h)