# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:22:05 2023

@author: Shutter Zor
@blog:   shutterzor.cn
@email:  Shutter_Z@outlook.com
"""

import os
import re
import pandas as pd

# 读入积极情绪词语，并赋值给变量posWords与negWords
with open('resources/posDict.txt', 'r', encoding='utf-8') as file:
    posWords = file.read().split('\n')

with open('resources/negDict.txt', 'r', encoding='utf-8') as file:
    negWords = file.read().split('\n')

# 将文件名称读入，并提取股票代码与年份
fileDF = pd.DataFrame(os.listdir('resources/files'))
fileDF.columns=['file']

for line in range(len(fileDF)):
    fileDF.loc[line, 'stkcd'] = re.findall('(\d+)\_', fileDF.loc[line, 'file'])[0]
    fileDF.loc[line, 'year']  = re.findall('\_(\d+)-', fileDF.loc[line, 'file'])[0]

# 计算对应文件中含有积极词语与消极词语的个数
for line in range(len(fileDF)):
    filePath = 'resources/files/' + fileDF.loc[line, 'file']
    with open(filePath, encoding='utf-8') as file:
        content = file.read()
    for posWord in posWords:
        fileDF.loc[line, posWord] = len(re.findall(posWord, content))
    for negWord in negWords:
        fileDF.loc[line, negWord] = len(re.findall(negWord, content))    
    
# 对积极情绪与消极情绪求和
fileDF.loc[:, 'posSentiment'] = fileDF.loc[:, posWords].sum(axis=1)
fileDF.loc[:, 'negSentiment'] = fileDF.loc[:, negWords].sum(axis=1)
fileDF = fileDF.loc[:,['stkcd', 'year', 'posSentiment', 'negSentiment']]
fileDF.to_csv('pySentimentResult.csv', index=False)


