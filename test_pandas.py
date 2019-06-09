#coding:utf-8

import pandas as pd
from pandas import Series, DataFrame
import re
from test_excel import *
from win32com.client import Dispatch
import numpy as np
import os

excel_relation = {
	'excel1': 'EUtranCellTDD',
	'excel2': 'EUtranCellMeasurementTDD',
	'excel3': 'CellMeasGroupTDD',
	'excel4': 'UeEUtranMeasurementTDD',
}

def cheak_excel():
	current_path = os.getcwd()
	file_path_list = []
	cheak_result = False
	for root, dirs, files in os.walk(current_path):
		for name in files:
			file_path_list.append(os.path.join(root, name))

	#将匹配到的excel按excel_relation顺序添加进新建列表
	new_excel_filepath_list = []
	for value in excel_relation.values():
		for f in range(len(file_path_list)):
			if value in file_path_list[f]:
				new_excel_filepath_list.append(file_path_list[f])

	#核查文件是否有缺失，如果有缺失，则返回缺失的文件列表
	if len(new_excel_filepath_list) == 4:
		cheak_result = True
		return cheak_result,new_excel_filepath_list
	else:
		missing_file = list(set(excel_relation.values()).difference(new_excel_filepath_list))
		return cheak_result, missing_file

def description_proc(cellLocalId):                   #获取对象描述
	pattern = re.compile(r'\d+')
	new_cellLocalId = pattern.findall(cellLocalId)
	return new_cellLocalId[0]

def refCellMeasGroupTDD_proc(refCellMeasGroupTDD):        #获取测量配置索引组ID
	tmp = refCellMeasGroupTDD.split("CellMeasGroupTDD=")
	if len(tmp) != 0:
		return tmp[1]

def eutranMeasParas_proc(eutranMeasParas):               #获取（异频测量频点）
	interCarriFreq_list = []
	it = re.finditer(r'interCarriFreq=\d+,|interCarriFreq=\d+\.\d+,',eutranMeasParas)
	interCarriFreq = ''
	for match in it:
		if match.group() != None:
			interCarriFreq = match.group().replace('interCarriFreq=',"").replace(',',"")
		interCarriFreq_list.append(interCarriFreq)
	return interCarriFreq_list

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

'''
pretreatment_excel1预处理内容包括：
1，打开excel1，截取需要的字段和记录；
2, 重新设置索引；
3，清洗description字段；
4，添加CI
'''

excel_path2 = r'C:\Users\luohao\Desktop\事件工具\EUtranCellMeasurementTDD_20190530.xlsx'
excel_path1 = r'C:\Users\luohao\Desktop\事件工具\EUtranCellTDD_20190530.xlsx'

def pretreatment_excel1(excel_path):
	df1 = pd.read_excel(excel_path, sheet_name='EUtranCellTDD')
	frame1 = df1.ix[[3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [4, 6, 7, 24, 25]]
	frame1.loc[:,'description'] = list(map(description_proc, list(frame1.description)))
	excel1_result = concat_columns(frame1, 'MEID', 'description', 'CI')
	return excel1_result

def pretreatment_excel2(excel_path):
	df2 = pd.read_excel(excel_path2,sheet_name='EUtranCellMeasurementTDD')
	frame2 = df2.ix[[3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [4, 6, 7, 35]]
	frame2['eutranMeasParas'] = list(map(eutranMeasParas_proc, list(frame2.eutranMeasParas)))
	frame2['description'] = list(map(description_proc, list(frame2.description)))
	frame2['refCellMeasGroupTDD'] = list(map(refCellMeasGroupTDD_proc, list(frame2.refCellMeasGroupTDD)))
	excel2_result = concat_columns(frame2, 'MEID', 'description', 'CI')
	return excel2_result

df2 = pretreatment_excel2(excel_path2)

eutranMeasParas_data = {'MEID': [''], 'description': [''], 'refCellMeasGroupTDD': [''], 'eutranMeasParas': ['']}
eutranMeasParas_frame = DataFrame(eutranMeasParas_data,index=[0])

'''
for i in range(len(eutranMeasParas_list)):
	row = {'MEID':'', 'description':'','refCellMeasGroupTDD':'' , 'eutranMeasParas':''}
	row['MEID'] = frame2.ix[i+3]['MEID']
	row['description'] = description_proc(frame2.ix[i+3]['description'])
	row['refCellMeasGroupTDD'] = refCellMeasGroupTDD_proc(frame2.ix[i+3]['refCellMeasGroupTDD'])
	for j in eutranMeasParas_list[i]:
		row['eutranMeasParas'] = j
		eutranMeasParas_frame = eutranMeasParas_frame.append(row,ignore_index=True)
'''


