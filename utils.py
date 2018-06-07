
def fl(number, precision=6):
	formatstring = '{:.'+str(precision)+'f}'
	return float(formatstring.format(number))


def depth(myList, counter):
	counter += 1
	depthList = []
	for item in myList:
		if isinstance(item, list):
			depthList.append(depth(item, counter))
		else:
			depthList.append(counter)
	return depthList

def flatten(pool):
	res = []
	for v in pool:
		if isinstance(v, list):
		  res += flatten(v)
		else:
			if isinstance(v, int) or isinstance(v, str) or isinstance(v, float):
				res.append(v)
	return res

def isOversliced(bars):
	targets = [bar > 0 and bar < 2.5 for bar in bars]
	return (True in targets)

def firstNonNegative(lst):
	for x in lst:
		if x >= 0:
			return x
	return 0

def lastNonPositive(lst):
	for x in list(reversed(lst)):
		if x <= 0:
			return x
	return 0