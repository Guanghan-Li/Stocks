import holidays

h = holidays.US()
print(h.get("07-05-2022"))
print("07-05-2022" in h)