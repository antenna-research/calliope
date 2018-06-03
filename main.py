from diagram import *
from grammar import *
from spec import *

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

# lexicon.addCategory()

phonology.print()
morphology.print()

lexeme = phonology.makeCadence()
lexeme.print()

syntax = Diagram()
syntax.print()

