from konlpy.tag import Kkma
from konlpy.utils import pprint
import json

kkma_cats= json.load(open(r"C:\Programming\KnightRunReader\scratch\tokenizer\kkma_groups.json", encoding='utf-8'))['types']
def get_kkma_cat(type_dict, cat):
	for x in type_dict:
		if cat.lower() in type_dict[x]['abbreviations_kkma']:
			return x

	raise ValueError(f"'{cat}' category (kkma) not found")


sentence= r"부서진 푸른꽃을 찾아다니며 코어와 몸체를 융합시키는 개체가 나오다니..."
sentence= r"레오... 뽑지 마"

for x in Kkma().pos(sentence):
	print(x[0].ljust(5), get_kkma_cat(kkma_cats, x[1]))