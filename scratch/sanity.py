import glob, utils.page_utils

glob_dir = r"C:\scans\Knight Run\225\wr*.png"
chap_num= 225

im_path= glob.glob(glob_dir)[0]
page= utils.page_utils.Page(page_num=1, im_path=im_path, series="knight", chap_num=225).load_bubbles()

for bubble in page.bubbles:
    print(bubble)
    for word in bubble.word_data:
        print("\t",word)
    print()

    data= bubble.word_data
    lines= []

