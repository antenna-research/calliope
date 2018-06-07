from pprint import pprint

'''
Cadence
	--from Latin cadō ("I fall, I cease").  Doublet of cadenza and chance.

	That which closes - the cork which makes the bottle
		Contrast prolongation: that which keeps open
	The act or state of declining or sinking.
		A fall in inflection of a speaker’s voice, such as at the end of a sentence.
		A progression of at least two chords which conclude a segment of music; musical punctuation; a clausula.
		A move which ends a phrase in dance.
	Rhythmic flow. ("The cadence of life is about to change.")
		The measure or beat of movement.
		The rhythm and sequence of a series of actions.
		The number of steps per unit time.
	The general inflection or modulation of the voice, or of any sound.

'''

class Cadence(object):
	"""a musical morpheme bundling rhythmic, gestural and harmonic features"""
	def __init__(self, ligature=None, function=None, path=None):
		self.ligature = ligature
		self.function = function
		self.path = path

	# string represention of cadence - note list ?
	def __str__(self):
		features = {
			'ligature': self.ligature,
			'function': self.function,
			'path': self.path,
		}
		return str(features)

	@property
	def features(self):
		features = {
			'ligature': self.ligature,
			'function': self.function,
			'path': self.path,
		}
		return features

	def update(featureDict):
		if 'ligature' in featureDict:
			self.ligature = featureDict['ligature']
		if 'function' in featureDict:
			self.function.update(featureDict['function'])
		if 'path' in featureDict:
			self.path.update(featureDict['path'])

	def print(self):
		features = {
			'ligature': self.ligature,
			'function': self.function,
			'path': self.path,
		}
		pprint(features)

'''
# example
cad = Cadence()

cad.ligature = [{
	'span': 2,
	'gait': 'double', # Gait.double or Gait['double']...
	'foot': [-1/2, -1/4, 0, 1/2],
	'sync': [0, 0, 0, 1/2],
},{
	'span': 1,
	'gait': 'double',
	'foot': [None],
	'sync': [None],
},{
	'span': 1,
	'gait': 'double',
	'foot': [-1/2, 0, 1/4, 1/2],
	'sync': [1/2, 0, 0, 0],
}]

cad.function = {
	'address': 'A1',
	'transposition': 1,
}

cad.path = {
	'range': 2,
	'figure': 'rampUp',
	'direction': 'float',
}

cad.print()  # = pprint(cad.features)
'''