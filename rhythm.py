from utils import *
from math import ceil, floor

refractions = { # 1     2      3      4      5      6      7      8       9      10      11     12      13     14      15      16      17
	'double':	[(0,1),(1,16),(1,8), (3,16),(1,4), (5,16),(3,8), (7,16), (1,2), (9,16), (5,8), (11,16),(3,4), (13,16),(7,8),  (15,16),(1,1)],
	'trip_ls':	[(0,1),(1,12),(1,6), (1,4), (1,3), (5,12),(1,2), (7,12), (2,3), (17,24),(3,4), (19,24),(5,6), (7,8),  (11,12),(23,24),(1,1)],
	'quint_ls':	[(0,1),(1,10),(2,10),(3,10),(4,10),(9,20),(1,2), (11,20),(3,5),(13,20),(7,10), (3,4),  (4,5), (17,20),(9,10), (19,20),(1,1)],
	'trip_ll':	[(0,1),(1,12),(1,6), (1,4), (1,3), (5,12),(1,2), (7,12), (2,3), (3,4),  (5,6), (11,12),(1,1), (13,12),(7,6),  (5,4),  (4,3)],
	'quint_ll':	[(0,1),(1,10),(2,10),(3,10),(4,10),(1,2), (3,5), (7,10), (4,5), (9,10), (1,1), (11,10),(6,5), (13,10),(7,5),  (15,10),(8,5)],
	'trip_sl':	[(0,1),(1,24),(1,12),(1,8), (1,6), (5,24),(1,4), (7,24), (1,3), (5,12), (1,2), (7,12), (2,3), (3,4),  (5,6),  (11,12),(1,1)],
	'quint_sl':	[(0,1),(1,20),(1,10),(3,20),(2,10),(1,4), (3,10),(7,20), (4,10),(9,20), (1,2), (11,20),(3,5), (7,10), (4,5),  (9,10), (1,1)],
	'trip_ss':	[(0,1),(1,24),(1,12),(1,8), (1,6), (5,24),(1,4), (7,24), (1,3), (3,8),  (5,12),(11,24),(1,2), (13,24),(7,12), (5,8),  (2,3)],
	'quint_ss':	[(0,1),(1,20),(1,10),(3,20),(2,10),(1,4), (3,10),(7,20), (4,10),(9,20), (1,2), (11,20),(3,5), (13,20),(7,10), (3,4),  (4,5)],
	'qt2_ls':   [(0,1),(1,10),(2,10),(1,4), (3,10),(7,20),(4,10),(9,20), (1,2), (3,5),  (7,10),(3,4),  (4,5), (17,20),(9,10), (19,20),(1,1)],
	'qt2_sl':   [(0,1),(1,20),(1,10),(3,20),(2,10),(1,4), (3,10),(4,10), (1,2), (11,20),(3,5), (13,20),(7,10),(3,4),  (4,5),  (9,10), (1,1)],
	'tp2_ls':	[(0,1),(1,12),(1,6), (1,4), (1,3), (3,8), (5,12),(11,24),(1,2), (7,12), (2,3), (3,4),  (5,6), (7,8),  (11,12),(23,24),(1,1)],
	'tp2_sl':	[(0,1),(1,24),(1,12),(1,8), (1,6), (1,4), (1,3), (5,12), (1,2), (13,24),(7,12),(5,8),  (2,3), (3,4),  (5,6),  (11,12),(1,1)],
}

points = [0.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]


metric_distances = {
	'double': [(0,1), (1,2), (1,4), (1,8), (1,16)],
	'trip_ls': [(0,1), (2,3), (1,3), (1,6), (1,12)],
	'quint_ls': [(0,1), (3,5), (4,10), (2,10), (1,10)],
	'trip_ll': [(0,1), (2,3), (1,3), (1,6), (1,12)],
	'quint_ll': [(0,1), (4,5), (4,10), (2,10), (1,10)],
	'trip_sl': [(0,1), (1,3), (1,6), (1,12), (1,24)],
	'quint_sl': [(0,1), (4,10), (2,10), (1,10), (1,20)],
	'trip_ss': [(0,1), (1,3), (1,6), (1,12), (1,24)],
	'quint_ss': [(0,1), (4,10), (2,10), (1,10), (1,20)],
	'qt2_ls': [(0,1), (1,2), (3,10), (2,10), (1,10)],
	'qt2_sl': [(0,1), (1,2), (2,10), (1,10), (1,20)],
	'tp2_ls': [(0,1), (1,2), (1,3), (1,6), (1,12)],
	'tp2_sl': [(0,1), (1,2), (1,6), (1,12), (1,24)],
}


def getOffsets(foot):
	""" calculate offsets for syncopated, refracted, scaled foot """
	syncedOffsets = syncOffsets(foot)
	finalOffsets = []
	for syncedOffset in syncedOffsets:
		finalOffset = getFinalOffset(syncedOffset, foot['gait'], foot['span'])
		finalOffsets.append(finalOffset)
	return finalOffsets


def syncOffsets(foot):
	""" syncopate logical offsets, desyncopate axis if crowded """
	syncedOffsets = []
	for i, offset in enumerate(foot['foot']):
		j = i%(len(foot['sync'])) # sync index wraps around
		if offset == 0:
			syncBasis = 1.0
		else:
			syncBasis = abs(offset)
		syncedOffset = offset + (syncBasis*foot['sync'][j])
		syncedOffsets.append(syncedOffset)
	# desyncopate axis if crowded in
	axisIndex = foot['foot'].index(0)
	beforeAxis = syncedOffsets[0:axisIndex]
	afterAxis = syncedOffsets[(axisIndex+1):len(syncedOffsets)]
	for offset in beforeAxis:
		if offset >= syncedOffsets[axisIndex]:
			syncedOffsets[axisIndex] = 0.0
	for offset in afterAxis:
		if offset <= syncedOffsets[axisIndex]:
			syncedOffsets[axisIndex] = 0.0
	syncedOffsets = resolveCollisions(syncedOffsets)
	return syncedOffsets


