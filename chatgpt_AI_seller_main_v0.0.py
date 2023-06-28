# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 11:28:54 2023

@author: nick0
"""
from AI_Seller import AI_Seller

def read_file(test_file_path):
    test = []
    with open(test_file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            test.append(line.strip())
    return test
def func_ai_seller(comment, Seller):
    data = {}
    answerOri, answerMatch, confidence = Seller.answer_question(comment)
    data['answerOri'], data['answerMatch'], data['confidence'] = answerOri, answerMatch, confidence
    if confidence > 0.9:
        data['type'] = 2 #正常qa
    else:
        data['type'] = 1 #非正常qa
    return data


if __name__ == '__main__':
    QA_file_path = './data/问答库_v1.1.xls'
    test_file_path = './data/test.txt'
    
    Seller = AI_Seller(QA_file_path)
    test = read_file(test_file_path)
    
    output = []
    test_output = [] #test
    for comment in test:
        out_dic = {}
        data = func_ai_seller(comment, Seller)
        print(f"\nQuestion:{comment}")
        print(f"ChatGPT(ori): {data['answerOri']}")
        if data['type'] == 2:
            print(f"ChatGPT(match): (similiarty:{data['confidence']:.2f}){data['answerMatch']}")
        else:
            print(f"ChatGPT(match): (similiarty:{data['confidence']:.2f})【非正常QA】")
        out_dic['data'] = data
        out_dic['code'] = 200
        out_dic['msg'] = ""
        output.append(out_dic)
        
        #test
        test_output.append(f"\nQuestion:{comment}")
        test_output.append(f"ChatGPT(ori): {data['answerOri']}")
        if data['type'] == 2:
            test_output.append(f"ChatGPT(match): (similiarty:{data['confidence']:.2f}){data['answerMatch']}")
        else:
            test_output.append(f"ChatGPT(match): (similiarty:{data['confidence']:.2f})【非正常QA】")
    #test        
    with open('./data/test_result.txt', 'w') as file:
        for line in test_output:
            file.write(line + '\n')