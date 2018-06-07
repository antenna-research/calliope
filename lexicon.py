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
		print('Lexicon')
		for i, lex in enumerate(self.categories):
			lex.print()
			print()


class Lexeme(object):
	"""the specification of an dependant and its agreement"""
	def __init__(self, cadence, anticipation=None, prolongation=None):
		self.cadence = cadence

		self.government = {
			# projected features
			'anticipation': anticipation,
			'prolongation': prolongation,
			# dependents
			'antecedents': [],
			'consequents': [],
		}

		self.realization = {}
		self.label = 'unlabeled'

	def print(self):
		print("\nlexeme "+str(self.label))
		self.cadence.print()
		pprint(self.government)

	def addAntecedent(self, category):
		self.antecedents.append(category)
		return self

	def addConsequent(self, category):
		self.consequents.append(category)
		return self

	def addAnticipation(self, projection):
		self.government['anticipation'].append(projection)
		return self

	def addProlongation(self, projection):
		self.government['prolongation'].append(projection)
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
		if len(self.government['anticipation']>0):
			anticipation = choice(self.government['anticipation'])
		return anticipation

	def selectProlongation(self):
		prolongation = None
		if len(self.government['prolongation']>0):
			prolongation = choice(self.government['prolongation'])
		return prolongation

