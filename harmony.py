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
	logicalFeet = [foot['foot'] for foot in ligature]

	numberOfSubloci = len(logicalFeet)
	footMagnificationfactor = 0
	while numberOfSubloci > 2**footMagnificationfactor:
		footMagnificationfactor += 1

	footAddresses = expand(harmonyFeatures['address'], footMagnificationfactor, False)
	if footMagnificationfactor == 0:
		footAddresses = [footAddresses]

	for i, foot in enumerate(logicalFeet):
		address = footAddresses[i]
		for note in foot:
			if note == 0:
				lens.append( expand(address, 1) )
			if note == 1/2:
				lens.append( flatten(expand(address, 3))[3] )
			if note == -1/2:
				lens.append( flatten(expand(address, 3))[1] )
			if note == 1/4:
				lens.append( flatten(expand(address, 4))[5] )
			if note == -1/4:
				lens.append( flatten(expand(address, 4))[3] )
			if note == 1/8:
				lens.append( flatten(expand(address, 5))[9] )
			if note == -1/8:
				lens.append( flatten(expand(address, 5))[7] )
			if note == 1/16:
				lens.append( flatten(expand(address, 6))[17] )
			if note == -1/16:
				lens.append( flatten(expand(address, 6))[15] )
			if note == 1/32:
				lens.append( flatten(expand(address, 7))[33] )
			if note == -1/32:
				lens.append( flatten(expand(address, 7))[31] )
	return lens

def expand(address, magnification, getValues=True):
	magnification = magnification-1
	if magnification%2 == 0: pattern = 'A'
	if magnification%2 == 1: pattern = 'B'
	if magnification > 0:
		return [expand( bisections[pattern][address][0], magnification, getValues ), expand( bisections[pattern][address][1], magnification, getValues )]
	else:
		if getValues:
			return loc[address]
		else:
			return address

'''
		each foot gets a piece
		calculate how many pieces to cover number of feet
			if number of feet is less than 2**x, maybe give feet with longer duration a double portion
			derive magnitude(s) at which to iterate over locus, apportion to feet
		calculate how much further to magnify so that there are enough notes for each foot

			ex. one foot divided by eight:
			anacrusis                                    station
			                      -1/2     -1/4 -1/8       0   1/8  1/4        1/2
			[[[-1, 0],[0, -1]],  [[0, -1], [-1, -1]]],  [[[0, -1],[-1, -1]],[[-1, -1], [-1, 1]]]


			or better yet:
			                      -1/2     -1/4 -1/8       0   1/8  1/4        1/2
														   1
            [  -1,                                        -1                     ]
            [[  1,                  0],                   [1,                 -1]]
            [[[-1,     -1],        [0,        1]],      [[-1,       1],       [1,       1]]] 
			[[[[1, 0], [1, -1]],  [[0, 1], [-1, 0]]],   [[[1, -1], [-1, -1]], [[-1, 0], [-1, 1]]]]
			
			 0 = exp(0) = flatten(exp(2))[2]

			-1/2 = exp(flatten(exp(2))[1])
			 1/2 = exp(flatten(exp(2))[3])
			-1/4 = exp(flatten(exp(3))[3])
			 1/4 = exp(flatten(exp(3))[5])
			-1/8 = exp(flatten(exp(2))[7])
			 1/8 = exp(flatten(exp(2))[9])
	'''