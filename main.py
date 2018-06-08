from grammar import *
from lexicon import *
from passage import *
from render import *
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
render.py 		list of n passages rendered to music21 score object
	export()	to xml, midi, ly'

'''

# lexicon.addCategory()

# g.phonology.print()
# g.morphology.print()

lexicon = Lexicon()
lexicon.populate(g, 8)

lexicon.print()
print("\n-----------\n-----------\n")

passage = Passage(height=5, size=23)

passage.spellout(lexicon)
passage.print()
# print(passage.bars)
# print(passage.tree)
print()

renderer = Renderer()
renderer.render(passage)


# todo: working with multiple voices at once
# todo: convincing m21 to break durations into tied notes over the tactus
# todo: add discovered lexemes, pairwise dependencies to lexicon pre-population, iteratively...


