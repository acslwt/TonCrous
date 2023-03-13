import myfitnesspal

client = myfitnesspal.Client()

day = client.get_date(2023, 6, 2)
print(day)