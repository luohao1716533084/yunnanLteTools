#coding:utf-8

import pandas as pd
from pandas import DataFrame
import re
import os
import copy

excel_relation_TDD = {
    'excel1': 'EUtranCellTDD',
    'excel2': 'EUtranCellMeasurementTDD',
    'excel3': 'CellMeasGroupTDD',
    'excel4': 'UeEUtranMeasurementTDD',
}

excel_relation_FDD = {
    'excel1': 'EUtranCellFDD',
    'excel2': 'EUtranCellMeasurement',
    'excel3': 'CellMeasGroup',
    'excel4': 'UeEUtranMeasurement',
}

EventId = {0:'A1', 1:'A2', 2: 'A3', 3:'A4', 4:'A5', 5:'A6'}
eventId_dict = {
    0: ['thresholdOfRSRP'],
    1: ['thresholdOfRSRP'],
    2: ['hysteresis', 'a3Offset'],
    3: ['thresholdOfRSRP'],
    4: ['thresholdOfRSRP', 'a5Threshold2OfRSRP'],
    5: ['thresholdOfRSRP']}

excel1_cols_TDD = ['MEID', 'description', 'userLabel', 'bandIndicator', 'earfcn']
excel1_cols_FDD = ['MEID', 'description', 'userLabel', 'freqBandInd', 'earfcnDl']
excel2_cols_TDD = ['MEID', 'description', 'refCellMeasGroupTDD', 'eutranMeasParas']
excel2_cols_FDD = ['MEID', 'description', 'refCellMeasGroup', 'eutranMeasParas']
excel3_cols = ['MEID', 'description', 'closedInterFMeasCfg', 'openInterFMeasCfg', 'openRedMeasCfg', 'intraFHOMeasCfg', 'interFHOMeasCfg']
excel4_cols = ['MEID', 'measCfgIdx', 'eventId', 'thresholdOfRSRP', 'a5Threshold2OfRSRP', 'hysteresis', 'a3Offset']

def cheak_excel(cheak_result=False):
    current_path = os.getcwd()
    file_path_list = []
    for root, dirs, files in os.walk(current_path):
        for name in files:
            file_path_list.append(os.path.join(root, name))

    #将匹配到的excel按excel_relation顺序添加进新建列表
    new_excel_filepath_list = []
    for value in excel_relation_TDD.values():
        for f in range(len(file_path_list)):
            if value in file_path_list[f]:
                new_excel_filepath_list.append(file_path_list[f])

    #核查文件是否有缺失，如果有缺失，则返回缺失的文件列表
    if len(new_excel_filepath_list) == 4:
        cheak_result = True
        LTE = 'TDD'
        return cheak_result,new_excel_filepath_list, LTE
    elif len(new_excel_filepath_list) == 0:
        for value in excel_relation_FDD.values():
            for f in range(len(file_path_list)):
                if value in file_path_list[f]:
                    new_excel_filepath_list.append(file_path_list[f])

        if len(new_excel_filepath_list) == 4:
            cheak_result = True
            LTE = 'FDD'
            return cheak_result,new_excel_filepath_list, LTE
    else:
        return cheak_result

def description_proc(cellLocalId):                   #获取对象描述
    pattern = re.compile(r'\d+')
    new_cellLocalId = pattern.findall(cellLocalId)
    return new_cellLocalId[0]


def delete_nan_proc(df):
    index_num = df.index.values
    for num in index_num:
        if str(df.loc[[num],['eutranMeasParas']].values[0][0]) == 'nan':
            df.drop([num],inplace=True)
    return df

def refCellMeasGroup_proc(refCellMeasGroupTDD):        #获取测量配置索引组ID
    pattern = re.compile(r'CellMeasGroup\w{0,3}\=\d+')
    new_CellMeasGroup = pattern.findall(refCellMeasGroupTDD)      #new_CellMeasGroup返回的是一个列表
    result = description_proc(new_CellMeasGroup[0])               #这里调用函数提取数字
    return result

