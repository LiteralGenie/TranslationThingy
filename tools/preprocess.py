import utils.endic_utils as endic, utils.papago_utils as translator
from utils.ocr_utils import gapi as api
from requests.exceptions import HTTPError
import glob, os, sys

seriesDir= r"C:\scans\Knight Run/"
chapDir= list([str(x) for x in range(165,166)])
# chapDir= ["213"]

for chapNum in chapDir:
	wordCount= 0

	for i,imPath in enumerate(glob.glob(seriesDir + chapNum + "/wr*.png")):
		pageNum= i+1
		print(chapNum, os.path.basename(imPath))

		try:
			ocr= api.ocr(imPath, name=f"knight_{chapNum}-{pageNum}")
		except HTTPError as e:
			# likely empty image
			print("\tWARNING: ocr fail", imPath, file=sys.stderr)
			continue

		for bubble, _ in ocr:
			for word,__ in bubble:
				pass # search= endic.search(word)

			block= " ".join([x[0] for x in bubble])
			print(f"\t{block}")

			wordCount+= len([x[0] for x in bubble])

			translator.getTranslation(block, delay=2, headless=True, maxTries=10)

	print(f"[{chapNum}] Word Count: {wordCount}\n")