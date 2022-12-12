from datetime import datetime

def check_time_in_range(start, end, x):
    start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S+%z')
    end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S+%z')
    x = datetime.strptime(x, '%Y-%m-%d %H:%M:%S+%z')

    return start <= x <= end


print(check_time_in_range('2022-12-12 11:00:00+00:00', '2022-12-12 16:00:00+00:00', '2022-12-12 12:00:00+00:00'))