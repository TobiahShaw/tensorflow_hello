"""
author:TobiahShaw
date:2019-06-24
util function
"""
import os

def get_item_info(input_file):
    """
    get item info [title, genre]
    Args:
        input_file: item info file
    Return:
        a dict key : itemId, value: [title, genre]
    """
    if not os.path.exists(input_file):
        return {}

    item_info = {}
    
    fp = open(input_file)

    linenum = 0
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        elif len(item) == 3:
            itemId, title, genre = item[0], item[1], item[2]
        else:
            itemId = item[0]
            genre = item[-1]
            title = ",".join(item[1:-1])
        item_info[itemId] = [title, genre]
    fp.close()
    return item_info;