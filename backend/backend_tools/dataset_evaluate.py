import itertools
from collections import OrderedDict
from os.path import basename

import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd

from backend_tools.global_functions import *


class Evaluator:
    CMmap = ['Ground Truth', 'Algorithm']
    result = {}

    def __init__(self, gt_data_set, algo_data_set):
        self.GTDataSet = gt_data_set['images']
        self.AlgoDataSet = algo_data_set['images']
        self.result['ground_truth'] = []
        self.result['algorithm'] = []
        self.y_gt = []
        self.y_algo = []
        self.imgMap = OrderedDict()
        self.images = []
        self.GTImgDirname = ''
        self.AlgoImgDirname = ''
        self.gTags = set()
        self.algoTags = set()
        self.CM = OrderedDict()
        self.cmTabel = None
        self.build_tags()
        self.check_tags()
        # self.df = pd.DataFrame()

    def build_tags(self):
        for sub_ds in self.GTDataSet:
            for tag in sub_ds['tags']:
                self.gTags.add(tag['label'])
        for sub_ds in self.AlgoDataSet:
            for tag in sub_ds['tags']:
                self.algoTags.add(tag['label'])

    def check_tags(self):
        if len(self.gTags) != len(self.algoTags):
            raise ValueError('Algorithm data set doesn\'t have the same labels as GT')
        for tag in self.algoTags:
            if tag not in self.gTags:
                raise ValueError('Algorithm data set doesn\'t have the same labels as GT')

    def build_results(self):
        for sub_gt_ds in self.GTDataSet:
            if not self.GTImgDirname:
                self.GTImgDirname = dirname(sub_gt_ds['uri'][0])
            for tag_set in sub_gt_ds['tags']:
                if tag_set['checked']:
                    # TODO: if there is more then one image, change the indexing ([0]) to for loop
                    self.result['ground_truth'].append({sub_gt_ds['uri'][0]: tag_set['label']})
                    self.images.append(sub_gt_ds['uri'][0])
                    if basename(sub_gt_ds['uri'][0]) in self.imgMap:
                        self.imgMap[basename(sub_gt_ds['uri'][0])].append(tag_set['label'])
                    else:
                        self.imgMap[basename(sub_gt_ds['uri'][0])] = [tag_set['label']]
        for sub_algo_ds in self.AlgoDataSet:
            if not self.AlgoImgDirname:
                self.AlgoImgDirname = dirname(sub_algo_ds['uri'][0])
            for tag_set in sub_algo_ds['tags']:
                if tag_set['checked']:
                    # TODO: if there is more then one image, change the indexing ([0]) to for loop
                    self.result['algorithm'].append({sub_algo_ds['uri'][0]: tag_set['label']})
                    if basename(sub_algo_ds['uri'][0]) not in [basename(img) for img in self.images]:
                        self.images.append(sub_algo_ds['uri'][0])
                    if basename(sub_algo_ds['uri'][0]) in self.imgMap:
                        self.imgMap[basename(sub_algo_ds['uri'][0])].append(tag_set['label'])
                    else:
                        self.imgMap[basename(sub_algo_ds['uri'][0])] = [tag_set['label']]

        self.create_cm()
        self.fill_cm()
        self.create_cm_table()

    def create_cm(self):
        for i, tag_i in enumerate(self.gTags):
            for j, tag_j in enumerate(self.algoTags):
                self.CM['{} {}'.format(tag_i, tag_j)] = 0

    def fill_cm(self):
        for classification in self.result['ground_truth']:
            for gt_uri, gt_label in classification.items():
                right_algo_classi = find_match(self.result['algorithm'], gt_uri)
                for algo_uri, algo_label in right_algo_classi.items():
                    if algo_label:
                        self.CM['{} {}'.format(gt_label, algo_label)] += 1

    def create_cm_table(self):
        # self.y_gt = pd.Series(list(self.gTags), name='Ground Truth')
        # self.y_algo = pd.Series(list(self.algoTags), name='Algorithm')
        # self.cmTabel = pd.crosstab(self.y_gt, self.y_algo)
        for label_set, value in self.CM.items():
            self.cmTabel.loc[label_set.split()[0], label_set.split()[1]] = value


def find_match(object_list, pattern):
    for obj in object_list:
        for key in obj.keys():
            if basename(key) == basename(pattern):
                return obj
    return {}


