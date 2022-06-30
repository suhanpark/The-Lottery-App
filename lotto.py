from itertools import combinations
from firebase import *
from collections import Counter
from typing import Callable, List, Dict, Optional


class Mega:
	__slots__ = ['link', 'link1', 'root', 'nums'
	             'latest', 'refs', 'last_update']

	def __init__(self):
		root = config()
		self.link = 'https://www.lottery.net/mega-millions/numbers/'
		self.link1 = 'https://www.lottery.net/mega-millions'
		self.refs = {
			'he': root.document(u'high_even'),
			'ho': root.document(u'high_odd'),
			'le': root.document(u'low_even'),
			'lo': root.document(u'low_odd'),
			'mega_number': root.document(u'mega_number'),
			'last_update': root.document(u'last_update'),
			'info': root.document(u'info')
		}

	def __str__(self):
		return str(self.link)

	@staticmethod
	def get_three(D: Dict) -> List[str]:
		"""
		Helper function for get_roster()
		O(N); N=len(D)
		:param D:
		:return: tuple
		"""
		c = Counter(D).most_common(3)
		return [c[0][0], c[1][0], c[2][0]]

	@staticmethod
	def getCombs(threes: List) -> List:
		"""
		Helper function for get_roster()
		O(12)~O(1)
		:param threes:
		:return:
		"""
		combs = []
		for ind, trio in enumerate(threes):
			combs.append([combo for combo in combinations(trio, 2)])
		return combs

	@staticmethod
	def maker(count: int, first: list, second: list):
		return f'\n{count}. Numbers: {first[0]}, {first[1]}, {first[2]}, {second[0]}, {second[1]}'		
 
	def get_roster(self):
		"""
		O(4N+12+12)=O(4N+24)~O(N)
		:return: string or dictionary
		"""
		mult_doc = self.get_three(toDict(self.refs, 'mega_number'))
		high_even = self.get_three(toDict(self.refs, 'he'))
		high_odd = self.get_three(toDict(self.refs, 'ho'))
		low_even = self.get_three(toDict(self.refs, 'le'))
		low_odd = self.get_three(toDict(self.refs, 'lo'))

		combs = self.getCombs([high_even, high_odd, low_even, low_odd])
		roster = f'Mega Multipliers: {mult_doc[0]}, {mult_doc[1]}, {mult_doc[2]}'
		count = 1
		for ind, comb in enumerate(combs):
			for tup in comb:
				if ind == 0:
					roster += self.maker(count, low_odd, tup)
				elif ind == 1:
					roster += self.maker(count, low_even, tup)
				elif ind == 2:
					roster += self.maker(count, high_odd, tup)
				elif ind == 3:
					roster += self.maker(count, high_even, tup)
				count += 1
		return roster
