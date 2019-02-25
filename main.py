# coding = utf-8

from query import build_query, start_query
from word2vec import load_model
from bm25 import BM25
import os
import time
from utils import get_doc_cont, eval_res, save_data

'''
query_path str 查询文件路径
w2v_path str 词向量路径
vocab_path str 词典文件
invert_table_path str 倒排表路径
doc_path str 文档路径
res_path str 结果存储路径
eval_path str 评估结果存储路径
trec_eval_path str trec_eval路径
'''
query_path = './topic.xml'
w2v_path = './data/w2v/w2v.model'
vocab_path = './data/w2v/vocab.pkl'
invert_table_path = './data/invert_table/clinicaltrials.json'
doc_path = './data/clinicaltrials_xml'
res_doc_path = './res'
trec_eval_path = './trec_eval/trec_eval'
res_path = './eval/res.txt'
qrels_path = './eval/qrels.txt'
eval_path = './eval/eval.txt'

# 返回的相关词个数
k1 = 5
k2 = 15

if __name__ == '__main__':
    start = time.time()
    print('开始执行')
    # 构建查询
    print('根据文件' + query_path + '构建查询并作查询扩展')
    query_list = build_query(query_path, w2v_path, vocab_path, k1)
    print('构建查询完毕')
    # bm模型
    print("构建BM25模型")
    bm = BM25()
    print('构建BM25模型完毕')
    # 导入倒排表
    print('从' + invert_table_path + '处导入倒排表')
    bm.build(invert_table_path)
    print('导入完毕')
    # 查询
    print("开始查询")
    res = start_query(bm, query_list, k2)
    print('存储查询结果到目录' + res_doc_path)
    get_doc_cont(res, res_doc_path, doc_path)
    # 计算p@10
    print('存储评估所需文件至' + res_path)
    eval_res(res, res_path)
    # 测试
    print("开始评估结果")
    cmd = trec_eval_path + ' ' + qrels_path + ' ' + res_path

    eval_data = os.popen(cmd).read()
    print('评估结果为')
    print(eval_data)
    print('存储评估结果至' + eval_path)
    save_data(eval_path, eval_data)
    # 获取查询文档的文本内容
    end = time.time()
    print('用时%.4f' % (end - start))
