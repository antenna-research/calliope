from binarytree import *

class Diagram(object):
	"""represents a syntactic structure (wrapper for binary tree)
	"""
	def __init__(self, height=3, size=None):
		self.tree = tree(height=height)
		if isinstance(size, int):
			if size>height and size<((2^(height+1))-1):
				while self.tree.size != size:
					self.tree = tree(height=height)
			else:
	            # raise NodeNotFoundError('no node to delete at index {}')
				print('syntax diagram impossible for height'+height+'and size'+size)

	def print(self):
		self.tree.pprint(index=True, delimiter='\'')

'''
# example
dee = Diagram()
dee.print()
'''