def eutranMeasParas_proc(eutranMeasParas):               #获取（异频测量频点）
    interCarriFreq_list = []
    it = re.finditer(r'interCarriFreq=\d+,|interCarriFreq=\d+\.\d+,',eutranMeasParas)
    interCarriFreq = ''
    for match in it:
        if match.group() != None:
            interCarriFreq = match.group().replace('interCarriFreq=',"").replace(',',"")
        interCarriFreq_list.append(interCarriFreq)
    return interCarriFreq_list

def get_firstOne_proc(str):
    if ';' in str:
        lst = str.split(";")[0]
    else:
        lst = list(str)
    return lst

def get_split_proc(str):
    lst = str.split(";")
    return lst

#将一个DataFrame类型对象的columns1，和columns2两个字段的数据连接组成一个新的字段的数据，并将新的字段添加进原DataFrame对象中；
def concat_columns(df, columns1, columns2, new_column):
    columns = list(df.columns[:])
    if columns1 in columns and columns2 in columns:
        new_column_data = []
        for x in range(len(df.index)):
            tmp = str(df[columns1].iloc[x]) + str("-") +df[columns2].iloc[x]
            new_column_data.append(tmp)
        df[new_column] = new_column_data
    return df

def pretreatment_excel1(excel_path, lte, excel_name):
    cols = ''
    df1 = pd.read_excel(excel_path, sheet_name=excel_name)
    if lte == 'TDD':
        cols = excel1_cols_TDD
        frame1 = df1.loc[3:,cols]
        frame1.loc[:,'description'] = list(map(description_proc, list(frame1.description)))
        excel1_result = concat_columns(frame1, 'MEID', 'description', 'CI')
        return excel1_result
    if lte == 'FDD':
        cols = excel1_cols_FDD
        frame1 = df1.loc[3:,cols]
        frame1.loc[:,'description'] = list(map(description_proc, list(frame1.description)))
        excel1_result = concat_columns(frame1, 'MEID', 'description', 'CI')
        excel1_result.rename(columns={'earfcnDl': 'earfcn'}, inplace=True)
        excel1_result.rename(columns={'freqBandInd':'bandIndicator'}, inplace=True)
        return excel1_result

def pretreatment_excel2(excel_path, lte, excel_name):
    cols = ''
    df2 = pd.read_excel(excel_path,sheet_name=excel_name)
    if lte == 'TDD':
        cols = excel2_cols_TDD
        frame = df2.loc[3:, cols]
        frame2 = delete_nan_proc(frame)
        frame2['eutranMeasParas'] = list(map(eutranMeasParas_proc, list(frame2.eutranMeasParas)))
        frame2['description'] = list(map(description_proc, list(frame2.description)))
        frame2['refCellMeasGroupTDD'] = list(map(refCellMeasGroup_proc, list(frame2.refCellMeasGroupTDD)))
        excel2_result = concat_columns(frame2, 'MEID', 'refCellMeasGroupTDD', 'refId')
        excel2_result = concat_columns(excel2_result, 'MEID', 'description', 'CI')
        excel2_result.rename(columns={'refCellMeasGroupTDD':'refCellMeasGroup'}, inplace=True)
        return excel2_result.loc[:, ['CI', 'refId', 'refCellMeasGroup', 'eutranMeasParas']]
    if lte == 'FDD':
        cols = excel2_cols_FDD
        frame = df2.loc[3:, cols]
        frame2 = delete_nan_proc(frame)
        frame2['eutranMeasParas'] = list(map(eutranMeasParas_proc, list(frame2.eutranMeasParas)))
        frame2['description'] = list(map(description_proc, list(frame2.description)))
        frame2['refCellMeasGroup'] = list(map(refCellMeasGroup_proc, list(frame2.refCellMeasGroup)))
        excel2_result = concat_columns(frame2, 'MEID', 'refCellMeasGroup', 'refId')
        excel2_result = concat_columns(excel2_result, 'MEID', 'description', 'CI')
        return excel2_result.loc[:, ['CI', 'refId', 'refCellMeasGroup', 'eutranMeasParas']]

