#coding:utf-8
import os
import numpy as np
import eval
import argparse

def read_article_test(article = None):

    labels = eval.read_true_output(article)
    print(len(labels))
    for key in labels.keys():
        for tag in labels[key]:
            try:
                int(tag)
            except:
                print('article {} has invalid tag {}'.format(key, tag))
            if len(tag) != 4:
                print('article {} has invalid tag {}'.format(key, tag))
        if len(labels[key]) != len(set(labels[key])):
            print('article {} has duplicate tag'.format(key))
        if len(labels[key]) > 1:
            print(labels[key], key)
        if len(labels[key]) == 1 and labels[key] == ['0']:
            print(key)

if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument('--filename', type = str, help='标签结果文件的路径')
    parse.add_argument('--article', default='易车文章--1000-out.txt',
                       type = str, help='标签结果文件的路径, 默认文件名：易车文章--1000-out.txt， 易车自媒体文章-1000-out.txt')
    arg = parse.parse_args()
    read_article_test(arg.article)

