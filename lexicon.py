from grammar import *
from numpy.random import choice, seed

class Lexicon(object):

	def __init__(self):
		self.categories = []

	def populate(self, grammar, number_categories=0):
		for x in range(number_categories):
			lexeme = self.makeLexeme(grammar)
			lexeme.label = self.nextLabel()
			self.categories.append(lexeme)

	def addLexeme(self, grammar, lexeme=None):
		if lexeme == None:
			lexeme = self.makeLexeme(grammar)
		lexeme.label = self.nextLabel()
		self.categories.append(lexeme)

	def makeLexeme(self, grammar):
		cadence = grammar.phonology.makeCadence()
		anticipation = grammar.morphology.selectAnticipation()
		prolongation = grammar.morphology.selectProlongation()
		lexeme = Lexeme(cadence, anticipation, prolongation)
		return lexeme

	def selectLexeme(self, index=None):
		if index == None:
			lexeme = choice(self.categories)
		else:
			lexeme = self.categories[index]
		return lexeme

	def nextLabel(self):
		nextLabel = 0
		if len(self.categories) > 0:
			nextLabel = self.categories[-1].label + 1
		return nextLabel

	def print(self):
		for i, lex in enumerate(self.categories):
			print('Lexeme', str(i))
			print('--------')
			lex.print()
			print()


class Lexeme(object):
	"""the specification of an dependant and its agreement"""
	def __init__(self, cadence, anticipation=None, prolongation=None):
		self.cadence = cadence

		# projections
		self.anticipation = anticipation
		self.prolongation = prolongation

		# dependents
		self.antecedents = []
		self.consequents = []

		self.label = 'unlabeled'

	def print(self):
		print("\n"+str(self.label))
		self.cadence.print()
		print("anticipation:", self.anticipation)
		print("prolongation:", self.prolongation)
		print("antecedents:", self.antecedents)
		print("consequents:", self.consequents)

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


