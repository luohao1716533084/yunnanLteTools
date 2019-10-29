#coding:utf-8

import pandas as pd

colName = ['区县', 'eNodeBName', 'CellName', '站点类型', 'EARFCN', 'Azimuth']
excelPath = r'C:\\Users\\luohao\\Desktop\\事件工具\\昆明华为LTE工参-20191028.xlsx'
sheetName = '华为'
AREA, CATE = '盘龙', '宏站'


class OpenExcel:
	def __init__(self, excel_path, sheet_name, col_name):
		self.path = excel_path
		self.col_name = col_name
		self.df = pd.read_excel(self.path, sheet_name)

	def pre_process(self, area, cate):
		self.frame = self.df.ix[:, self.col_name]
		self.frame_data = self.frame[(self.frame['区县'] == area) & (self.frame['站点类型'] == cate)]
		self.frame_data_reindex = self.frame_data.reset_index()
		return self.frame_data_reindex


class DfOperate:
	def __init__(self, df):
		self.df = df

	def get_cellname(self, col_Name):                  #获取需要的字段的去重值
		self.colName_list = list(set(self.df[col_Name]))
		return self.colName_list

	def filter_field(self, field_value):
		df = self.df[self.df['eNodeBName'] == field_value]
		return df


def main():
	excel = OpenExcel(excelPath, 'test', colName)
	df = excel.pre_process(AREA, CATE)
	dfoperate = DfOperate(df)                                #生成一个DfOperate
	ENodeBName_List = dfoperate.get_cellname('eNodeBName')
	for ENodeBName in ENodeBName_List:
		sub_tmp = dfoperate.filter_field(ENodeBName)
		#pivot_table = pd.pivot_table(sub_tmp, values=['eNodeBName', 'CellName', 'Azimuth'], columns=['eNodeBName', 'CellName', 'Azimuth'], index='EARFCN')
		print(sub_tmp.stack())


if __name__ == '__main__':
	main()

