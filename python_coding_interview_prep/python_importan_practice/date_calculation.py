from datetime import date, time, datetime, timedelta

from mpmath.calculus.differentiation import difference

today = date.today()
print(f"Todays date is {today}")

current_time = time(15, 5, 23)
print(f"Current time is {current_time}")

now = datetime.now()
print(f"Current date and time is {now}")

specific_dt = datetime(2025, 4, 5, 15, 5, 23)
print(f"Specific date and time is {specific_dt}")

dt1 = datetime(2025, 4, 5, 15, 5, 23)
dt2 = datetime(2024, 6, 5, 15, 5, 23)
diff =  dt1 - dt2
print(f"Difference between {dt1} and {dt2} is {diff}")

one_week_later = dt1 + timedelta(weeks=1)
print(f"One week later: {one_week_later}")




