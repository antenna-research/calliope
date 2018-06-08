from copy import copy
from math import floor
from random import choice
from itertools import chain, accumulate
from math import floor, ceil
from pprint import pprint
from utils import *


'''
To ensure that all intervallic relationships are unit-based, loci must have different ternary *and* quaternary functions simultaneously

ternary functions:						quaternary functions:

C2	E4	C1		o	.	.				C2	E4	C1	A3		o	.	.	*		
A3	D6	E5		*	+	.				D6	E5	D5	B1		+	.	*	.		
D5	B1	C4		*	.	+				C4	E6	C3	A2		+	*	.	.		
E6	C3	A2		*	.	.				D2	E1	D1	B3		#	.	.	*		
D2	E1	D1		#	.	.				C6	E2	C5	A1		+	.	*	.		
B3	C6	E2		*	+	.				D4	E3	D3	B2		+	*	.	.		
C5	A1	D4		*	.	+				
E3	D3	B2		*	.	.				Key: . = unit, * = whole-tone/aug, + = diminished, # = tritone, o = reference 


quaternary reduction:

┌──┬──┬──┬──┐
│C2 E2 C1 A1│
├──┼──┼──┼──┤
│D2 E1 D1 B1│ 
└──┴──┴──┴──┘


'''

loc = {
	'C2': 1, 'E2': 1, 'C1':-1, 'A1': 0, 'D2':-1, 'E1':-1, 'D1': 1, 'B1':0,
}

# pick any three groups - pairs can't be combined / fourth group not unitary
groups = [('C1','D1'),('A1','B1'),('D2','C2'),('E1','E2')]

gen = {
	'A': ['E2','C1','A1','D2','E1','D1','B1','C2'],
	'B': ['E2','D2','B1','C1','E1','C2','A1','D1'],
}

obl = {
	'A': [['E2','C2','E1','D2'],['C1','A1','D1','B1']],
	'B': [['E2','D1','E1','C1'],['C2','A1','D2','B1']]
}

bisections = {
	'A': {'C1': ('C2','E2'), 'A1': ('E2','C1'), 'D2': ('C1','A1'), 'E1': ('A1','D2'),
	      'D1': ('D2','E1'), 'B1': ('E1','D1'), 'C2': ('D1','B1'), 'E2': ('B1','C2')},
	'B': {'C1': ('D2','B1'), 'A1': ('E1','C2'), 'D2': ('D1','E2'), 'E1': ('B1','C1'),
	      'D1': ('C2','A1'), 'B1': ('E2','D2'), 'C2': ('C1','E1'), 'E2': ('A1','D1')}
}


def makeLens(harmonyFeatures, ligature):
	lens = []
	logicalFeet = []
	for foot in ligature:
		logicalFeet.append(foot['foot'])
	print('logicalFeet', logicalFeet)
	# each foot gets a piece
	# calculate how many pieces to cover number of feet
	# 	derive magnitude at which to iterate over locus, apportion to feet
	# calculate how much further to magnify so that there are enough notes for each foot
	# for each foot
'''
      ex. one foot divided by eight:
	  anacrusis                                    station
	                      -1/2     -1/4 -1/8       0   1/8  1/4        1/2
	[[[-1, 0],[0, -1]],  [[0, -1], [-1, -1]]],  [[[0, -1],[-1, -1]],[[-1, -1], [-1, 1]]]
'''


	locus = expand(harmonyFeatures['address'], 5)
	print('locus',locus)
	return lens

def expand(address, magnification):
	magnification = magnification-1
	pattern = 'A'
	# if magnification%2 == 0: pattern = 'A'
	# if magnification%2 == 1: pattern = 'B'
	if magnification > 0:
		return [expand( bisections[pattern][address][0], magnification ), expand( bisections[pattern][address][1], magnification )]
	else:
		return loc[address]
