from grammar import *

footprintRules = [
	[{
		'span': [2],
		'gait': ['double','triple'],
		'foot': [[-1/2, 0, 1/2]],
		'step': [[0, 1/2], [0, 1/2], [0, 1/2]],
	}],
]

functionRules = [
	{
	'address': ['A1','B1'],
	'transposition': [-1,0,1],
	},
]

pathRules = [
	{
	'range': [2,3,4],
	'figure': ['rampUp', 'rampDown'],
	'tilt': ['float', 'dive'],
	},
]

anticipationRules = [
	['footprint'],
	['tilt'],
	[],
]

prolongationRules = [
	['address','transposition'],
	['address'],
	['figure','range'],
	['range'],
	['range','tilt'],
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
