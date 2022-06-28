import requests
from bs4 import BeautifulSoup
from lotto import *
from firebase import *
from datetime import datetime


class Scraper(Mega):
	def __init__(self):
		super().__init__()
		self.categories = {'he': {},
		                   'ho': {},
		                   'le': {},
		                   'lo': {},
		                   'mega_number': {}
		                   }

	@staticmethod
	def get_source(link: str):
		"""
		Get the link of the source and convert the html to lxml
		for BeautifulSoup lxml has advantage in reading large xml files,
		which makes faster data processing
		:return: LXML representation of html skeleton of the website
		"""
		website = requests.get(link).text
		source = BeautifulSoup(website, "html.parser")
		return source

	def scraper(self, source, initial=False):
		reference = self.categories if initial else self.refs
		nums_src = source.findAll('li', attrs={'class': 'ball'})
		bonus_src = source.findAll('li', attrs={'class': 'mega-ball'})
		for num in nums_src:
			txt = num.get_text(strip=True)
			nums_add(reference, txt, initial)
		for bonus in bonus_src:
			txt = bonus.get_text(strip=True)
			num_update(reference['mega_number'], txt, initial)

	def first_scrape(self):
		"""
		scrape all
		:return: None
		"""
		current_date = formatter(str(datetime.now()))
		current = current_date[:4]
		for year in range(1996, int(current) + 1):
			link = ''.join([self.link, str(year)])
			source = self.get_source(link)
			self.scraper(source, True)
		print('Updating DB with initial data scraped...')
		self.refs['he'].set(self.categories['he'])
		self.refs['ho'].set(self.categories['ho'])
		self.refs['le'].set(self.categories['le'])
		self.refs['lo'].set(self.categories['lo'])
		self.refs['mega_number'].set(self.categories['mega_number'])
		self.refs['last_update'].update({u'timestamp': current_date})

	def day_scrape(self) -> None:
		current_date = formatter(str(datetime.now()))
		link = ''.join([self.link, get_date(self.refs)])
		source = self.get_source(link)
		self.scraper(source)
		self.refs['last_update'].update({u'timestamp': current_date})
