# -*- coding: utf-8 -*-
"""
Created on Sun May 28 22:50:14 2023

@author: nick0
"""

import os
import openai
import xlrd
import random
from transformers import logging
from count_sim import count_similarity
logging.set_verbosity_warning()


class AI_Seller:
    def __init__(self, QA_file_path):
        self.api_key_list = [
            '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', 
            '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',
            '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',
            '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',
            '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',
            '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',
            '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',
            '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']
        self.QA_file_path = QA_file_path
        self.unnormal_QA = '“【非正常QA】”'
        self.review_sent = f'你只能按照规则回答其中一句话，不允许擅自回答多余的字符。若问题中没有出现关键词，则回复“{self.unnormal_QA}”'
        
        
        # 打开文件
        workbook = xlrd.open_workbook(self.QA_file_path)
        
        # 获取所有sheet
        sheets = workbook.sheet_names()
        
        # 遍历所有sheet
        output = []
        output.append('从现在开始角色扮演一个销售，但需要遵守以下规则：')
        self.answers = set()
        for i in range(len(sheets)):
            sheet = workbook.sheet_by_index(i)
        
            # 遍历当前sheet中的所有行
            for j in range(1,sheet.nrows):
                row_values = sheet.row_values(j)
                ans = str(row_values[2]) if str(row_values[2]) else ans
                self.answers.add(ans)
        
                # 将第二列和第三列中的字符串拼接
                new_value = f"当我问到包含关键词“{str(row_values[1])}”时，你回答“{ans}”"
        
                # 输出结果
                output.append(new_value)
        
        output.append(self.review_sent)
        self.output2 = '\n'.join(output)

    def match(self, string, answers):
        answers = list(answers)
        sims = []
        for i in answers:
            sims.append(round(count_similarity(string,i),4))
        return answers[sims.index(max(sims))], max(sims)


    def answer_question(self, content):
        openai.api_key = random.choice(self.api_key_list)
        self.messages = [{"role": "system", "content" : self.output2}]
        self.messages.append({"role": "system", "content": content})#role为system无上下文，user开启上下文
        
        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          temperature = 0,
          messages=self.messages,
          #system={"interrupt": True}  # 关闭上下文关联
        )
    
        chat_response = completion.choices[0].message.content
        match_content = self.match(chat_response, self.answers)
        '''
        print(f'ChatGPT(ori): {chat_response}')
        if match_content[1] > 0.9:
            print(f'ChatGPT(match): (similiarty:{match_content[1]:.2f}){match_content[0]}')
        else:
            print(f'ChatGPT(match): (similiarty:{match_content[1]:.2f})听不懂您在说什么')
        '''
        #关闭上下文关联
        self.messages.append({"role": "assistant", "content": chat_response})
        self.messages.append({"role": "system", "content": self.review_sent})
        return chat_response, match_content[0], round(match_content[1],2)