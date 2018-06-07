from cadence import *
from numpy import array
from numpy.random import choice, seed

class Grammar(object):

	def __init__(self, phonology=None, morphology=None, syntax=None):
		self.phonology = phonology
		self.morphology = morphology
		self.syntax = syntax


class Phonology(object):
	"""weighted repository of rhythmic, harmonic and gestural features"""

	def __init__(self, ligatures=[], functions=[], paths=[]):
		self.ligatures = ligatures
		self.functions = functions
		self.paths = paths

	def print(self):
		features = {
			'ligatures': self.ligatures,
			'functions': self.functions,
			'paths': self.paths,
		}
		print("\nPhonology")
		pprint(features)
		print()

	def addligatureRule(self, ligatureRule, weight=1):
		self.ligatures.append((ligatureRule, weight))

	def addFunctionRule(self, functionRule, weight=1):
		self.functions.append((functionRule, weight))

	def addPathRule(self, pathRule, weight=1):
		self.paths.append((pathRule, weight))

	def makeCadence(self): # (duration=None, harmonicFilter=None)
		""" assemble bundle of features from phonology rules """
		cadence = Cadence()
		cadence.ligature = self.makeligature()
		cadence.function = self.makeFunction()
		cadence.path = self.makePath()
		return cadence

	def makeligature(self):
		# select ligature rule
		weights = array([rule[1] for rule in self.ligatures])
		normalized_weights = weights.astype(float) / weights.sum()
		ligatureChoices = array(self.ligatures)
		index = choice(len(ligatureChoices), p=normalized_weights)
		ligatureRule = ligatureChoices[index][0]

		# select feature value from range where necessary
		ligature = []
		for footRule in ligatureRule:
			foot = {}
			# each foot option is composite
			footChoices = array(footRule['foot'])
			index = choice(len(footChoices))
			foot['foot'] = list(footChoices[index])
			# other feature options aren't
			foot['span'] = choice(footRule['span'])
			foot['gait'] = choice(footRule['gait'])
			# timing options are per note:
			foot['sync'] = []
			for steps in footRule['sync']:
				foot['sync'].append( choice(steps) )
			ligature.append(foot)

		return ligature


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
		path['direction'] = choice(pathRule['direction'])

		return path


class Morphology(object):

	def __init__(self):
		self.anticipationRules = []
		self.prolongationRules = []

	def addAnticipationRule(self, projectedFeatures):
		self.anticipationRules.append(projectedFeatures)

	def addProlongationRule(self, projectedFeatures):
		self.prolongationRules.append(projectedFeatures)

	def selectAnticipation(self):
		return choice(self.anticipationRules)

	def selectProlongation(self):
		return choice(self.prolongationRules)

	def print(self):
		features = {
			'anticipations': self.anticipationRules,
			'prolongations': self.prolongationRules,
		}
		print("\nMorphology")
		pprint(features)
		print()


