import datetime

string = 'Утре / 18:00'.split('/')

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

date = datetime.datetime.strptime(str(tomorrow) + string[1], '%Y-%m-%d %H:%M')

print(date)