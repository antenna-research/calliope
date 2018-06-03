from phonology import *
from numpy.random import choice, seed

class Lexicon(object):
	def makeLexeme(self):
	def makeProjection(self):

class Lexeme(object):
	"""the specification of an dependant and its agreement"""
	def __init__(self, cadence=None, antecedent=None, consequent=None):
		if cadence=None:
		self.cadence = cadence
		# lexemes
		self.antecedents = []
		self.consequents = []
		# projections
		self.anticipations = []
		self.prolongations = []

		# self.label -- manage serial numbers somehow

	def addAntecedent(self, category):
		self.antecedents.append(category)
		return self

	def addConsequent(self, category):
		self.consequents.append(category)
		return self

	def addAnticipation(self, projection):
		self.anticipations.append(projection)
		return self

	def addProlongation(self, projection):
		self.prolongations.append(projection)
		return self


	def selectAntecedent(self):
		antecedent = None
		if len(self.antecedents>0):
			antecedent = choice(self.antecedents)
		return antecedent

	def selectConsequent(self):
		consequent = None
		if len(self.consequents>0):
			consequent = choice(self.consequents)
		return consequent

	def selectAnticipation(self):
		anticipation = None
		if len(self.anticipations>0):
			anticipation = choice(self.anticipations)
		return anticipation

	def selectProlongation(self):
		prolongation = None
		if len(self.prolongations>0):
			prolongation = choice(self.prolongations)
		return prolongation