def pretreatment_excel3(excel_path, excel_name):
    df3 = pd.read_excel(excel_path, sheet_name=excel_name)
    frame3 = df3.loc[3:, excel3_cols]
    frame3['description'] = list(map(description_proc, list(frame3.description)))
    #closedInterFMeasCfg字段，取第一元素，为A1
    frame3['closedInterFMeasCfg'] = list(map(get_firstOne_proc, list(frame3.closedInterFMeasCfg)))
    #openInterFMeasCfg字段，取第一元素，为A2
    frame3['openInterFMeasCfg'] = list(map(get_firstOne_proc, list(frame3.openInterFMeasCfg)))
    #openRedMeasCfg字段，取第一元素，为重定向
    frame3['openRedMeasCfg'] = list(map(get_firstOne_proc, list(frame3.openRedMeasCfg)))
    #intraFHOMeasCfg字段，取第一元素，为同频切换
    frame3['intraFHOMeasCfg'] = 50
    frame3['interFHOMeasCfg'] = list(map(get_split_proc, list(frame3.interFHOMeasCfg)))

    excel3_result = concat_columns(frame3, 'MEID', 'description', 'refId')

    return excel3_result.loc[:, ['refId','closedInterFMeasCfg', 'openInterFMeasCfg', 'openRedMeasCfg', 'intraFHOMeasCfg', 'interFHOMeasCfg']]

def pretreatment_excel4(excel_path, excel_name):
    df4 = pd.read_excel(excel_path, sheet_name=excel_name)
    #[x for x in range(3, 110)]
    frame4 = df4.loc[3:, excel4_cols]
    excel4_result = concat_columns(frame4, 'MEID', 'measCfgIdx', 'MEID-measCfgIdx')
    excel4_result = excel4_result.set_index('MEID-measCfgIdx')
    return excel4_result

"""根据站号(MEID)和测量配置号获取UeEUtranMeasurementTDD表里的门限值"""
def get_threshold_value(meid, measCfgIdx, subUeEUtran):
    threshold_value = []
    meid_eventId = str(meid) + str('-') + str(measCfgIdx)
    #series为行记录，其类型为<class 'pandas.core.series.Series'>；可以通过['列名']访问值
    series = subUeEUtran.loc[meid_eventId]
    event_value = int(series['eventId'])
    dict_list = eventId_dict[event_value]
    if event_value == 2:
        tmp_value = float(series[dict_list[0]]) + float(series[dict_list[1]])
        threshold_value.append(str(tmp_value))
    elif event_value == 4:
        tmp_value1 = series[dict_list[0]]
        threshold_value.append(str(tmp_value1))
        tmp_value2 = series[dict_list[1]]
        threshold_value.append(str(tmp_value2))
    else:
        tmp_value = series[dict_list[0]]
        threshold_value.append(tmp_value)
    #返回的threshold_value是一个列表,元素是门限值；
    return threshold_value

def get_threshold_value1(meid, measCfgIdx, subUeEUtran):
    threshold_value = [' ', ' ', ' ', ' ']
    meid_eventId = str(meid) + str('-') + str(measCfgIdx)
    #series为行记录，其类型为<class 'pandas.core.series.Series'>；可以通过['列名']访问值
    series = subUeEUtran.loc[meid_eventId]
    event_value = int(series['eventId'])
    dict_list = eventId_dict[event_value]
    if event_value == 2:                      #异频A3
        tmp_value = float(series[dict_list[0]]) + float(series[dict_list[1]])
        threshold_value[0] = tmp_value
    elif event_value == 3:                    #异频A4
        tmp_value = series[dict_list[0]]
        threshold_value[1] = tmp_value
    elif event_value == 4:                    #A5
        tmp_value1 = series[dict_list[0]]
        threshold_value[2] = tmp_value1
        tmp_value2 = series[dict_list[1]]
        threshold_value[3] = tmp_value2
    #返回的threshold_value是一个列表,元素是门限值；该长度固定是4
    return threshold_value

