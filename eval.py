#coding:utf-8
import numpy as np
import argparse

def eval(outputs = None, article = None, filename = None, dup_valid = False):
    """
    :param outputs:  存放结果的字典，dict[文章] = [tag1，tag2]
    :param article:  文章路径，若不提供，则默认当前文件夹下的 易车文章-1000-out.txt
    :param filename: 存放结果的txt文件，文件格式：文章 tag1，tag2
    :param dup_valid: 如果False，则多个重复标签只算一个正确
    :return: 召回和精度
    """
    assert outputs or filename, 'Please offer outputs or filename including outputs!'
    if filename:
        outputs = {}
        with open(filename,'r') as f:
            files = f.readlines()
        for line in files:
            line = line.strip().split(' ')
            outputs[line[0]] = line[1].split(',')

    if not isinstance(outputs, dict):
        raise ValueError('outputs is not a dict!')

    labels = read_true_output(article)

    predict_true = 0
    predict_false = 0
    total = 0
    for article in outputs.keys():
        true_output = np.zeros(len(labels[article]))
        total += len(labels[article])
        # 给预测结果去重
        if dup_valid:
            outputs[article] = list(set(outputs[article]))
            
        for i,label in enumerate(labels[article]):
            for predict in outputs[article]:
                if label == predict:
                    true_output[i] = 1
                    break
        predict_true += np.sum(true_output)
        predict_false = predict_false + (len(outputs[article]) - np.sum(true_output))

    recall = predict_true/total
    precise = predict_true/(predict_true + predict_false)
    print("Recall is {}, and Precise is {}".format(recall, precise))


def read_true_output(article = None):
    """
    :param article: 文章路径，若不提供，则默认当前文件夹下的 易车文章-1000-out.txt
    :return:
    """
    filename = '易车文章-1000-out.txt'
    if article:
        filename = article

    with open(filename, 'r') as f:
        files = f.readlines()

    print(len(files))
    label = {}
    for line in files:
        line = line.split('&&ArticleTag&&')
        tmp = ''.join(line[5].split(','))
        label[line[0]] = []
        if len(tmp) % 4 == 0 and len(line[5].split(',')[0]) != 4:
            for x in range(len(tmp)//4):
                if int(tmp[x*4:x*4+4]) > 0:
                    label[line[0]].append(tmp[x*4:x*4+4])
            if len(label[line[0]]) == 0:
                label[line[0]].append('0')
        else:
            for tmp in line[5].split(','):
                if int(tmp) > 0:
                    label[line[0]].append(tmp)
            if len(label[line[0]]) == 0:
                label[line[0]].append('0')
        label[line[0]] = list(set(label[line[0]]))

    return label

if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument('--filename', type = str, help='标签结果文件的路径')
    parse.add_argument('--article', default='易车文章-1000-out.txt',
                       type = str, help='标签结果文件的路径, 默认文件名：易车文章-1000-out.txt， 易车自媒体文章-1000-out.txt')
    arg = parse.parse_args()
    eval(filename = arg.filename, article=arg.article)

