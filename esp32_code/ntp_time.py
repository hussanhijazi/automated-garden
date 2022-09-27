import ntptime

# ntptime.host = "a.st1.ntp.br"

time_delta = 946684800


def get_ntp_time():
    try:
        ntptime.settime()
        return ntptime.time() + time_delta
    except:
        print("Error syncing time")
