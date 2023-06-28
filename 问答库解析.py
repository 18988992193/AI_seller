# -*- coding: utf-8 -*-
"""
Created on Sun May  1 00:13:00 2022

@author: nick0
"""
import xlrd

# 打开文件
workbook = xlrd.open_workbook('问答库(1).xls')

# 获取所有sheet
sheets = workbook.sheet_names()

# 遍历所有sheet
output = []
output.append('从现在开始角色扮演一个销售，但需要遵守以下规则：')
answers = set()
for i in range(len(sheets)):
    sheet = workbook.sheet_by_index(i)

    # 遍历当前sheet中的所有行
    for j in range(1,sheet.nrows):
        row_values = sheet.row_values(j)
        ans = str(row_values[2]) if str(row_values[2]) else ans
        answers.add(ans)

        # 将第二列和第三列中的字符串拼接
        new_value = f"当我问到包含关键词“{str(row_values[1])}”时，你回答“{ans}”"

        # 输出结果
        output.append(new_value)

output.append('你只能按照规则回答，不允许回答多余的字符。若问题中不包含关键字，则回答“土豪在说啥听不懂”，等我开始询问你再开始回答')
with open('问答库解析.txt', 'w') as f:
    for item in output:
        f.write(item+"\n")