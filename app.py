from fastapi import FastAPI
from lotto import *
from firebase import *
from mass_scraper import *

app = FastAPI()

M = Mega()
S = Scraper()


@app.get("/roster")
def getRoster():
    roster =  M.get_roster()
    return roster.split('\n')

@app.get("/date")
def getDate():
    return formatter(str(datetime.now()))

@app.get('/updated date')
def getLastdate():
    return get_date(M.refs)

@app.get('/info')
def getInformation():
    return get_info(M.refs)

@app.get('/numbers')
def getNumbers():
    return M.getAllNumbers()

@app.get('/multipliers')
def getMultipliers():
    return toDict(M.refs, 'mega_number')

@app.put('/new scrape')
def updateNums():
    S.day_scrape()
    return getDate()
