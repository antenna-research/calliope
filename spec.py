from grammar import *

ligatureRules = [
	# [{
	# 	'span': [2.0],
	# 	'gait': ['double'],
	# 	'foot': [[0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2]],
	# 	'sync': [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]],
	# }],
	# [{
	# 	'span': [3.0, 5.0, 6.0],
	# 	'gait': ['trip_sl', 'trip_ls', 'double'],
	# 	'foot': [[0, 1/2], [0]],
	# 	'sync': [[0]],
	# }],
	[{
		'span': [3.0, 5.0],
		'gait': ['double','trip_sl'],
		'foot': [[0]],
		'sync': [[0]],
	}],
	[{
		'span': [0.5, 1.0],
		'gait': ['double','trip_sl'],
		'foot': [[-1/2, 0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2]],
		'sync': [[0]],
	}],
	[{
		'span': [0.5, 1.0],
		'gait': ['double','trip_sl'],
		'foot': [[-1/2, 0, 1/2], [0, 1/2]],
		'sync': [[0]],
	}],
	[{
		'span': [0.5, 1.0],
		'gait': ['double','trip_sl'],
		'foot': [[-1/2, 0, 1/2], [0, 1/2], [0, 1/2]],
		'sync': [[0]],
	}],
]

functionRules = [
	{
	'address': ['A1','B1'],
	'transposition': [0],
	},
	{
	'address': ['C1','D1'],
	'transposition': [0],
	},
	{
	'address': ['D2','C2'],
	'transposition': [0],
	},
	{
	'address': ['E1','E2'],
	'transposition': [0],
	},
]

#
# ['flat']
# ['rampDown','accDown','decDown','sawtooth1Down','sawtooth2Down','sawtooth3Down']
# ['rampUp','accUp','decUp','sawtooth1Up','sawtooth2Up','sawtooth3Up']
# ['triangleUp','saddleUp','spikeUp','zigZagUp']
# ['triangleDown','saddleDown','spikeDown','zigZagDown']
#

pathRules = [
	# {
	# 'range': [1,2,3],
	# 'figure': ['saddleDown','spikeDown'],
	# 'direction': [5],
	# },
	{
	'range': [5,6,7],
	'figure': ['decDown','decUp'],
	'direction': [0,1,2],
	},
	{
	'range': [1,2,3],
	'figure': ['sawtooth1Up','sawtooth2Up','sawtooth3Up','sawtooth1Down','sawtooth2Down','sawtooth3Down'],
	'direction': [0,1],
	},
	{
	'range': [1,2,4,5],
	'figure': ['zigZagUp','zigZagDown'],
	'direction': [0,1],
	},
]


anticipationRules = [
	# ['transposition', 'ligature'],
	['address','address'],
	['transposition', 'ligature'],
	['transposition', 'span'],
	['gait','transposition'],
	['figure'],
]
	
	
prolongationRules = [
	['transposition', 'transposition'],
	['gait', 'gait'],
	['gait', 'ligature'],
	['transposition', 'span'],
	['sync'],
	# ['ligature', 'address'],
	# ['direction', 'ligature'],
	# ['transposition', 'figure'],
	# ['figure', 'figure'],
	# ['ligature', 'transposition'],
	# ['figure'],
]

# as patient - (yield, check, ask) # ([default] adopt given features, refuse given features, request features
# as agent -   (let, put, drive) # ([default] feature not shared, feature shared with immediately below, feature shared with all below
# probe - goal

'''
# need something like
projectionRules = {
	# produces less uniformity
	'check': [],
	# produces local uniformity (inflection)
	'anticipate': [],
	'prolong': [],
	# produces global uniformity
	'project': [],
	'inject': [],
}
'''

# assemble grammar object
phonology = Phonology()
for rule in ligatureRules:
	phonology.addligatureRule(rule)
for rule in functionRules:
	phonology.addFunctionRule(rule)
for rule in pathRules:
	phonology.addPathRule(rule)

morphology = Morphology()
for rule in anticipationRules:
	morphology.addAnticipationRule(rule)
for rule in prolongationRules:
	morphology.addProlongationRule(rule)

g = Grammar()
g.phonology = phonology
g.morphology = morphology
