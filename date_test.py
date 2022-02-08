from datetime import datetime, timedelta

a = '2020-12-12'
dt = datetime.strptime(a, '%Y-%m-%d')
result = dt + timedelta(days=20)
print(result.strftime('%Y-%m-%d'))
