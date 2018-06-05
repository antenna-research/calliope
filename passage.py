import rhythm
from binarytree import *
from utils import *
from math import ceil, floor
from copy import copy, deepcopy

class Passage(object):
	"""represents a syntactic structure (wrapper for binary tree)
	"""
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
		self.unified = []
		self.durations = []
		self.anacruses = []
		self.landings = []
		self.bars = []

	def printSyntax(self):
		print(self.tree)

	def spellout(self, lexicon):
		# prolonged features trickle down to leaves
		for node in self.tree.levelorder:
			node.lexeme = lexicon.selectLexeme()
			node.value = node.lexeme.label

			if node.left:
				node.left.unify = copy(node.unify)
				for feat in node.lexeme.anticipation:
					# if feat == 'footprint': <- take off first condition for 'agree' prolongation
					if feat not in node.left.unify.keys() and feat == 'footprint':
						node.left.unify['footprint'] = node.lexeme.cadence.footprint
					if feat not in node.left.unify.keys() and feat in node.lexeme.cadence.function:
						node.left.unify[feat] = node.lexeme.cadence.function[feat]
					if feat not in node.left.unify.keys() and feat in node.lexeme.cadence.path:
						node.left.unify[feat] = node.lexeme.cadence.path[feat]

			if node.right:
				node.right.unify = copy(node.unify)
				for feat in node.lexeme.prolongation:
					if feat not in node.right.unify.keys() and feat == 'footprint':
						node.right.unify['footprint'] = node.lexeme.cadence.footprint
					if feat not in node.right.unify.keys() and feat in node.lexeme.cadence.function:
						node.right.unify[feat] = node.lexeme.cadence.function[feat]
					if feat not in node.right.unify.keys() and feat in node.lexeme.cadence.path:
						node.right.unify[feat] = node.lexeme.cadence.path[feat]

		spellout = []
		# now read out nodes into list, with prolonged features replacing lexical features
		for node in self.tree.inorder:
			next_lexeme = deepcopy(node.lexeme)
			for feat in node.unify.keys():
				if feat == 'footprint':
					next_lexeme.cadence.footprint = node.unify[feat]
				if feat in ['address', 'transposition']:
					next_lexeme.cadence.function[feat] = node.unify[feat]
				if feat in ['range','figure','tilt']:
					next_lexeme.cadence.path[feat] = node.unify[feat]
			spellout.append(next_lexeme)
		self.unified = spellout
		return spellout


	def setMeter(self):
		durations = self.getDurations(self.unified)
		pickupBar = max([fl(ceil(-self.anacruses[0])),2.0])
		bars = []
		for i in range(len(self.durations)-1):
			bars.append(self.landings[i]-self.anacruses[i+1])
		bars.append(self.landings[-1])
		# partitionedBars = self.partition(bars, self.tree)
		# depthScores = (flatten(depth(partitionedBars,0)))
		# depthTransitions = [abs(depthScores[i]-depthScores[i+1]) for i in range(len(depthScores)-1) ]

		print('bars',bars)
		# print('depthScores',depthScores)
		removedIndices = []
		while isOversliced(bars):
			bars, removedIndices = self.desliceBars(bars, removedIndices)

		print('bars',bars)		
		removedIndices.sort()
		removedIndices.reverse()
		print('removedIndices',removedIndices)		
		for index in removedIndices:
			bars.pop(index)
		print('bars',bars)

		bars.insert(0, pickupBar)
		self.bars = bars
		return bars


	def desliceBars(self, bars, removedIndices):
		# targets = [bar < 2.5 for bar in bars]
		# i = targets.index(True)
		targets = []
		for b, bar in enumerate(bars):
			if bar < 2.5:
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

		print('targets', targets)
		print('max(targets)', max(targets), 'targets.index(max(targets))', targets.index(max(targets)))
		scores = [node.size for node in self.tree.inorder]
		print('scores',scores)
		if bars[i] < 2.5:
			right = False
			if i == 0 or prev < 0:
				right = True
			elif i == len(bars)-1 or next > len(bars)-1:
				right = False
			else:
				if bars[i]+bars[next] < 6 and bars[i]+bars[prev] > 6:
					right = True
				elif bars[i]+bars[next] > 6 and bars[i]+bars[prev] < 6:
					right = False
				else:
					if scores[i] > scores[prev]:
						right = True
					else:
						right = False

			if right == True:
				bars[i] += bars[next]
				# bars.pop(next)
				removedIndices.append(next)
			else:
				bars[i] += bars[prev]
				# bars.pop(prev)
				removedIndices.append(prev)
		return bars, removedIndices

	def consolidate(self, bars):
		# [[[3.0, [2.5, 2.5, [5.0, 4.5]]], [2.5, [5.0, 7.0], [7.0, 4.5]]], [3.0, [5.0, [4.5, 5.0, 7.0, 5.0]], [5.0, [[4.5, 5.0], [7.0, 7.0, 4.5]], 2.0]]]
		for component in bars:
			pass

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


	def incrementalSetMeter(self, durations, anacruses, landings):
		firstChunk = -anacruses[0]
		firstBar = ceil(firstChunk)
		bars = [firstBar]
		load = 0
		partitions = []
		nextPartition = []
		for i, duration in enumerate(durations):
			nextChunk = landings[i]
			if (i+1) < len(landings):
				nextChunk -= anacruses[i+1]
			load += nextChunk
			nextPartition.append(duration)
			if load >= 3:
				bars.append(load)
				partitions.append(nextPartition)
				load = 0
				nextPartition = []
		return bars, partitions

	def getDurations(self, unified):
		durations = []
		anacruses = []
		for lexeme in unified:
			# special extra bit before barline
			anacrusis = 0.0
			boundaryEvents = []
			metricBoundaries = []
			subdurations = []
			for i, foot in enumerate(lexeme.cadence.footprint):
				offsets = rhythm.getOffsets(foot)
				firstAttack = offsets[0]
				lastAttack = offsets[-1]
				boundaryEvents.append( (firstAttack, offsets[-1]) )

				leadingBoundary = 0
				if firstAttack < 0:
					leadingBoundary = floor((firstAttack*2)) / 2
					# leadingBoundary = floor(firstAttack) # use this version for whole-beat measures (1 of 3)

				trailingBoundary = 0
				if lastAttack > 0:
					trailingBoundary = ceil((lastAttack*2)) / 2
					# trailingBoundary = ceil(lastAttack) # use this version for whole-beat measures (2 of 3)

				# give last note some time to sustain
				if lastAttack - floor(lastAttack) == 0:
					trailingBoundary += 1
				 # comment below out in case of whole-beat measures (3 of 3)
				if lastAttack - floor(lastAttack) == 0.5:
					trailingBoundary += 0.5

				# pad out to minimum duration
				if trailingBoundary < foot['span']:
					trailingBoundary = fl(foot['span'])

				metricBoundaries.append( (leadingBoundary, trailingBoundary) )
				subdurations.append(trailingBoundary - leadingBoundary)

				# remember anacrusis of first foot - barline will come after it
				if i == 0:
					anacruses.append(leadingBoundary)

			durations.append(sum(subdurations))

			# print('boundaryEvents', boundaryEvents)
			# print('metricBoundaries', metricBoundaries)
			# print('subdurations', subdurations)

		# print('durations', durations)
		# print('anacruses', anacruses)
		self.durations = durations
		self.anacruses = anacruses
		self.landings = [self.durations[i] + self.anacruses[i] for i in range(len(durations))]
		return durations


'''

>>> print(root)

    __1
   /   \
  2     3
 / \
4   5

>>> root.inorder - linear order of lexemes
[Node(4), Node(2), Node(5), Node(1), Node(3)]

>>> root.levelorder
[Node(1), Node(2), Node(3), Node(4), Node(5)]

>>> root.preorder
[Node(1), Node(2), Node(4), Node(5), Node(3)]

>>> root.postorder
[Node(4), Node(5), Node(2), Node(3), Node(1)]

'''
