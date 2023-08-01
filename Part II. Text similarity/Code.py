# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:55:23 2023

@author: Shutter Zor
@blog:   shutterzor.cn
@email:  Shutter_Z@outlook.com
"""

import os
import re
import jieba
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 读入相关文件信息
fileDF = pd.DataFrame(os.listdir('resources/files'))
fileDF.columns=['file']

# 补充dataframe的其他数据信息
for line in range(len(fileDF)):
    fileDF.loc[line, 'province'] = re.findall('(.*)-', fileDF.loc[line, 'file'])[0]
    fileDF.loc[line, 'year']     = re.findall('-(\d+)', fileDF.loc[line, 'file'])[0]
    with open('resources/files/'+fileDF.loc[line, 'file'], encoding='utf-8') as file:
        fileDF.loc[line, 'content'] = file.read()

# 仅保留汉字
for line in range(len(fileDF)):
    contentText = ''
    tempText    = re.findall('[\u4e00-\u9fa5]+', fileDF.loc[line, 'content'])
    for idx in range(len(tempText)):
        contentText += tempText[idx]
    fileDF.loc[line, 'content'] = contentText

# 去除停用词
with open('resources/stopwords.txt', encoding='utf-8') as file:
    stopWordList = file.read().split('\n')

fileDF['content'] = fileDF['content'].apply(lambda x: jieba.lcut(x))

for line in range(len(fileDF)):
    content_list = fileDF.loc[line, 'content']
    # 使用列表推导式过滤掉不在 stopWordList 中的单词
    filtered_content = [word for word in content_list if word not in stopWordList]
    # 将过滤后的单词用空格拼接成单个字符串
    new_content = ' '.join(filtered_content)
    # 将新的内容赋值回 'content' 列
    fileDF.loc[line, 'content'] = new_content
    
vectorizer = CountVectorizer(binary=True)
X = vectorizer.fit_transform(list(fileDF.loc[:,'content']))
meanVec = np.average(X.toarray(), axis=0)
meanVecNew = meanVec.reshape(1,-1)
CS1 = cosine_similarity(X, meanVecNew)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(list(fileDF.loc[:,'content']))
meanVec = np.average(X.toarray(), axis=0)
meanVecNew = meanVec.reshape(1,-1)
CS2 = cosine_similarity(X, meanVecNew)

transformer = TfidfTransformer()
X = vectorizer.fit_transform(list(fileDF.loc[:,'content']))
tfidf = transformer.fit_transform(X)
meanVec = np.average(tfidf.toarray(), axis=0)
meanVecNew = meanVec.reshape(1,-1)
CS3 = cosine_similarity(tfidf, meanVecNew)








