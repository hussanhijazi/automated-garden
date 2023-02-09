import datetime

def check_time(time):
    now = datetime.datetime.now().time()

    date_time = datetime.datetime.combine(datetime.date.today(), time)
    date_time_now = datetime.datetime.combine(datetime.date.today(), now)

    seconds = (date_time - date_time_now).total_seconds() / 60

    return seconds
