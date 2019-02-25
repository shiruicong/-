# coding = utf-8

import math
import json
import operator
from collections import Counter
from utils import load_data

class BM25 :
    '''
    BM25模型
    '''
    def __init__(self, k1 = 2, k3 = 1, b = 0.75, N = 241006, avg_l = 300):
        '''
        BM25模型超参数

        Args:
            b float BM25模型中的b
            k1 int BM25模型中的k1
            k3 int BM25模型中的k3
            N int 文档数
            avg_l int 平均文档长度
        '''
        self.b = b
        self.k1 = k1
        self.k3 = k3
        self.N = N
        self.avg_l = avg_l

    def build(self, file):
        '''
        导入倒排表

        Args:
            file str 倒排表路径
        '''
        self.invert_index_table = json.loads(load_data(file))

    def get_query(self, field_dict):
        '''
        获取查询词及其对应的相近词，构成新的查询

        Args:
            field_dict dict 对应字段的查询词及其相近词
        Returns:
            query_list list 查询
        '''
        query_list = []
        for k, v in field_dict.items():
            query_list.append(k)
            query_list.extend(v)
        return query_list

    def query(self, word_group, k):
        '''
        根据BM25模型计算得分并排序

        Args:
            word_group list 查询词
            weight_group list 查询词的权重
            k int 返回前k个
        Returns
            (res_doc[:k], res_score[:k]) list 查询文档id和得分
        '''
        weight = 0
        for i in range(4):
            for _, value in word_group[i].items():
                weight += len(value) 
        if weight < 5:
            weight = 5
    
        # 获取查询
        disease_query_dict = word_group[0]
        gene_query_dict = word_group[1]
        demographic_query_dict = word_group[2]
        other_query_dict = word_group[3]
        query_list = []
        query_list.extend(self.get_query(disease_query_dict))
        query_list.extend(self.get_query(gene_query_dict))
        query_list.extend(self.get_query(demographic_query_dict))
        query_list.extend(self.get_query(other_query_dict))
        # 查询中词与词频字典
        qtf_dict = dict(Counter(query_list))
        # 结果集合
        res = {}
        # 倒排表（第0个元素：文档id，第1个元素：文档词频，第2个元素：文档长度）
        table = self.invert_index_table
        for i, word_dict in enumerate(word_group):
            word_list = self.get_query(word_dict)
            for word in word_list:
                if word in table:
                    # 查询中词频
                    qtf = float(qtf_dict[word])
                    # 文档集（id）
                    doc_group = table[word]
                    # 文档频率
                    df = float(len(doc_group))
                    for item in doc_group:
                        id_tf_ld = item.split()
                        Doc_id = id_tf_ld[0]
                        tf = float(id_tf_ld[1])
                        # 文档长度
                        ld = float(id_tf_ld[2])
                        score = qtf / (self.k3 + qtf) * (self.k1 + tf) / (tf + self.k1 * (1 - self.b + self.b * ld / self.avg_l)) * math.log2((self.N - df + 0.5) / (df + 0.5))
                        if word in word_dict.keys():
                            if Doc_id not in res:
                                res[Doc_id] = score * (weight - i)
                            else:
                                res[Doc_id] += score * (weight - i)
                        else:
                            if Doc_id not in res:
                                res[Doc_id] = score * 0.9
                            else:
                                res[Doc_id] += score * 0.9
        # 排序
        res = sorted(res.items(), key=operator.itemgetter(1))
        res.reverse()
        res_doc = ["NCT0" + num[0] for num in res]
        res_score = [num[1] for num in res]
        return (res_doc[:k], res_score[:k])

if __name__ == '__main__':
    bm_model = BM25(k1 = 2, k3 = 1, b = 0.75, N = 241006, avg_l = 300)
    bm_model.build("./clinicallevel_cleaned_txt.json")
    res = bm_model.query(["Liposarcoma","CDK4","Amplification","38-year-old","male","GERD"], 5)
