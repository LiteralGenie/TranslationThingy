import glob, utils.page_utils

glob_dir = r"C:\scans\Knight Run\225\wr*.png"
chap_num= 225

im_path= glob.glob(glob_dir)[0]
page= utils.page_utils.Page(page_num=1, im_path=im_path, series="knight", chap_num=225).load_bubbles()

def get_y_bounds(bbox, factor=2):
    half= factor * 2
    tmp= bbox['h']//half

    center= bbox['y'] + bbox['h']//factor
    bounds= [center-tmp, center+tmp]
    bounds.sort()

    return bounds

def get_x_bounds(bbox, factor=1):
    bounds= [bbox['x'], bbox['x']+bbox['w']]
    bounds.sort()

    return bounds

def get_overlap(itvl_a, itvl_b):
    y= min(itvl_a[1], itvl_b[1])
    x= max(itvl_a[0], itvl_b[0])

    return y-x


for bubble in page.bubbles:
    print(bubble)
    # for word in bubble.word_data:
    #     print("\t",word)
    # print()

    data= bubble.word_data
    lines= []

    while data:
        start_word= data.pop(0)
        start_bounds= get_y_bounds(start_word[1])

        inds= []
        for i in range(len(data)):
            w_bounds= get_y_bounds(data[i][1])

            if get_overlap(w_bounds, start_bounds) > 0:
                inds.append(i)

        lines.append([start_word] + [data[i] for i in inds])
        [data.pop(i) for i in reversed(inds)]

        # print(f"\tfound line {' '.join([x[0] for x in lines[-1]])}")





    # print()
    words= []
    for l in lines:
        while l:
            start_char= l[0]
            start_bounds= get_x_bounds(start_char[1])

            inds= []
            for i in range(len(l)):
                chr_bounds= get_x_bounds(l[i][1])
                if get_overlap(start_bounds, chr_bounds) >= -start_char[1]['h']//7:
                    start_char= l[i]
                    start_bounds= chr_bounds
                    inds.append(i)
                else: break

            words.append([l[i][0] for i in inds])
            [l.pop(i) for i in reversed(inds)]

            # print(f"\tfound word {''.join(words[-1])}")

    print(' '.join([x for x in [''.join(y) for y in words]]))
    print()