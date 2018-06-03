from grammar import *
from lexicon import *
from passage import *
from spec import *

'''
modules:

cadence.py		define musical morphemes
projection.py	dependencies and agreement
				antecedent or consequent cadence bundled with prolongation rules for each feature - (dominates) or (dominates, agrees) or (dominates, agrees, submits)
				(1)==Head; (0)==Complement; (1,0)==XP; (1,1)==XBar; (0,1)==X; (0,0)==None; 

phonology.py	distribution of cadential features for given grammar
lexicon.py		repository of lexemes: (cadence, dependencies, prolongation)
passage.py		lexemes unified over binary tree
	spellout()	sequence of unified cadences in passage (for each voice)
score.py 		list of n passages rendered to music21 score object
	export()	to xml, midi, ly'

'''

# lexicon.addCategory()

g.phonology.print()
g.morphology.print()

lexicon = Lexicon()
lexicon.populate(g, 4)
lexicon.print()

passage = Passage(size=12)
passage.printSyntax()

realization = passage.spellout(lexicon)

pprint(realization)

for lex in realization:
	lex.print()



