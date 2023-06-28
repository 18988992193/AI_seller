# -*- coding: utf-8 -*-
"""
Created on Tue May 30 22:14:33 2023

@author: nick0
"""
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

# 加载BERT模型和tokenizer
tokenizer = BertTokenizer.from_pretrained('./mac_bert/')
model = BertModel.from_pretrained('./mac_bert')
model.eval()

def count_similarity(text1,text2):
    # 对文本进行tokenization和padding
    inputs = tokenizer([text1, text2], padding=True, truncation=True, return_tensors='pt')
    
    # 获取输入的token IDs和attention masks
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    
    # 使用BERT模型获取文本的嵌入向量
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    
    # 获取文本的嵌入向量
    embeddings = outputs[0][:, 0, :].numpy()
    
    # 计算文本之间的余弦相似度
    similarity = cosine_similarity(embeddings[0].reshape(1, -1), embeddings[1].reshape(1, -1))[0][0]
    
    # 打印文本相似度
    return similarity
