import math
from pprint import pprint
from utils import *

figures = {
	# sample continuous functions, apply scaling factor
	'flat': lambda x: 1,
	'rampUp': lambda x: x,
	'rampDown': lambda x: -x,
	'accUp': lambda x: math.sin(5*(x-1)/math.pi)+1,
	'accDown': lambda x: -(math.sin(5*(x-1)/math.pi)+1),
	'decUp': lambda x: math.sin(5*x/math.pi),
	'decDown': lambda x: -math.sin(5*x/math.pi),
	'triangleUp': lambda x: abs(((((x/2)+0.25)%(0.5))*4)-1),
	'triangleDown': lambda x: -abs(((((x/2)+0.25)%(0.5))*4)-1),
	'saddleUp': lambda x: math.sin(10*(x-0.5)/math.pi),
	'saddleDown': lambda x: -math.sin(10*x/math.pi),
	'spikeUp': lambda x: -(abs(math.sin(10*(x-0.5)/math.pi))-1),
	'spikeDown': lambda x: abs(math.sin(10*(x-0.5)/math.pi))-1,
	'zigZagDown': lambda x: (abs((((x/2)%(0.3333)+0.1667)*3)-1.0)-0.5)*2,
	'zigZagUp': lambda x: -(abs((((x/2)%(0.3333)+0.1667)*3)-1.0)-0.5)*2,
	'sawtooth1Up': lambda x: x%(1.0),   # same as ramp except f(1.0)==0
	'sawtooth1Down': lambda x: -x%(1.0),
	'sawtooth2Up': lambda x: (x%(0.5))*2,
	'sawtooth2Down': lambda x: -(x%(0.5))*2,
	'sawtooth3Up': lambda x: (x%(0.3333))*3,
	'sawtooth3Down': lambda x: -(x%(0.3333))*3,
	# 'stepUp': just use if/then
	# 'stepDn': just use if/then
# etc
}

def makeOutline(pathFeatures, realizationFeatures):
	outline = []
	cardinality = len(flatten(realizationFeatures['feet']))
	for i in range(cardinality):
		positionRatio = i / cardinality
		# calculate relative positions
		pitch = figures[pathFeatures['figure']](positionRatio)
		# scale by height
		pitch = round(pitch * pathFeatures['range'])
		# shift by direction
		pitch += realizationFeatures['height']
		outline.append(pitch)
	return outline

	# print('"feet"', feet)
	# span = voice['span'][1] - voice['span'][0]
	# proportional - also try sampling function evenly by # notes.
	# for note in voice['notes']:
	# 	position_ratio = (note[1] - voice['span'][0]) / span

