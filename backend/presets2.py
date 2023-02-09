import firebase
import firebase as my_firebase
import datetime

c = my_firebase.connect()
a = my_firebase.get_presets(c)
print(a)
start = a[0]["time2"]

parts = start.split(":")
time = datetime.time(int(parts[0]), int(parts[1]), int(parts[2]))
print(time)
print(datetime.datetime.now().time())
# print(time - datetime.datetime.now().time())
dateTimeA = datetime.datetime.combine(datetime.date.today(), time)
dateTimeB = datetime.datetime.combine(datetime.date.today(), datetime.datetime.now().time())
# Get the difference between datetimes (as timedelta)
dateTimeDifference = dateTimeA - dateTimeB
# Divide difference in seconds by number of seconds in hour (3600)
dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 60
print(dateTimeDifferenceInHours)
#minutes_diff = (time - datetime.datetime.now().time())
#print(minutes_diff)
