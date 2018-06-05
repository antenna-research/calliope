from utils import *

refractions = { # 1     2      3      4      5      6      7      8       9      10      11     12      13     14      15      16      17
	'double':	[(0,1),(1,16),(1,8), (3,16),(1,4), (5,16),(3,8), (7,16), (1,2), (9,16), (5,8), (11,16),(3,4), (13,16),(7,8),  (15,16),(1,1)],
	'trp_ls':	[(0,1),(1,12),(1,6), (1,4), (1,3), (5,12),(1,2), (7,12), (2,3), (17,24),(3,4), (19,24),(5,6), (7,8),  (11,12),(23,24),(1,1)],
	'qnt_ls':	[(0,1),(1,10),(2,10),(3,10),(4,10),(9,20),(1,2), (11,20),(3,5),(13,20),(7,10), (3,4),  (4,5), (17,20),(9,10), (19,20),(1,1)],
	'trp_ll':	[(0,1),(1,12),(1,6), (1,4), (1,3), (5,12),(1,2), (7,12), (2,3), (3,4),  (5,6), (11,12),(1,1), (13,12),(7,6),  (5,4),  (4,3)],
	'qnt_ll':	[(0,1),(1,10),(2,10),(3,10),(4,10),(1,2), (3,5), (7,10), (4,5), (9,10), (1,1), (11,10),(6,5), (13,10),(7,5),  (15,10),(8,5)],
	'trp_sl':	[(0,1),(1,24),(1,12),(1,8), (1,6), (5,24),(1,4), (7,24), (1,3), (5,12), (1,2), (7,12), (2,3), (3,4),  (5,6),  (11,12),(1,1)],
	'qnt_sl':	[(0,1),(1,20),(1,10),(3,20),(2,10),(1,4), (3,10),(7,20), (4,10),(9,20), (1,2), (11,20),(3,5), (7,10), (4,5),  (9,10), (1,1)],
	'trp_ss':	[(0,1),(1,24),(1,12),(1,8), (1,6), (5,24),(1,4), (7,24), (1,3), (3,8),  (5,12),(11,24),(1,2), (13,24),(7,12), (5,8),  (2,3)],
	'qnt_ss':	[(0,1),(1,20),(1,10),(3,20),(2,10),(1,4), (3,10),(7,20), (4,10),(9,20), (1,2), (11,20),(3,5), (13,20),(7,10), (3,4),  (4,5)],
	'qt2_ls':   [(0,1),(1,10),(2,10),(1,4), (3,10),(7,20),(4,10),(9,20), (1,2), (3,5),  (7,10),(3,4),  (4,5), (17,20),(9,10), (19,20),(1,1)],
	'qt2_sl':   [(0,1),(1,20),(1,10),(3,20),(2,10),(1,4), (3,10),(4,10), (1,2), (11,20),(3,5), (13,20),(7,10),(3,4),  (4,5),  (9,10), (1,1)],
	'tp2_ls':	[(0,1),(1,12),(1,6), (1,4), (1,3), (3,8), (5,12),(11,24),(1,2), (7,12), (2,3), (3,4),  (5,6), (7,8),  (11,12),(23,24),(1,1)],
	'tp2_sl':	[(0,1),(1,24),(1,12),(1,8), (1,6), (1,4), (1,3), (5,12), (1,2), (13,24),(7,12),(5,8),  (2,3), (3,4),  (5,6),  (11,12),(1,1)],
}

points = [0.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]


metric_distances = {
	'double': [(0,1), (1,2), (1,4), (1,8), (1,16)],
	'trp_ls': [(0,1), (2,3), (1,3), (1,6), (1,12)],
	'qnt_ls': [(0,1), (3,5), (4,10), (2,10), (1,10)],
	'trp_ll': [(0,1), (2,3), (1,3), (1,6), (1,12)],
	'qnt_ll': [(0,1), (4,5), (4,10), (2,10), (1,10)],
	'trp_sl': [(0,1), (1,3), (1,6), (1,12), (1,24)],
	'qnt_sl': [(0,1), (4,10), (2,10), (1,10), (1,20)],
	'trp_ss': [(0,1), (1,3), (1,6), (1,12), (1,24)],
	'qnt_ss': [(0,1), (4,10), (2,10), (1,10), (1,20)],
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
		j = i%(len(foot['sync'])) # sync index
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
	return syncedOffsets


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