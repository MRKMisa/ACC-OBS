import datetime

while True:
    now = datetime.datetime.now()
    print([*str(now.second)][1])