from binarytree import *
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



{scaffold, configuration, shell, backbone, spine, projection}

# example
dee = Passage()
dee.print()

'''
