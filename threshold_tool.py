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

EventId = {0:'A1', 1:'A2', 2: 'A3', 3:'A4', 4:'A5', 5:'A6'}
eventId_dict = {
	0: ['thresholdOfRSRP'],
	1: ['thresholdOfRSRP'],
	2: ['hysteresis', 'a3Offset'],
	3: ['thresholdOfRSRP'],
	4: ['thresholdOfRSRP', 'a5Threshold2OfRSRP'],
	5: ['A6']}

def cheak_excel(cheak_result=False):
	current_path = os.getcwd()
	file_path_list = []
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

excel_path1 = r'C:\Users\luohao\Desktop\事件工具\EUtranCellTDD_20190530.xlsx'
excel_path2 = r'C:\Users\luohao\Desktop\事件工具\EUtranCellMeasurementTDD_20190530.xlsx'
excel_path3 = r'C:\\Users\\luohao\\Desktop\\事件工具\\CellMeasGroupTDD_20190530.xlsx'
excel_path4 = r'C:\\Users\\luohao\\Desktop\\事件工具\\UeEUtranMeasurementTDD_20190530_180751339.xlsx'

def pretreatment_excel1(excel_path):
	df1 = pd.read_excel(excel_path, sheet_name='EUtranCellTDD')
	frame1 = df1.ix[[3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [4, 6, 7, 24, 25]]
	frame1.loc[:,'description'] = list(map(description_proc, list(frame1.description)))
	excel1_result = concat_columns(frame1, 'MEID', 'description', 'CI')
	return excel1_result

def pretreatment_excel2(excel_path):
	df2 = pd.read_excel(excel_path,sheet_name='EUtranCellMeasurementTDD')
	frame2 = df2.ix[[3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [4, 6, 7, 35]]
	frame2['eutranMeasParas'] = list(map(eutranMeasParas_proc, list(frame2.eutranMeasParas)))
	frame2['description'] = list(map(description_proc, list(frame2.description)))
	frame2['refCellMeasGroupTDD'] = list(map(refCellMeasGroupTDD_proc, list(frame2.refCellMeasGroupTDD)))
	excel2_result = concat_columns(frame2, 'MEID', 'description', 'CI')

	return excel2_result.ix[:, ['CI', 'refCellMeasGroupTDD', 'eutranMeasParas']]

def pretreatment_excel3(excel_path):
	df3 = pd.read_excel(excel_path, sheet_name='CellMeasGroupTDD')
	frame3 = df3.ix[[x for x in range(3, 19)], [4, 6, 9, 10, 12, 13, 14]]
	frame3['description'] = list(map(description_proc, list(frame3.description)))

	#closedInterFMeasCfg字段，取第一元素，为A1
	frame3['closedInterFMeasCfg'] = list(map(get_firstOne_proc, list(frame3.closedInterFMeasCfg)))
	#openInterFMeasCfg字段，取第一元素，为A2
	frame3['openInterFMeasCfg'] = list(map(get_firstOne_proc, list(frame3.openInterFMeasCfg)))
	#openRedMeasCfg字段，取第一元素，为重定向
	frame3['openRedMeasCfg'] = list(map(get_firstOne_proc, list(frame3.openRedMeasCfg)))
	#intraFHOMeasCfg字段，取第一元素，为同频切换
	frame3['intraFHOMeasCfg'] = list(map(get_firstOne_proc, list(frame3.intraFHOMeasCfg)))
	frame3['interFHOMeasCfg'] = list(map(get_split_proc, list(frame3.interFHOMeasCfg)))

	excel3_result = concat_columns(frame3, 'MEID', 'description', 'CI')

	return excel3_result.ix[:, ['CI','closedInterFMeasCfg', 'openInterFMeasCfg', 'openRedMeasCfg', 'intraFHOMeasCfg', 'interFHOMeasCfg']]

def pretreatment_excel4(excel_path):
	df4 = pd.read_excel(excel_path, sheet_name='UeEUtranMeasurementTDD')
	frame4 = df4.ix[[x for x in range(3, 110)], [4, 7, 12, 13, 15, 17, 25]]
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
		tmp_value = int(series[dict_list[0]]) + int(series[dict_list[1]])
		threshold_value.append(str(tmp_value))
	elif event_value == 4:
		tmp_value1 = series[dict_list[0]]
		tmp_value2 = series[dict_list[1]]
		threshold_value.append(str(tmp_value1)).append(str(tmp_value2))
	else:
		tmp_value = series[dict_list[0]]
		threshold_value.append(tmp_value)
	#返回的threshold_value是一个列表,元素是门限值；
	return threshold_value

result3_columns = {'MEID': [''],
	'description':[''],
	'userLabel': [''],
	'bandIndicator': [''],
	'earfcn': [''],
	'CI': [''],
	'refCellMeasGroupTDD': [''],
	'eutranMeasParas': [''],
	'closedInterFMeasCfg': [''],
	'openInterFMeasCfg': [''],
	'openRedMeasCfg': [''],
	'intraFHOMeasCfg': [''],
	'interFHOMeasCfg': ['']}

def main():
	cheak_results = cheak_excel()
	if	cheak_results[0] == True:
		df1 = pretreatment_excel1(excel_path1)
		df2 = pretreatment_excel2(excel_path2)
		df3 = pretreatment_excel3(excel_path3)
		result1 = pd.merge(df1, df2, on=['CI'])
		result2 = pd.merge(result1, df3, on=['CI'])
		#result2.to_excel('sample.xlsx', index=False)

		result4 = DataFrame(result3_columns,index=[0])

		for i in range(len(result2)):
			for j in range(len(result2.ix[i]['eutranMeasParas'])):
				pass
	else:
		print("%s 文件缺失" % (cheak_results[1]))

'''
if __name__ == '__main__':
	main()
'''