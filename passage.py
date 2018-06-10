from binarytree import *
from utils import *
from math import ceil, floor
from copy import copy, deepcopy
from pprint import pprint
import rhythm
import path
import harmony

class Passage(object):
	"""represents a syntactic structure (wrapper for binary tree)"""

	def __init__(self, height=3, size=None):
		self.tree = tree(height=height)
		if isinstance(size, int):
			if size>=height and size<((2**(height+1))-1):
				while self.tree.size != size:
					self.tree = tree(height=height)
			else:
				print('Syntax tree of height '+str(height)+' must have between '+str(height+1)+' and '+str((2**(height+1))-1)+' nodes, but you asked for '+str(size)+' nodes.')
		# relabel nodes in level order
		for i, node in enumerate(self.tree.levelorder):
			node.value = i
			node.unify = {}

		# sequence of lexeme objects constituting passage
		self.spelling = []

		# duration of each individual foot in each ligature (including any pickup)
		self.durations = []

		# duration of the pre-barline portion of each lexeme 
		self.anacruses = []

		# duration of the post-barline portion of each lexeme
		self.stations = []

		self.bars = []

	def printSyntax(self):
		print(self.tree)

	def print(self):
		lexemes = []
		for lex in self.spelling:
			lexemes.append({
				'_label': lex.label,
				'ligature': lex.cadence.ligature,
				'function': lex.cadence.function,
				'path': lex.cadence.path,
				'realization': lex.realization,
			})
		pprint(lexemes)

	def spellout(self, lexicon):
		# prolonged features trickle down to leaves
		for node in self.tree.levelorder:
			node.lexeme = lexicon.selectLexeme()
			node.value = node.lexeme.label

			if node.left:
				node.left.unify = copy(node.unify)
				for feat in node.lexeme.government['anticipation']:
					# if feat == 'ligature': <- take off first condition for 'agree' prolongation
					if feat not in node.left.unify.keys() and feat == 'ligature':
						node.left.unify['ligature'] = node.lexeme.cadence.ligature
					if feat not in node.left.unify.keys() and feat in node.lexeme.cadence.function:
						node.left.unify[feat] = node.lexeme.cadence.function[feat]
					if feat not in node.left.unify.keys() and feat in node.lexeme.cadence.path:
						node.left.unify[feat] = node.lexeme.cadence.path[feat]

			if node.right:
				node.right.unify = copy(node.unify)
				for feat in node.lexeme.government['prolongation']:
					if feat not in node.right.unify.keys() and feat == 'ligature':
						node.right.unify['ligature'] = node.lexeme.cadence.ligature
					if feat not in node.right.unify.keys() and feat in node.lexeme.cadence.function:
						node.right.unify[feat] = node.lexeme.cadence.function[feat]
					if feat not in node.right.unify.keys() and feat in node.lexeme.cadence.path:
						node.right.unify[feat] = node.lexeme.cadence.path[feat]

		spellout = []
		# read out nodes into list
		for node in self.tree.inorder:
			next_lexeme = node.lexeme # deepcopy(node.lexeme)
			# prolonged features replace lexical features, unless lexeme projects that feature itself
			reprojectedFeatures = []
			for feat in node.unify.keys():
				if feat in next_lexeme.government['prolongation'] or next_lexeme.government['anticipation']:
					reprojectedFeatures.append(feat)
			for feat in reprojectedFeatures:
				del node.unify[feat]
			for feat in node.unify.keys():
				if feat == 'ligature':
					next_lexeme.cadence.ligature = node.unify[feat]
				if feat in ['address', 'transposition']:
					next_lexeme.cadence.function[feat] = node.unify[feat]
				if feat in ['range','figure','direction']:
					next_lexeme.cadence.path[feat] = node.unify[feat]
			spellout.append(next_lexeme)
		self.spelling = spellout
		self.setMeter()
		self.setFigure()
		self.setHarmony()
		return spellout

	def setHarmony(self):
		for i, node in enumerate(self.tree.levelorder):
			node.lexeme.realization['lens'] = harmony.makeLens(node.lexeme.cadence.function, node.lexeme.cadence.ligature)

	def setFigure(self):
		for i, node in enumerate(self.tree.levelorder):
			if i == 0:
				node.lexeme.realization['height'] = 0
			if node.left:
				leadingDirection = node.left.lexeme.cadence.path['direction']
				node.left.lexeme.realization['height'] = node.lexeme.realization['height'] - leadingDirection
			if node.right:
				trailingDirection = node.right.lexeme.cadence.path['direction']
				node.right.lexeme.realization['height'] = node.lexeme.realization['height'] + trailingDirection
			node.lexeme.realization['outline'] = path.makeOutline(node.lexeme.cadence.path, node.lexeme.realization)

	def setMeter(self):
		durations = self.getDurations(self.spelling)
		pickupBar = max([fl(ceil(-self.anacruses[0])),2.0])
		bars = []
		for i in range(len(self.stations)-1):
			bars.append(self.stations[i]-self.anacruses[i+1])
		bars.append(self.stations[-1])
		# partitionedBars = self.partition(bars, self.tree)

		removedIndices = []
		prolongedIndices = []
		while isOversliced(bars):
			bars, removedIndices, prolongedIndices = self.desliceBars(bars, removedIndices, prolongedIndices)

		removedIndices.sort()
		removedIndices.reverse()
		for index in removedIndices:
			bars.pop(index)

		bars.insert(0, pickupBar)
		self.bars = bars
		return bars

	def desliceBars(self, bars, removedIndices, prolongedIndices):
		# targets = [bar < 2.5 for bar in bars]
		# i = targets.index(True)
		targets = []
		for b, bar in enumerate(bars):
			if bar > 0 and bar < 2.0:
				targets.append(self.tree.inorder[b].size)
			else:
				targets.append(0)

		i = targets.index(max(targets))
		prev = i-1
		next = i+1
		while prev in removedIndices:
			prev -= 1
		while next in removedIndices:
			next += 1

		scores = [node.size for node in self.tree.inorder]
		if bars[i] < 2.0:
			right = False
			if i == 0 or prev < 0:
				right = True
			elif i == len(bars)-1 or next > len(bars)-1:
				right = False
			else:
				if bars[i]+bars[next] <= 4.0 and bars[i]+bars[prev] > 4.0:
					right = True
				elif bars[i]+bars[next] > 4.0 and bars[i]+bars[prev] <= 4.0:
					right = False
				if bars[i]+bars[next] <= 5.0 and bars[i]+bars[prev] > 5.0:
					right = True
				elif bars[i]+bars[next] > 5.0 and bars[i]+bars[prev] <= 5.0:
					right = False
				if bars[i]+bars[next] <= 6.0 and bars[i]+bars[prev] > 6.0:
					right = True
				elif bars[i]+bars[next] > 6.0 and bars[i]+bars[prev] <= 6.0:
					right = False
				else:
					if (scores[i] > scores[prev]) and (next not in prolongedIndices):
						right = True
					else:
						right = False

			if right == True:
				bars[i] += bars[next]
				bars[next] = 0.0
				removedIndices.append(next)
				prolongedIndices.append(i)
			else:
				bars[i] += bars[prev]
				bars[prev] = 0.0
				removedIndices.append(prev)

		return bars, removedIndices, prolongedIndices


	def partition(self, bars, syntaxTree):

		if syntaxTree.left: 
			if syntaxTree.left.height > 0:
				splitAt = syntaxTree.inorder.index(syntaxTree.left.inorder[-1])
				leftBars = bars[0:splitAt+1]
				leftBars = self.partition(leftBars, syntaxTree.left)
			else:
				leftIndex = syntaxTree.inorder.index(syntaxTree.left.inorder[-1])
				leftBars = bars[leftIndex]
		else:
			leftBars = None

		if syntaxTree.right: 
			if syntaxTree.right.height > 0:
				splitAt = syntaxTree.inorder.index(syntaxTree.right.inorder[0])
				rightBars = bars[splitAt:]
				rightBars = self.partition(rightBars, syntaxTree.right)
				if isinstance(rightBars, float) or isinstance(rightBars, int):
					rightBars = [bars[splitAt-1], rightBars]
				else:
					rightBars.insert(0, bars[splitAt-1])
			else:
				rightIndex = syntaxTree.inorder.index(syntaxTree.right.inorder[0])
				rightBars = bars[rightIndex-1:rightIndex+1]
		else:
			# rightIndex = syntaxTree.inorder.index(syntaxTree.right.inorder[-1])
			rightBars = bars[-1]

		if leftBars != None and rightBars != None:
			newBars = [leftBars, rightBars]
		elif leftBars != None:
			newBars = leftBars
		elif rightBars != None:
			newBars = rightBars
		else:
			newBars = []

		return newBars


	def getDurations(self, spelling):
		durations = []
		anacruses = []
		for lexeme in spelling:
			# special extra bit before barline
			anacrusis = 0.0
			boundaryEvents = []
			metricBoundaries = []
			subdurations = []
			lexeme.realization['feet'] = []
			for i, foot in enumerate(lexeme.cadence.ligature):
				offsets = rhythm.getOffsets(foot)
				lexeme.realization['feet'].append(offsets)

				firstAttack = offsets[0]
				lastAttack = offsets[-1]
				boundaryEvents.append( (firstAttack, offsets[-1]) )

				leadingBoundary = 0
				if firstAttack < 0:
					leadingBoundary = floor((firstAttack*4)) / 4
					# leadingBoundary = floor(firstAttack) # use this version for whole-beat measures (1 of 3)

				trailingBoundary = 0
				if lastAttack > 0:
					trailingBoundary = ceil((lastAttack*4)) / 4
					# trailingBoundary = ceil(lastAttack) # use this version for whole-beat measures (2 of 3)

				# give last note some time to sustain
				if lastAttack - floor(lastAttack) == 0:
					trailingBoundary += 0.25
				 # comment below out in case of whole-beat measures (3 of 3)
				if lastAttack - floor(lastAttack) == 0.25:
					trailingBoundary += 0.25

				# pad out to minimum duration
				if trailingBoundary < foot['span']:
					trailingBoundary = fl(foot['span'])

				metricBoundaries.append( (leadingBoundary, trailingBoundary) )
				subdurations.append(trailingBoundary - leadingBoundary)

				# remember anacrusis of first foot - barline will come after it
				if i == 0:
					anacruses.append(leadingBoundary)

			durations.append(subdurations)

		self.durations = durations
		self.anacruses = anacruses
		self.stations = [sum(self.durations[i]) + self.anacruses[i] for i in range(len(durations))]
		return durations

	def fitToInstrument(self, instrument):
		floor, ceiling = (instrument.lowestNote.ps, instrument.highestNote.ps)
		self.fitConstituent(self.tree, floor, ceiling)

	def fitConstituent(self, constituent, floor, ceiling):
		pitches = []
		for node in constituent.inorder:
			for i, target in enumerate(node.lexeme.realization['outline']):
				pitches.append(target + node.lexeme.realization['lens'][i])
		pitchReference = deepcopy(pitches)
		shift = 0
		print(pitchReference)
		while min(pitchReference) > floor+12:
			pitchReference = [pitch-12 for pitch in pitchReference]
			print(pitchReference)
			shift -= 12
		while min(pitchReference) < floor:
			pitchReference = [pitch+12 for pitch in pitchReference]
			print(pitchReference)
			shift += 12
		if max(pitchReference) > ceiling and constituent.left and constituent.right: # and constituent.left.min_leaf_depth>1 and constituent.right.min_leaf_depth>1:
			self.fitConstituent(constituent.left, floor, ceiling)
			self.fitConstituent(constituent.right, floor, ceiling)
		else:
			print(constituent)
			print(min(pitchReference), floor, max(pitchReference), ceiling)
			print(constituent.left)
			print(constituent.right)
			for node in constituent.inorder:
				node.lexeme.realization['shift'] = shift