def save_confusion_matrix(df_confusion, cmap=plt.cm.Oranges):
    plt.matshow(df_confusion, cmap=cmap)
    tick_marks = np.arange(len(df_confusion.columns))
    plt.xticks(tick_marks, df_confusion.columns, rotation=45)
    plt.yticks(tick_marks, df_confusion.index)
    plt.tight_layout()
    for i, j in itertools.product(range(df_confusion.shape[0]), range(df_confusion.shape[1])):
        plt.text(j, i, int(df_confusion.ix[i, j]),
                 horizontalalignment="center",
                 color="black")
    plt.ylabel(df_confusion.index.name)
    plt.xlabel(df_confusion.columns.name)
    plt.savefig('CM.png', bbox_inches="tight")


def style_table(html_table):
    table1 = html_table.split('<tbody>')[0].split()
    style_table1 = []
    for row in table1:
        if row.__contains__('<th></th>'):
            style_table1.append(row.replace('<th>', '<th style="width:30%;">'))
        elif row.__contains__('right'):
            style_table1.append(row.replace('right', 'center'))
        else:
            style_table1.append(row)
    table2 = html_table.split('<tbody>')[-1].split()
    style_table2 = []
    i = 0
    for row in table2:
        if row.__contains__('<th>'):
            style_table2.append(row.replace('<th>', '<th style="width:30%;" id="row {}">'.format(i)))
            i += 1
        elif row.__contains__('<td>'):
            new_row = row.replace('<td>', '<td style="text-align:center;">')
            if new_row.__contains__('True'):
                new_row = new_row.replace('True',
                                          '<p '
                                          'style="padding: 4px;color: white;background-color: #388E3C;display:initial">'
                                          'Passed'
                                          '</p>')
            elif new_row.__contains__('False'):
                new_row = new_row.replace('False',
                                          '<p '
                                          'style="padding: 4px;color: white;background-color: #D32F2F;display:initial">'
                                          'Failed'
                                          '</p>')
            style_table2.append(new_row)
        else:
            style_table2.append(row)
    return '{} <tbody> {}'.format('\n    '.join(style_table1), '\n    '.join(style_table2))


def evaluate(gt_dataset, algo_dataset):
    warnings = []
    evaluator = Evaluator(gt_dataset, algo_dataset)
    evaluator.build_results()
    save_confusion_matrix(evaluator.cmTabel)
    idx = ['{}'.format(key[0]) for key in
           [list(dataset.keys()) for dataset in evaluator.result['ground_truth']]]

    # Build the detailed table with columns of img, GT label, Algo label and predict
    gt_img_dirname = evaluator.GTImgDirname
    # detailed_table = pd.DataFrame(columns=evaluator.CMmap, index=idx)
    # for key, value in evaluator.imgMap.items():
    #     if len(value) == 1:
    #         value.append('Nan')
    #     elif len(value) == 0:
    #         value = ['Nan', 'Nan']
    #     detailed_table.loc['{}/{}'.format(gt_img_dirname, key)] = pd.Series({'Ground Truth': value[0], 'Algorithm': value[1]})
    # detailed_table['Predict'] = detailed_table['Ground Truth'] == detailed_table['Algorithm']
    #
    # # Append warnings if exists
    # if not [value for value in list(detailed_table.Algorithm.values) if value != 'Nan']:
    #     warnings.append('Could be Empty (not labeled) Algorithm data set')
    # if not [val for val in list(detailed_table.loc[:, 'Ground Truth'].values) if val != 'Nan']:
    #     warnings.append('Could be Empty (not labeled) Ground Truth data set')
    #
    # # Calculate accuracy
    # success = 0
    # divider = 1
    # if detailed_table[detailed_table.Predict].Predict.value_counts().size:
    #     success = int(detailed_table[detailed_table.Predict].Predict.value_counts())
    # if detailed_table.Predict.size:
    #     divider = int(detailed_table.Predict.size)
    # accuracy = success / divider
    # accuracy_str = '{:.2f}%'.format(accuracy*100)
    # images = list(evaluator.images)
    # copy_files(images=images)
    # html_table = style_table(detailed_table.to_html(classes='DetailedTable'))
    # return evaluator.cmTabel.to_html(classes='CMTable'), html_table, images, accuracy_str, warnings
