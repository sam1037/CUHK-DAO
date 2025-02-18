import pandas as pd
import re
import opencc

def extract_word(text):
    # Match Chinese characters before the parenthesis
    match = re.match(r'^([\u4e00-\u9fff]+)(?:（.*）)?', str(text))
    return match.group(1) if match else text.strip()

def load_common_words():
    commonWordDict = {}
    converter = opencc.OpenCC('s2t')

    # Read entire sheet
    df1 = pd.read_excel('HSK-2012.xls', sheet_name='HSK（一级）（150）', header=None)
    w1 = df1[0].apply(extract_word).tolist()
    for w in w1:
        traditional = converter.convert(w)
        commonWordDict[traditional] = 1


    df = pd.read_excel('HSK-2012.xls', sheet_name='HSK（二级）（300）', header=None)
    w2 = df[0].apply(extract_word).tolist()
    for w in w2:
        traditional = converter.convert(w)
        commonWordDict[traditional] = 2


    df = pd.read_excel('HSK-2012.xls', sheet_name='HSK（三级）（600）', header=None)
    w3 = df[0].apply(extract_word).tolist()
    for w in w3:
        traditional = converter.convert(w)
        commonWordDict[traditional] = 3

    df = pd.read_excel('HSK-2012.xls', sheet_name='新HSK（四级）（1200）', header=None)
    w4 = df[0].apply(extract_word).tolist()
    for w in w4:
        traditional = converter.convert(w)
        commonWordDict[traditional] = 4

    return commonWordDict