#intraFHOMeasCfg：同频A3
final_columns = {'MEID': [''],
                 'description':[''],
                 'userLabel': [''],
                 'bandIndicator': [''],
                 'earfcn': [''],
                 'CI': [''],
                 'refId': [''],
                 'refCellMeasGroup': [''],
                 'eutranMeasParas': [''],
                 '频点序列索引': [''],
                 'A1门限': [''],
                 'A2门限': [''],
                 'A2盲重定向': [''],
                 '同频A3': [''],
                 '异频A3': [''],
                 'A4门限': [''],
                 'A5门限1': [''],
                 'A5门限2': ['']}

row1_cols = ['MEID',
             'description',
             'userLabel',
             'bandIndicator',
             'earfcn',
             'CI',
             'refId',
             'refCellMeasGroup']

row2_cols = ['closedInterFMeasCfg',
             'openInterFMeasCfg',
             'openRedMeasCfg',
             'intraFHOMeasCfg']

def insert_threshold(df1, df2):          #df1为3个原始表关联的表，df2为UeEUtran表
    meid_set1 = set(df1['MEID'])
    meid_set2 = set(df2['MEID'])
    meid_set = meid_set1.intersection(meid_set2)
    final_result = DataFrame(final_columns,index=[0])
    count = 0
    for meid in meid_set:
        sub_df1 = df1[df1['MEID'] == meid]
        sub_df2 = df2[df2['MEID'] == meid]
        for i in range(len(sub_df1)):
            insertRow = []
            row = sub_df1.iloc[i]   #row 的类型为series
            fre_lst = row['eutranMeasParas']   #fre_lst为异频频点列表,本身就是list类型，无需进行转化
            row1 = row[row1_cols]     #row1的类型为series
            row2 = row[row2_cols]     #row2的类型为series
            cfg_lst = row['interFHOMeasCfg']

            for value in list(row1):         #向insertRow列表插入row1八个元素
                insertRow.append(value)

            for value in list(row2):          #向insertRow列表插入4个元素
                threshold_value = get_threshold_value(meid, value, sub_df2)   #将测量配置号换成门限值
                insertRow.append(threshold_value[0])

            for n in range(len(fre_lst)):
                insertRow_cp = copy.deepcopy(insertRow)
                insertRow_cp.insert(8, fre_lst[n])
                insertRow_cp.insert(9, n+1)
                tmplist = get_threshold_value1(meid, cfg_lst[n], sub_df2)
                new_result = insertRow_cp + tmplist
                final_result.loc[count] = new_result
                count += 1
                del insertRow_cp, tmplist, new_result

    return final_result

def main():
    cheak_results = cheak_excel()
    if	cheak_results[0] == True:
        excel_path_list = cheak_results[1]
        lte = cheak_results[2]
        excel_dict = {}
        if lte == 'TDD':
            excel_dict = excel_relation_TDD
        if lte == 'FDD':
            excel_dict = excel_relation_FDD
        df1 = pretreatment_excel1(excel_path_list[0], lte, excel_dict['excel1'])
        df2 = pretreatment_excel2(excel_path_list[1], lte, excel_dict['excel2'])
        df3 = pretreatment_excel3(excel_path_list[2], excel_dict['excel3'])
        df4 = pretreatment_excel4(excel_path_list[3], excel_dict['excel4'])
        result1 = pd.merge(df1, df2, on=['CI'])
        result2 = pd.merge(result1, df3, on=['refId'])
        result = insert_threshold(result2, df4)
        result.to_excel('result.xlsx', index=False)
    else:
        print("%s 文件缺失, 请核查文件是否存在")

if __name__ == '__main__':
    print("Welcome to use threshold tool.The version2.1. Author by luohao")
    print('欢迎使用中兴LTE切换事件工具')
    print('***TDD和FDD制式均可使用该工具')
    print("程序静默执行，请耐心等待...")
    main()
    print(input("result.xlsx文件已生成，输入任意键按回车退出："))
