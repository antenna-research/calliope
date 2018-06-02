from phonology import *
from diagram import *


'''
modules:

cadence.py		define musical morphemes
diagram.py		define binary tree structures
phonology.py	distribution of cadential features for given lexicon
lexicon.py		repository of lexemes w/ weighted dependency correlations
passage.py		cadences from lexicon mapped to tree diagram
	spellout()	sequence of unified cadences in passage (for each voice)
score.py 		list of n passages rendered to music21 score object
	export()	to xml, midi, ly

'''

phonology = Phonology()

phonology.addFootprintRule([{
	'span': [2],
	'gait': ['double','triple'],
	'foot': [[-1/2, 0, 1/2]],
	'step': [[0, 1/2], [0, 1/2], [0, 1/2]],
}])

phonology.addFunctionRule({
	'address': ['A1','B1'],
	'transposition': [-1,0,1],
})

phonology.addPathRule({
	'range': [2,3,4],
	'figure': ['rampUp', 'rampDown'],
	'tilt': ['float', 'dive'],
})

lex = phonology.makeCadence()
lex.print()

syntax = Diagram()
syntax.print()

