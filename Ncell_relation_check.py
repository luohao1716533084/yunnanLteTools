#coding:utf-8

import pandas as pd
import os
from pandas import DataFrame

def get_path():
	current_path = os.getcwd()
	file_path_list = []
	for root, dirs, files in os.walk(current_path):
		for name in files:
			file_path_list.append(os.path.join(root,name))

	if len(file_path_list) != 0:
		for i in file_path_list:
			if '现网邻区' in i:
				return i

columns = ['本地小区名称', '邻区小区名称']
def main():
	excel_path = get_path()
	df1 = pd.read_excel(excel_path,sheet_name='邻区列表')
	df2 = pd.read_excel(excel_path, sheet_name='工参表')

	cell_lst = []                              #生成小区名列表
	for f in df2['CellName']:
		cell_lst.append(f)

	cell_lsts = []                            #生成小区二维列表
	for i in cell_lst:
		for j in cell_lst:
			if i != j:
				tmp = list((i,j))
				cell_lsts.append(tmp)

	df3 = DataFrame(cell_lsts, columns=columns)

	df3 = df3.append(df1)
	df3 = df3.append(df1)
	result = df3.drop_duplicates(subset=columns, keep=False)
	result.to_excel('缺失邻区.xlsx', index=False)

main()