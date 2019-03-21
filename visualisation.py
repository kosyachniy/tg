import time


def timeline(messages):
	times = [i.date.timestamp() for i in messages]

	time_min = min(times)
	month_start = time.strftime('%m.%Y', time.gmtime(time_min))
	month_stop = time.strftime('%m.%Y', time.gmtime(time.time()))

	time_all = {}
	i = month_start
	while True:
		time_all[i] = 0

		if i == month_stop:
			break

		if i[:2] == '12':
			i = '01.{}'.format(int(i[3:])+1)
		elif i[:2] in ('01', '02', '03', '04', '05', '06', '07', '08'):
			i = '0{}.{}'.format(int(i[:2])+1, i[3:])
		else:
			i = '{}.{}'.format(int(i[:2])+1, i[3:])

	for i in times:
		time_all[time.strftime('%m.%Y', time.gmtime(i))] += 1

	return [{'time': i, 'count': time_all[i]} for i in time_all]