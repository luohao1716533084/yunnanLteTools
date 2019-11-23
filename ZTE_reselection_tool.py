#coding:utf-8

import pandas as pd
import re

excel1_cols_TDD = ['MEID', 'description', 'userLabel', 'earfcn']
excelPath = r'C:\\Users\\luohao\\Desktop\\事件工具\\EUtranCellTDD.xlsx'
excelPath_reselection = r'C:\\Users\\luohao\\Desktop\\事件工具\\EUtranReselectionTDD.xlsx'
SHEET_NAME = 'EUtranCellTDD'

class OpenExcel:
	def __init__(self, excel_path, sheet_name, col_name):
		self.path = excel_path
		self.col_name = col_name
		self.df = pd.read_excel(self.path, sheet_name)

	def pre_process(self,):
		self.frame = self.df.ix[3:, self.col_name]
		self.frame.loc[:,'description'] = list(map(description_proc, list(self.frame.description)))
		excel1_result = concat_columns(self.frame, 'MEID', 'description', 'CI')
		return excel1_result

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

def description_proc(cellLocalId):                   #获取对象描述
	pattern = re.compile(r'\d+')
	new_cellLocalId = pattern.findall(cellLocalId)
	return new_cellLocalId[0]

# test_object = OpenExcel(excelPath, SHEET_NAME, excel1_cols_TDD)
# test_file = test_object.pre_process()
# test_file.to_excel('test_result.xlsx', index=False)



