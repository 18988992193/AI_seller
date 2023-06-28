# -*- coding: utf-8 -*-
"""
Created on Sun May 28 22:50:14 2023

@author: nick0
"""

import os
import openai
from count_sim import count_similarity
openai.api_key = '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'


import xlrd

# 打开文件
workbook = xlrd.open_workbook('问答库_v1.1.xls')

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

output.append('当我问到身高体重相关时，你回答“姐姐，直接点进去下单，选尺码的位置都有备注建议的体重，您根据这个体重建议来拍就行哦。”')
output.append('你只能按照规则回答，不允许擅自回答多余的字符。')
output2 = '\n'.join(output)

def match(string, answers):
    answers = list(answers)
    sims = []
    for i in answers:
        sims.append(round(count_similarity(string,i),4))
    return answers[sims.index(max(sims))], max(sims)



messages = [
 {"role": "system", "content" : output2}
]
'''
#content = input("User: ")
messages.append({"role": "system", "content": output2})

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages,
  
)

chat_response = completion.choices[0].message.content
messages.append({"role": "assistant", "content": chat_response})
'''


while True:
    content = input("User: ")
    messages.append({"role": "system", "content": content})#role为system无上下文，user开启上下文
    
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      temperature = 0,
      messages=messages,
      #system={"interrupt": True}  # 关闭上下文关联
    )

    chat_response = completion.choices[0].message.content
    match_content = match(chat_response, answers)
    print(f'ChatGPT(ori): {chat_response}')
    if match_content[1] > 0.9:
        print(f'ChatGPT(match): (similiarty:{match_content[1]:.2f}){match_content[0]}')
    else:
        print(f'ChatGPT(match): (similiarty:{match_content[1]:.2f})听不懂您在说什么')
    #关闭上下文关联
    messages.append({"role": "assistant", "content": chat_response})
    messages.append({"role": "system", "content": '你只能按照规则回答，不允许擅自回答多余的字符。'})