def resolveCollisions(syncedOffsets):
	# for now remove one - note lexeme object will reflect incorrect number of notes
	return sorted(list(set(syncedOffsets)))

	# because this breaks it
	# while len(syncedOffsets) != len(set(syncedOffsets)):
	# 	neighborPairs = [ (x,y) for x, y in zip(syncedOffsets[:-1], syncedOffsets[1:]) ]
	# 	removeIndices = []
	# 	for i, pair in enumerate(neighborPairs):
	# 		if pair[0] == pair[1]:
	# 			if pair[0] > 0:				
	# 				if syncedOffsets[i+1] == ceil((syncedOffsets[i+1]*2)) / 2:
	# 					syncedOffsets[i+1] += 0.5
	# 				else:
	# 					syncedOffsets[i+1] = fl(ceil((syncedOffsets[i+1]*2)) / 2)
	# 			if pair[0] < 0:
	# 				if syncedOffsets[i] == floor((syncedOffsets[i]*2)) / 2:
	# 					syncedOffsets[i] -= 0.5
	# 				else:
	# 					syncedOffsets[i] = fl(floor((syncedOffsets[i]*2)) / 2)
	# return syncedOffsets


def getFinalOffset(offset, refraction, scale):
	""" calculate refracted, scaled offset from 'logical' duple offset """
	if offset < 0:
		working_offset = -offset
	else:
		working_offset = offset
	offset_index = [x/16 for x in range(0,17)].index(working_offset)
	final = refractions[refraction][offset_index]

	if offset < 0:
		scale *= -1
	return fl((final[0]*scale)/(final[1]), 6)


# [0.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]

'''

Number line: -0.5 <—0—> +0.5
level	-1		-2			-3			0			3			2			1			
ratio	-0.5	-0.25		-0.125		0.0			+0.125		+0.25		+0.5		
1/4		8th		16th		32nd					32nd		16th		8th		
4/4		half	quarter		eighth					eighth		quarter		half


refraction table key

index		0			6			5			4			3			2			1
duple		0.0			0.015625	0.03125		0.0625		0.125		.25			0.5
quint_ls	0.0			0.025		0.05		0.1			0.2			0.4			0.6
quint_sl	0.0			0.0125		0.025		0.05		0.1			0.2			0.4
quint_half	0.0			0.025		0.05		0.1			0.2			0.3			0.5
trip_ls		0.0			0.02083		0.0416		0.083		0.166		0.33		0.66
trip_sl		0.0			0.010416	0.02083		0.0416		0.083		0.166		0.33
trip_half	0.0			0.02083		0.0416		0.083		0.166		0.33		0.5


refraction table - through level 4 (= 16th notes for duple measure level object)

duple		quint_ls	quint_sl	trip_ls		trip_sl		trip_ll		trip_ss		quint_ll	quint_ss	quint2_ls	quint2_sl	trip2_ls	trip2_sl
0.0			0.0			0.0			0.0			0.0			0.0 		0.0			0.0			0.0			0.0			0.0			0.0			0.0		
0.0625		0.1			0.05		0.08333		0.04167		0.08333		0.04167		0.1			0.05		0.1			0.05		0.08333		0.04167	
0.125		0.2			0.1			0.16667		0.08333		0.16667		0.08333		0.2			0.1			0.2			0.1			0.16667		0.08333	
0.1875		0.3			0.15		0.25		0.125		0.25		0.125		0.3			0.15		0.25		0.15		0.25		0.125	
0.25		0.4			0.2			0.33333		0.16667		0.33333		0.16667		0.4			0.2			0.3			0.2			0.33333		0.16667	
0.3125		0.45		0.25		0.41667		0.20833		0.41667		0.20833		0.5			0.25		0.35		0.25		0.375		0.25	
0.375		0.5			0.3			0.5			0.25		0.5			0.25		0.6			0.30		0.4			0.3			0.41667		0.33333	
0.4375		0.55		0.35		0.58333		0.29167		0.58333		0.29167		0.7			0.35		0.45		0.4			0.45833		0.41667	
0.5			0.6			0.4			0.66667		0.33333		0.66667		0.33333		0.8			0.4			0.5			0.5			0.5			0.5		
0.5625		0.65		0.45		0.70833		0.41667		0.75		0.375		0.9			0.45		0.6			0.55		0.58333		0.54167	
0.625		0.7			0.5			0.75		0.5			0.83333		0.41667		1.0			0.5			0.7			0.6			0.66667		0.58333	
0.6875		0.75		0.55		0.79167		0.58333		0.91667		0.45833		1.1			0.55		0.75		0.65		0.75		0.625	
0.75		0.8			0.6			0.83333		0.66667		1.0			0.5			1.2			0.60		0.8			0.7			0.83333		0.66667	
0.8125		0.85		0.7			0.875 		0.75		1.08333		0.54167		1.3			0.65		0.85		0.75		0.875		0.75	
0.875		0.9			0.8			0.91667		0.83333		1.16667		0.58333		1.4			0.70		0.9			0.8			0.91667		0.83333	
0.9375		0.95		0.9			0.95833		0.91667		1.25		0.625		1.5			0.75		0.95		0.9			0.95833		0.91667	


'''
