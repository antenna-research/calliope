from grammar import *

ligatureRules = [
	[{
		'span': [0.5, 1.0, 1.5],
		'gait': ['double'],
		'foot': [[0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2]],
		'sync': [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [0.5, 1.5],
		'gait': ['double'],
		'foot': [[0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2]],
		'sync': [[0], [0], [0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [0.5, 1.5],
		'gait': ['double'],
		'foot': [[0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2]],
		'sync': [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [0.5, 1.5],
		'gait': ['double'],
		'foot': [[0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0, 1/2], [0], [0]],
		'sync': [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1/2], [1/2]],
	}],
	[{
		'span': [0.5, 1.5],
		'gait': ['double'],
		'foot': [[-1/2, 0], [-1/2, 0], [-1/2, 0], [-1/2, 0], [-1/2, 0], [-1/2, 0], [-1/2, 0], [-1/2, 0]],
		'sync': [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [0.5, 1.0],
		'gait': ['double'],
		'foot': [[-1/2, 0], [-1/2, 0], [-1/2, 0], [-1/2, 0]],
		'sync': [[0], [0], [0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [0.5, 1.0],
		'gait': ['double'],
		'foot': [[-1/2, 0], [-1/2, 0], [-1/2, 0], [0, 1/2], [0, 1/2]],
		'sync': [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [0.5, 1.0],
		'gait': ['double'],
		'foot': [[-1/2, 0], [-1/2, 0], [-1/2, 0], [-1/2, 0]],
		'sync': [[0], [0], [0], [0], [0], [0], [0], [0]],
	}],
	[{
		'span': [2.0, 3.0],
		'gait': ['double'],
		'foot': [[0],[0]],
		'sync': [[0,1/2],[0,1/2]],
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
	{
	'range': [1,2,3],
	'figure': ['saddleUp','spikeUp'],
	'direction': [-7],
	},
	{
	'range': [1,2,3],
	'figure': ['saddleDown','spikeDown'],
	'direction': [5],
	},
	{
	'range': [2,3],
	'figure': ['rampUp','accUp','decUp'],
	'direction': [-7],
	},
	{
	'range': [2,3],
	'figure': ['rampDown','accDown','decDown'],
	'direction': [5],
	},
	{
	'range': [1,3,4,7,11,18],
	'figure': ['sawtooth2Up','sawtooth2Down','sawtooth3Up','sawtooth3Down','zigZagUp','zigZagDown'],
	'direction': [-1],
	},
]

anticipationRules = [
	['transposition', 'ligature'],
	['address', 'direction'],
	['range', 'figure'],
	['figure', 'address'],
	['direction', 'transposition'],
	['ligature'],
]
	
	
	
	
	
prolongationRules = [
	['transposition', 'ligature'],
	['address', 'transposition'],
	['range', 'figure'],
	['figure', 'range'],
	['direction', 'direction'],
	['ligature', 'address'],
	['direction', 'ligature'],
	['transposition', 'figure'],
	['figure', 'direction'],
	['ligature', 'transposition'],
	['address', 'address'],
	['ligature'],
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
