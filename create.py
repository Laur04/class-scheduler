import requests
from datetime import datetime, timedelta, date
import os
import subprocess

link_file = open("class-links.txt", "r+")
links = link_file.readlines()
if len(links) != 9:
    links = [
        input("Collab link for homeroom?"),
        input("Collab link for 1st period?"),
        input("Collab link for 2nd period?"),
        input("Collab link for 3rd period?"),
        input("Collab link for 4th period?"),
        input("Collab link for 5th period?"),
        input("Collab link for 6th period?"),
        input("Collab link for 7th period?"),
        "https://ion.tjhsst.edu"
    ]
    link_file.seek(0)
    for l in links:
        link_file.write(l + "\n")
    link_file.truncate()
    link_file.close()
    
open_command = 'xdg-open'

day = date.today()
dates = []
for i in range(30):
    dates.append(day)
    day += timedelta(days=1)

times = [[], [], [], [], [], [], [], [], []]
for d in dates:
    resp = requests.get("https://ion.tjhsst.edu/api/schedule/{}".format(str(d))).json()
    for block in resp["day_type"]["blocks"]:
        day_index = None
        if "1" in block["name"]:
            day_index = 1
        elif "2" in block["name"]:
            day_index = 2
        elif "3" in block["name"]:
            day_index = 3
        elif "4" in block["name"]:
            day_index = 4
        elif "5" in block["name"]:
            day_index = 5
        elif "6" in block["name"]:
            day_index = 6
        elif "7" in block["name"]:
            day_index = 7
        elif "8" in block["name"]:
            day_index = 8
        elif "Homeroom" in block["name"]:
            day_index = 0

        if day_index is not None:
            temp_time = block["start"].split(":")
            hour = int(temp_time[0])
            minute = int(temp_time[1])
            times[day_index].append(datetime(d.year, d.month, d.day, hour, minute) - timedelta(minutes=5))

for i, time in enumerate(times):
    for t in times[i]:
        at_cmd = "at {}:{} {}-{}-{}".format(t.hour, t.minute, t.year, t.month, t.day)
        open_cmd = "env DISPLAY=:0 {} {}".format(open_command, links[i])
        os.system("echo '{}' | {}".format(open_cmd, at_cmd))
