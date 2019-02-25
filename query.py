# coding = utf-8

from word2vec import load_model
from utils import pickle_load, clean_data, xml_parse, preprocess

def demographic_split(demographic_field):
    '''
    人口信息字段有特殊格式

    Args:
        demographic_field str demographic字段
    Returns:
        demographic_list list 切分后的demographic字段
    '''
    # 人口信息有特殊格式
    demographic_list = demographic_field.split(' ')
    age = demographic_list[0]
    age_list = age.split('-')
    sex = demographic_list[1]
    demographic_list = []
    demographic_list.extend(age_list)
    demographic_list.append(sex)
    return demographic_list

def query_extension(field_list, w2v_model, vocab, k):
    '''
    查询扩展
    
    Args:
        field_list list 相应字段的列表
        w2v_model bin 词向量模型
        vocab list 词典
        k int 前k个相近词
    Returns:
        query_dict dict 扩展后的查询字典（键为查询词，值为相近词）
    '''
    query_dict = {}
    for query in field_list:
        if query not in query_dict.keys():
            query_dict[query] = []
        if query not in vocab:
            continue
        sim_word_list = w2v_model.wv.most_similar_cosmul(query, topn = k)
        extend_list = [word for word, _ in sim_word_list]
        query_dict[query] = clean_data(extend_list)
    return query_dict

def build_query(data_path, w2v_path, vocab_path, k):
    '''
    构建查询
    
    Args:
        data_path str 查询文件路径
        model_path str 词向量模型路径
        vocab_path str 词典路径
        k int 返回前k个相近词
    Returns:
        query_list list 已扩展的查询列表
    '''
    # 载入词向量模型，词典模型
    w2v_model = load_model(w2v_path)
    vocab = pickle_load(vocab_path)
    query_list = []
    # 解析xml文档
    qurey_dict = {'disease' : [], 'gene' : [], 'demographic' : [], 'other' : []}
    query_dict = xml_parse(data_path, qurey_dict, 1)
    disease_field_list = query_dict['disease']
    gene_field_list = query_dict['gene']
    demographic_field_list = query_dict['demographic']
    other_field_list = query_dict['other']
    del query_dict
    # 遍历查询
    for i in range(len(disease_field_list)):
        query_tmp_list = []
        # 获取一条查询的查询词
        disease_field_list[i] = preprocess(disease_field_list[i])
        disease_list = disease_field_list[i].split(' ')
        gene_field_list[i] = preprocess(gene_field_list[i])
        gene_list = gene_field_list[i].split(' ')
        other_list = preprocess(other_field_list[i])
        other_list = other_field_list[i].split(' ')
        demographic_list = demographic_split(demographic_field_list[i])
        # 对原始查询进行词性还原与去停用词操作
        disease_clean_list = clean_data(disease_list)
        gene_clean_list = clean_data(gene_list)
        demographic_clean_list = clean_data(demographic_list)
        other_clean_list = clean_data(other_list)
        # 查询扩展(含词干还原和去停用词操作)
        query_tmp_list.append(query_extension(disease_clean_list, w2v_model, vocab, k))
        query_tmp_list.append(query_extension(gene_clean_list, w2v_model, vocab, k))
        query_tmp_list.append(query_extension(other_clean_list, w2v_model, vocab, k))
        tmp_dict = {}
        for tmp in demographic_clean_list:
            tmp_dict[tmp] = []
        query_tmp_list.append(tmp_dict)
        query_list.append(query_tmp_list)
    return query_list

def start_query(bm, query_list, k):
    '''
    开始查询

    Args:
        bm cls bm25模型
        query_list list 全部查询
        k int 返回前k个文档
    Returns:
        res list 查询结果
    '''
    res = []
    for query_tmp_list in query_list:
        res_tmp = bm.query(query_tmp_list, k)
        res.append(res_tmp)
    return res