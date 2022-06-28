from mass_scraper import *
from twilioOps import *


if __name__ == "__main__":
	print('DB connecting...')
	M = Mega()
	S = Scraper()
	print('Connected Successfully')

	if get_date(M.refs) == '1996':
		print('Initial Scraping...')
		S.first_scrape()
		print('Initial Scraping Complete')
	else:
		print('Day Scraping...')
		S.day_scrape()
		print('Day Scraping Complete')

	print('Generating Message...')
	Message = f"<Recently updated Michigan Mega Millions Numbers>\n" \
	          f"Updated MMM Numbers {get_date(M.refs)}\n" \
	          f"{M.get_roster()}\n" \
	          f"\n-Automated Message Sent by LNP"
	notif(Message)
	print('Message Sent!')
