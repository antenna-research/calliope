from cadence import *
from numpy import array
from numpy.random import choice, seed

class Phonology(object):
	"""weighted repository of rhythmic, harmonic and gestural features"""

	def __init__(self, footprints=[], functions=[], paths=[]):
		self.footprints = footprints
		self.functions = functions
		self.paths = paths

	def addFootprintRule(self, footprintRule, weight=1):
		self.footprints.append((footprintRule, weight))

	def addFunctionRule(self, functionRule, weight=1):
		self.functions.append((functionRule, weight))

	def addPathRule(self, pathRule, weight=1):
		self.paths.append((pathRule, weight))

	def makeCadence(self): # (duration=None, harmonicFilter=None)
		""" assemble bundle of features from phonology rules """
		cadence = Cadence()
		cadence.footprint = self.makeFootprint()
		cadence.function = self.makeFunction()
		cadence.path = self.makePath()
		return cadence

	def makeFootprint(self):
		# select footprint rule
		weights = array([rule[1] for rule in self.functions])
		normalized_weights = weights.astype(float) / weights.sum()
		footprintChoices = array(self.footprints)
		index = choice(len(footprintChoices), p=normalized_weights)
		footprintRule = footprintChoices[index][0]

		# select feature value from range where necessary
		footprint = []
		for footRule in footprintRule:
			foot = {}
			# each foot option is composite
			footChoices = array(footRule['foot'])
			index = choice(len(footChoices))
			foot['foot'] = list(footChoices[index])
			# other feature options aren't
			foot['span'] = choice(footRule['span'])
			foot['gait'] = choice(footRule['gait'])
			# timing options are per note:
			foot['step'] = []
			for steps in footRule['step']:
				foot['step'].append( choice(steps) )
			footprint.append(foot)

		return footprint


	def makeFunction(self):
		# select function rule
		weights = array([rule[1] for rule in self.functions])
		normalized_weights = weights.astype(float) / weights.sum()
		functionChoices = array(self.functions)
		index = choice(len(functionChoices), p=normalized_weights)
		functionRule = functionChoices[index][0]

		# select value from range for each feature
		function = {}
		function['address'] = choice(functionRule['address'])
		function['transposition'] = choice(functionRule['transposition'])

		return function


	def makePath(self):

		# select path rule
		weights = array([rule[1] for rule in self.paths])
		normalized_weights = weights.astype(float) / weights.sum()
		pathChoices = array(self.paths)
		index = choice(len(pathChoices), p=normalized_weights)
		pathRule = pathChoices[index][0]


		# select value from range for each feature
		path = {}
		path['range'] = choice(pathRule['range'])
		path['figure'] = choice(pathRule['figure'])
		path['tilt'] = choice(pathRule['tilt'])

		return path
