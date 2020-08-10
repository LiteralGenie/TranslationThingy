import utils,time,re
from selenium.common.exceptions import NoSuchElementException as NoSuchElementException
from bs4 import BeautifulSoup as bs



def hotfix(text):
	ret= text
	subs= {
		"regex": { "chars": [], "reps": [] },
		"order": {"chars": ["기사단"], "reps": ["Knight Order"]},
		"knight": {"chars": ["기사"], "reps": ["Knight"]},
		"leo": {"chars": ["레오"], "reps": ["Leo"]},
		"dots": {"chars": [".."], "reps": ["..."]},
		"pray식": {"chars": ["프레이식", "프레 이식"], "reps": ["pray style"]}
	}
	for group in subs:
		for char in subs[group]['chars']:
			for rep in subs[group]['reps']:
				if group == "regex": ret= re.sub(char, rep, ret)
				else: ret= ret.replace(char, rep)

	return ret

d= 0.5
def getTranslation(query, delay=0.5, headless=True, maxTries=20, verbose=True):
	if not query: return ""
	query= hotfix(query)

	cache= utils.loadJson(utils.PAPAGO_CACHE)
	if query in cache: return cache[query]
	else:
		global d
		d= delay

		driver= utils.initDriver(headless=headless)
		driver= loadPage(driver, query)
		time.sleep(delay)

		try: tl= retrievetl(driver, maxTries=maxTries)
		except FileNotFoundError: raise Exception("Could not retrieve translation for", query)

		cache= utils.loadJson(utils.PAPAGO_CACHE)
		cache[query]= tl
		utils.dumpJson(cache,utils.PAPAGO_CACHE)

		if verbose: print(query,"-->",tl)
		return tl



def loadPage(driver, query):
	base= "https://papago.naver.com/?sk=ko&tk=en&st="
	driver.get(base+query)
	return driver

def retrievetl(driver, maxTries=20):
	time.sleep(1)
	xpath= r'//*[@id="txtTarget"]'
	translation= driver.find_element_by_xpath(xpath).text

	count= 0
	while not translation:
		time.sleep(d)
		translation= driver.find_element_by_xpath(xpath).text

		count+=1
		if count > maxTries: raise FileNotFoundError

	driver.close()
	return translation
