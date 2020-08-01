import utils, re, time, os
from bs4 import BeautifulSoup as bs


def getSearchPage(query, driver):
	base= "https://en.dict.naver.com/#/search?query="
	driver.get(base + query)
	soup= bs(driver.page_source, 'html.parser')

	while len(soup.find(id='content').find_all("div")) == 0:
		time.sleep(.2)
		soup= bs(driver.page_source, 'html.parser')

	return soup

def clean(x):
	ret= re.sub(r"(\s+)", " ",  x).strip()
	return ret


def getPhrases(soup):
	ret= []
	words= soup.select('#searchPage_entry')
	if not words: return []

	y= words[0].find_all("div", class_="origin")
	for x in y:
		w= x.find('a')
		if w.find('sup'): w.find('sup').extract()
		w= clean(w.text.strip())

		h= x.find('span', lang='zh_CN')
		if h:
			h= clean(h.text)
			h= f" ({h})"
		else: h= ''

		m= x.parent.find_all(class_='mean')
		m= [clean(z.text) for z in m]


		kex= x.find(class_="example")
		eex= x.find(class_="translate")
		if kex:
			kex= clean(kex.text)
			eex= clean(eex.text)
			ex= {"korean": kex, "english": eex}
		else: ex= {}

		ret.append({
			"phrase": w,
			"hanja": h,
			"example": ex,
			"meanings": m
		})

	return ret

def getMeanings(soup):
	ret= []
	means= soup.select("#searchPage_mean > div")
	if not means: return []

	rows= means[0].find_all(class_="row")
	for r in rows:
		m= clean(r.find("a").text)
		freq= r.find("span", class_="unit_grade")

		if freq:
			tmp= freq.find("span")['class'][1]
			freq= int(re.search(r"(\d+)", tmp).group())
		else: freq= 0

		ret.append({
			"meaning": m,
			"frequency": freq
		})

	return ret

def getExV(soup):
	ret= []
	subs= soup.select("#searchPage_vlive")
	if not subs: return []


	rows= subs[0].find_all(class_="row")
	for r in rows:
		ko= r.find(class_="text", lang="ko")
		ko= clean(r.text) if ko else ""

		en= r.find("p", lang="en")
		en= clean(en.text.replace("듣기", "")) if en else ""

		ret.append({ "korean": ko, "english": en})

	return ret

def getEx(soup):
	ret= []
	exs= soup.select("#searchPage_example > div")
	if not exs: return []

	rows= exs[0].find_all(class_="row")
	for r in rows:
		ko= r.find(class_="text", lang="ko")
		ko= clean(r.text) if ko else ""

		en= r.find(lang="en")
		en= clean(en.text.replace("듣기", "")) if en else ""

		ret.append({ "korean": ko, "english": en})

	return ret


def search(query, online=True):
	query= re.sub(r"[^\w]","",query)
	if not query: query= ""

	outFile= utils.ENDIC_DIR + query + ".json"

	if os.path.exists(outFile):
		ret= utils.loadJson(outFile)
	elif online:
		driver= utils.initDriver()
		result= getSearchPage(query, driver)

		phrases= getPhrases(result)
		meanings= getMeanings(result)
		vlive= getExV(result)
		examples= getEx(result)

		driver.close()

		ret= {
			"phrases": phrases,
			"meanings": meanings,
			"vlive": vlive,
			"examples": examples
		}
		utils.dumpJson(ret, outFile)
		# print(query, ret)
	else:
		ret= { "phrases": [], "meanings": [], "vlive": [], "examples": [] }

	return ret

if __name__ == "__main__":
	result= search("살짝")