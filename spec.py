from grammar import *

ligatureRules = [
	[{
		'span': [1],
		'gait': ['double'],
		'foot': [[-1/2, 0, 1/2], [-1/2, 0, 1/2]],
		'sync': [[0], [0], [-1/2], [0], [0], [-1/2]],
	}],
	[{
		'span': [1],
		'gait': ['double'],
		'foot': [[-1/2, 0, 1/2], [-1/2, 0], [-1/2, 0]],
		'sync': [[0], [0], [0], [0], [0, 1/2], [0], [0, 1/2]],  #
	}],
	[{
		'span': [2],
		'gait': ['quint_ss', 'trip_ss'],
		'foot': [[1/2, 0, 1/2], [-1/2, 0, 1/2]],
		'sync': [[0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [1],
		'gait': ['double'],
		'foot': [[-1/2, 0], [-1/2, 0, 1/2]],
		'sync': [[0, 1/2], [0], [0], [0], [0]],
	}],
	[{
		'span': [1],
		'gait': ['trip_ss'],
		'foot': [[-1/2, 0, 1/2], [-1/2, 0, 1/2]],
		'sync': [[0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [1],
		'gait': ['trip_ss'],
		'foot': [[-1/2, 0, 1/2], [-1/2, 0, 1/2]],
		'sync': [[0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [1],
		'gait': ['quint_ss','trip_ss', 'double'],
		'foot': [[0, 1/2], [0], [0, 1/2]],
		'sync': [[0], [0], [0], [0], [0]],
	}],
	[{
		'span': [1],
		'gait': ['quint_ss','trip_ss', 'double'],
		'foot': [[-1/2, 0], [0], [1/2, 0]],
		'sync': [[0], [0], [0], [0], [0]],
	}],
	[{
		'span': [2,4],
		'gait': ['trip_ss','quint_ss','double'],
		'foot': [[-1/2, 0],[-1/2, 0],[-1/2, 0],[0]],
		'sync': [[0], [0], [0], [0], [0], [0], [-1/2]],
	}],
	[{
		'span': [2,4],
		'gait': ['trip_ss','quint_ss'],
		'foot': [[-1/2, -1/4, 0, 1/2]],
		'sync': [[0], [0], [0], [0]],
	}],
	[{
		'span': [1,4],
		'gait': ['double'],
		'foot': [[-1/2, -1/4, 0, 1/4]],
		'sync': [[0, 1/2], [0], [0], [0]],
	}],
]

functionRules = [
	{
	'address': ['A1','B1'],
	'transposition': [-1,0,1],
	},
	{
	'address': ['C1','D1'],
	'transposition': [-1,0,1],
	},
	{
	'address': ['D2','C2'],
	'transposition': [-1,0,1],
	},
	{
	'address': ['E1','E2'],
	'transposition': [-1,0,1],
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
	{
	'range': [9,10,11],
	'figure': ['saddleUp','spikeUp'],
	'direction': [1],
	},
	{
	'range': [6,7,8],
	'figure': ['saddleDown','spikeDown'],
	'direction': [-1],
	},
	# {
	# 'range': [2,3,4],
	# 'figure': ['rampUp','accUp','decUp'],
	# 'direction': [1],
	# },
	# {
	# 'range': [5,6,7],
	# 'figure': ['rampDown','accDown','decDown'],
	# 'direction': [-1],
	# },
	{
	'range': [2,3,4,10,11,12],
	'figure': ['sawtooth2Up','sawtooth2Down','sawtooth3Up','sawtooth3Down','zigZagUp','zigZagDown'],
	'direction': [0],
	},
]

anticipationRules = [
	['transposition','askldfjds'],
	['address'],
	['direction'],
	[],
]

prolongationRules = [
	['transposition','sdfsdf'],
	['address'],
	['direction'],
	[],
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
