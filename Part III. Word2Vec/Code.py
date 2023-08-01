# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 18:51:13 2023

@author: Shutter Zor
@blog:   shutterzor.github.io
@email:  Shutter_Z@outlook.com
"""

import re
import jieba
import gensim


# 定义一个获取年报中所有汉字的函数
def get_chinese_character(Text, Remethod):
    FilterText = ""
    temp = re.findall(Remethod, Text)
    for i in range(len(temp)):
        FilterText += temp[i]
    return FilterText


# 引入停用词
with open("resources/stopwords.txt", 'r', encoding='utf-8') as stoptext:
    stopword = stoptext.read()
stopword_list = stopword.split('\n')

# 设置文本去停用词
def get_Text(OriginalText, StopWordsList):
    PureText = ''
    for word in OriginalText:
        if word not in StopWordsList:
            PureText += word
    WordList = jieba.lcut(PureText)
    return WordList


# 读入年报文件，按句号分句
with open("resources/files/湖北省-2022.txt", "r", encoding="utf-8") as file:
    text = get_chinese_character(file.read(), "[\u4e00-\u9fa5]+|。")
text_list = text.split("。")

# 对每一个句子去停用词
for i in range(len(text_list)):
    text_list[i] = get_Text(text_list[i], stopword_list)


# CBOW
model = gensim.models.Word2Vec(text_list, vector_size=200, window=30, min_count=3, sg=0)
model.wv.most_similar("武汉", topn=10)

# Skip-Gram
model = gensim.models.Word2Vec(text_list, vector_size=200, window=30, min_count=3, sg=1)
model.wv.most_similar("湖北", topn=10)




