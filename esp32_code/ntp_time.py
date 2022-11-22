import ntptime

#ntptime.host = "a.st1.ntp.br"

time_delta = 946684800

ntptime.settime()
def get_ntp_time():
    try:
        return ntptime.time() + time_delta
    except:
        print("Error syncing time")
