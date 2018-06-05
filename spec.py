from grammar import *

footprintRules = [
	[{
		'span': [2],
		'gait': ['double'],
		'foot': [[-1/2, 0, 1/2]],
		'sync': [[0, 1/2], [0, 1/2], [0, 1/2]],
	}],
	[{
		'span': [1],
		'gait': ['trp_ls'],
		'foot': [[-1/2, 0, 1/2]],
		'sync': [[0], [0], [0]],
	}],
	[{
		'span': [2],
		'gait': ['double'],
		'foot': [[-1/2, -1/4, 0, 1/2]],
		'sync': [[0, 1/4], [0, 1/4], [0, 1/4], [0, 1/4]],
	}],
	[{
		'span': [1],
		'gait': ['trp_sl'],
		'foot': [[-1/2, -1/4, 0, 1/4]],
		'sync': [[0], [0], [0], [0]],
	}],
	[{
		'span': [1],
		'gait': ['double'],
		'foot': [[-1/2, -1/4, 0, 1/2]],
		'sync': [[0], [0], [0], [0]],
	}],
	[{
		'span': [2],
		'gait': ['trp_ll'],
		'foot': [[-1/2, -1/4, 0, 1/4]],
		'sync': [[0, 1/4], [0, 1/4], [0, 1/4], [0, 1/4]],
	}],
]

functionRules = [
	{
	'address': ['A1','B1'],
	'transposition': [-1,0],
	},
	{
	'address': ['C1','D1'],
	'transposition': [0,1],
	},
	# {
	# 'address': ['D2','C2'],
	# 'transposition': [0,1],
	# },
	# {
	# 'address': ['E1','E2'],
	# 'transposition': [0,1],
	# },
]

pathRules = [
	{
	'range': [2,3,4],
	'figure': ['rampUp', 'rampDown'],
	'tilt': ['float', 'dive'],
	},
	{
	'range': [5,6,7],
	'figure': ['stepUp', 'stepDown'],
	'tilt': ['rise', 'fall'],
	},
]

anticipationRules = [
	# ['footprint'],
	# ['footprint','tilt'],
	# ['footprint','figure'],
	[],
	['tilt'],
	['figure'],
]

prolongationRules = [
	['address','figure','range'],
	['address','figure'],
	['address','range'],
	['address'],
	['figure','range'],
	['figure'],
	['range'],
]

# assemble grammar object
phonology = Phonology()
for rule in footprintRules:
	phonology.addFootprintRule(rule)
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
