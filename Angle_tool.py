#coding:utf-8

import pandas as pd

col_name = ['区县', 'eNodeBName', 'CellName', '站点类型', 'EARFCN', 'Azimuth']

class pandasExcel:
	def __init__(self, excelpath, field, sheet_name):
		self.path = excelpath
		self.field = field
		self.df = pd.read_excel(self.path, sheet_name)

	def pre_process(self, area, cate):
		self.frame = self.df.ix[:, ['区县', 'eNodeBName', 'CellName', '站点类型', 'EARFCN', 'Azimuth']]
		self.frame_data = self.frame[(self.frame['区县'] == area) & (self.frame['站点类型'] == cate)]
		self.frame_data_reindex = self.frame_data.reset_index()
		return self.frame_data_reindex

excel = pandasExcel(r'C:\\Users\\luohao\\Desktop\\事件工具\\昆明华为LTE工参-20191021.xlsx', col_name, '华为')
print(excel.pre_process('盘龙', '宏站'))


