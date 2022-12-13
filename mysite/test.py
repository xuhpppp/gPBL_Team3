from datetime import datetime

def check_time_in_range(start, end, x):
    start = datetime.strptime(start[:-6], '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end[:-6], '%Y-%m-%d %H:%M:%S')
    x = datetime.strptime(x[:-6], '%Y-%m-%d %H:%M:%S')

    return start <= x <= end


print(check_time_in_range('2022-12-12 11:00:00+00:00', '2022-12-12 16:00:00+00:00', '2022-12-12 17:00:00+00:00'))