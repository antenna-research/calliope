from phonology import *
from diagram import *


'''
modules:

cadence.py		define musical morphemes
projection.py	dependencies and agreement
				antecedent or consequent cadence bundled with prolongation rules for each feature - (dominates) or (dominates, agrees) or (dominates, agrees, submits)
				(1)==Head; (0)==Complement; (1,0)==XP; (1,1)==XBar; (0,1)==X; (0,0)==None; 

diagram.py		define binary tree structures
phonology.py	distribution of cadential features for given grammar
lexicon.py		repository of lexemes: (cadence, dependencies, prolongation)
passage.py		lexemes unified over tree diagram
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

morphology = Morphology()
morphology.addAnticipationRule(['footprint'])
morphology.addAnticipationRule(['tilt'])
morphology.addAnticipationRule([])
morphology.addProlongationRule(['address','transposition'])
morphology.addProlongationRule(['address'])
morphology.addProlongationRule(['figure','range'])
morphology.addProlongationRule(['range'])
morphology.addProlongationRule(['range','tilt'])



# lexicon.addCategory()

phonology.print()
morphology.print()

lexeme = phonology.makeCadence(label=1)
lexeme.print()

syntax = Diagram()
syntax.print()

