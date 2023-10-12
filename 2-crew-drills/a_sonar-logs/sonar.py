import pytz # need 2020.4
from datetime import datetime

input_txt = open("input.txt", "r")
lines = input_txt.readlines()

def process_line(line):
    parts = line.split(' ')
    (date, time, tz) = parts[:3]
    char = chr(int(parts[-1][1:-2], 16))

    fmt = "%Y-%m-%d %H:%M:%S"
    local_time = datetime.strptime(f"{date} {time}", fmt)
    local_tz = pytz.timezone(tz)

    loc_dt = local_tz.localize(local_time)

    utctime = loc_dt.astimezone(pytz.utc)
    return (utctime, char)

print(''.join(map(lambda x: x[1], sorted([process_line(line) for line in lines]))))
