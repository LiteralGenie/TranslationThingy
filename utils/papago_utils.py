import utils,time,re
from selenium.common.exceptions import NoSuchElementException as NoSuchElementException
from bs4 import BeautifulSoup as bs

# remove invalid characters
def hotfix(text):
	ret= text
	subs= {
		"regex": { "chars": [r"[^ a-zA-Z0-9\u3131-\u3163\uac00-\ud7a3.?,!:$*&]"], "reps": [""] },
		"order": {"chars": ["기사단"], "reps": ["Knight Order"]},
		"knight": {"chars": ["기사"], "reps": ["Knight"]},
		"leo": {"chars": ["레오"], "reps": ["Leo"]},
		# "dots": {"chars": [".."], "reps": ["..."]},
		"pray식": {"chars": ["프레이식", "프레 이식"], "reps": ["pray style"]},
		"bad": {"chars": ["|","&"], "reps": [""]}
	}
	for group in subs:
		for char in subs[group]['chars']:
			for rep in subs[group]['reps']:
				if group == "regex": ret= re.sub(char, rep, ret)
				else: ret= ret.replace(char, rep)

	ret= ret.strip()
	return ret

# get papago translation (from cache if possible)
def getTranslation(text, delay=0.5, headless=True, maxTries=20, verbose=True):
	if not text: return ""
	query= hotfix(text)
	if not query:
		print(f"EmptyError: {text} --> {query}")
		return ""

	cache= utils.loadJson(utils.PAPAGO_CACHE)
	if query in cache:
		return cache[query]
	else:
		driver= utils.initDriver(headless=headless)
		driver= loadPage(driver, query)
		time.sleep(delay)

		try: tl= retrievetl(driver, maxTries=maxTries, delay=delay)
		except FileNotFoundError: raise Exception("Could not retrieve translation for", query)

		cache= utils.loadJson(utils.PAPAGO_CACHE)
		cache[query]= tl
		utils.dumpJson(cache,utils.PAPAGO_CACHE)

		if verbose: print(query,"-->",tl)
		return tl

# visit translation page
def loadPage(driver, query):
	base= "https://papago.naver.com/?sk=ko&tk=en&st="
	driver.get(base+query)
	return driver

# retrieve translation
def retrievetl(driver, maxTries=20, delay=1):
	time.sleep(1)
	translation= driver.find_element_by_id('txtTarget').text

	count= 0
	while not translation:
		time.sleep(delay)
		translation= driver.find_element_by_id('txtTarget').text

		count+=1
		if count > maxTries: raise FileNotFoundError

	driver.close()
	return translation
