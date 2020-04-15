"""Utility file for convinient cleaning functions"""

def clean_white_spaces(list_of_symbols):
    """ Cleans white spaces give a list of strings

    @Params:
    list_of_symbols - a list of type strings

    @Returns:
    mList - a new list of type strings
    """
    mList = []
    for items in list_of_symbols:
        mList.append(items.strip().strip('\t').replace('\\t',''))
    return mList




