import copy

# Un-tokenize the OCR data
def stitch_words(bubble_data):
	lines= _stitch_y(bubble_data)
	words= _stitch_x(lines)
	return words

# Group the data by line
def _stitch_y(bubble_data):
	data= copy.deepcopy(bubble_data)
	lines= []

	while data:
		start_word= data.pop(0)
		start_bounds= _get_y_bounds(start_word[1])

		# Get words whose vertical-centers overlap.
		inds= []
		for i in range(len(data)):
			bnds= _get_y_bounds(data[i][1])
			overlap= _get_overlap(start_bounds, bnds)

			if overlap > 0:
				inds.append(i)

		lines.append([start_word] + [data[i] for i in inds])
		for i in reversed(inds): data.pop(i)

	return lines

def _stitch_x(line_data, factor=7):
	data= copy.deepcopy(line_data)
	words= []

	for line_data in data:
		# Loop through line to find connected words
		while line_data:
			start_char= line_data[0]
			start_bounds= _get_x_bounds(line_data[0][1])

			inds= [0]
			for i in range(1,len(line_data)):
				chr_bounds= _get_x_bounds(line_data[i][1])

				# Count as connected if the horizontal distance between the two intervals is at most the height // factor
				if _get_overlap(start_bounds, chr_bounds) > -start_char[1]['h']//factor:
					start_char= line_data[i]
					start_bounds= _get_x_bounds(line_data[i][1])

					inds.append(i)
				else: break

			tmp= [line_data[i][1] for i in inds]
			w= ''.join([line_data[i][0] for i in inds])
			for i in reversed(inds): line_data.pop(i)

			words.append([w, get_bbox(tmp)])

	return words

# Generate new bbox containing all bbox's in a list
def get_bbox(bbox_data):
	ret= dict(x=0,y=0,w=0,h=0)

	ret['x']= min([x['x'] for x in bbox_data] + [x['x'] + x['w'] for x in bbox_data])
	ret['y']= min([x['y'] for x in bbox_data] + [x['y'] + x['h'] for x in bbox_data])

	ret['w']= -ret['x'] + max([x['x'] for x in bbox_data] + [x['x'] + x['w'] for x in bbox_data])
	ret['y']= -ret['y'] + max([x['y'] for x in bbox_data] + [x['y'] + x['h'] for x in bbox_data])

	return ret

# Get bounds of vertical center
def _get_y_bounds(bbox, factor=2):
	half= factor * 2
	tmp= bbox['h']//half

	center= bbox['y'] + bbox['h']//factor
	bounds= [center-tmp, center+tmp]
	bounds.sort()

	return bounds

# Get bounds of horizontal center
def _get_x_bounds(bbox, factor=1):
	bounds= [bbox['x'], bbox['x']+bbox['w']]
	bounds.sort()

	return bounds

# Get overlap of two intervals
def _get_overlap(itvl_a, itvl_b):
	y= min(itvl_a[1], itvl_b[1])
	x= max(itvl_a[0], itvl_b[0])

	return y-x



if __name__ == "__main__":
	import json

	test_data= [
		['각', {'x': 410, 'y': 188, 'w': 15, 'h': 14}]		,
		['기지', {'x': 440, 'y': 185, 'w': 24, 'h': 19}]		,
		['에', {'x': 465, 'y': 185, 'w': 12, 'h': 19}]		,
		['기술', {'x': 488, 'y': 185, 'w': 33, 'h': 19}]		,
		['지원', {'x': 522, 'y': 185, 'w': 34, 'h': 19}]		,
		['과', {'x': 557, 'y': 185, 'w': 8, 'h': 19}]		,
		['동시에', {'x': 410, 'y': 207, 'w': 46, 'h': 14}]	,
		['심은', {'x': 465, 'y': 207, 'w': 32, 'h': 14}]		,
		['워프', {'x': 502, 'y': 204, 'w': 37, 'h': 19}]		,
		['마커', {'x': 540, 'y': 204, 'w': 28, 'h': 19}]		,
		['.', {'x': 571, 'y': 218, 'w': 2, 'h': 2}]			,

	]

	answer_key= """
	각 기지에 기술지원과
	동시에 심은 워프머커.
	"""
	print([x[0] for x in stitch_words(test_data)])
