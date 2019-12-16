#coding:utf-8

import pandas as pd
import re
import copy

eutranTDD_cols = ['MEID', 'description', 'userLabel', 'earfcn']
eutranTDD_Reselection_cols = ['MEID', 'description', 'cellReselectionPriority', 'eutranRslPara', 'eutranRslParaExt']
excelPath_eutranTDD = r'C:\\Users\\luohao\\Desktop\\事件工具\\EUtranCellTDD.xlsx'
excelPath_reselection = r'C:\\Users\\luohao\\Desktop\\事件工具\\EUtranReselectionTDD.xlsx'
SHEET_NAME_EUtran = 'EUtranCellTDD'
SHEET_NAME_Re = 'EUtranReselectionTDD'

#列表第一个元素是template，第二个元素是替换根据template匹配出来的内容，得到需要的数据
freq = [r'interCarriFreq=\d+,|interCarriFreq=\d+\.\d+,', 'interCarriFreq=']
freq_ext = [r'interCarriFreqExt=\d+,|interCarriFreqExt=\d+\.\d+,', 'interCarriFreqExt=']
reselection = [r'interReselPrio=\d', 'interReselPrio=']
reselection_ext = [r'eMTCInterReselPrioExt=\d', 'eMTCInterReselPrioExt=']
result_columns = ['eNodeBId', 'Id', '小区名', '本小区服务频点', '本小区服务频点优先级', 'CI', '频间频点', '频间频点优先级']

#将一个DataFrame类型对象的columns1，和clumns2两个字段的数据连接组成一个新的字段的数据，并将新的字段添加进原DataFrame对象中；
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

class GetFilePath:
	pass

class OpenExcel:
	def __init__(self, excel_path, sheet_name, col_name):
		self.path = excel_path
		self.col_name = col_name
		self.df = pd.read_excel(self.path, sheet_name)

	def pre_process(self,):
		self.frame = self.df.ix[3:, self.col_name]
		self.frame.loc[:,'description'] = list(map(description_proc, list(self.frame.description)))
		excel1_result = concat_columns(self.frame, 'MEID', 'description', 'CI')
		return excel1_result       #反馈的结果已经是DataFrame类型

class EasyRe:
	def __init__(self, template, replace_text):
		self.template = template                             #template为正则表达式模板
		self.replace_text = replace_text                     #匹配的出内容需要进一步清洗

	def list_result_proc(self,text):       #获取（异频测量频点，返回的是列表形式）text为需要匹配的文本
		interCarriFreq_list = []
		it = re.finditer(self.template, text)
		interCarriFreq = ''
		for match in it:
			if match.group() != None:
				interCarriFreq = match.group().replace(self.replace_text, "").replace(',', "")
			interCarriFreq_list.append(interCarriFreq)
		return interCarriFreq_list

result_cols = ['MEID_x', 'description_x','userLabel','earfcn','cellReselectionPriority', 'CI','eutranRslPara','eutranRslParaExt']

def re_proc(cell_data1, cell_data2, flag):
	eutranPara_freq_obj = EasyRe(freq[0],freq[1])
	eutranPara_freq_ext_obj = EasyRe(freq_ext[0],freq_ext[1])
	eutranPara_Prio_obj = EasyRe(reselection[0], reselection[1])
	eutranPara_Prio_ext_obj = EasyRe(reselection_ext[0], reselection_ext[1])
	freq_list, Prio_list = [], []
	freq_list.append(eutranPara_freq_obj.list_result_proc(cell_data1))
	Prio_list.append(eutranPara_Prio_obj.list_result_proc(cell_data1))
	if flag == False:
		freq_list_result = freq_list[0] + eutranPara_freq_ext_obj.list_result_proc(cell_data2)
		Prio_list_result = Prio_list[0] + eutranPara_Prio_ext_obj.list_result_proc(cell_data2)
		return freq_list_result, Prio_list_result
	else:
		return freq_list[0], Prio_list[0]

def main():
	EUtranCellTDD = OpenExcel(excelPath_eutranTDD, SHEET_NAME_EUtran,eutranTDD_cols)
	EUtranReselectionTDD = OpenExcel(excelPath_reselection,SHEET_NAME_Re,eutranTDD_Reselection_cols)
	excel1 = EUtranCellTDD.pre_process()
	excel2 = EUtranReselectionTDD.pre_process()
	result1 = pd.merge(excel1, excel2, on=['CI'])
	result1 = result1.ix[:, result_cols]
	eutranRslPara = result1['eutranRslPara']
	eutranRslParaExt = result1['eutranRslParaExt']
	Flag = list(pd.isna(eutranRslParaExt))
	freq_prio = []
	for t1, t2, f in zip(eutranRslPara, eutranRslParaExt, Flag):
		try:
			tmp = re_proc(t1, t2, f)
			freq_prio.append(tmp)
		except TypeError:
			print(t1, t2, f)

	result_df = []
	for row, fp in zip(result1.iterrows(), freq_prio):
		insertRow_tmp = list(row[1][0:6])
		for f, p in zip(fp[0], fp[1]):
			insertRow_copy = copy.deepcopy(insertRow_tmp)
			insertRow_copy = insertRow_copy + [f, p]
			result_df.append(insertRow_copy)
			del insertRow_copy

	df = pd.DataFrame(result_df)
	df.columns = result_columns
	df.to_excel('result_df1211.xlsx', index=False)
	result1.to_excel('result112_11.xlsx', index=False)

if __name__ == '__main__':
	print("Welcome to use ZTE_reselection_tool.The version1.0. Author by LuoHao")
	print('欢迎使用中兴重选工具')
	print("程序静默执行，请耐心等待...")
	main()
	print(input("result.xlsx文件已生成，输入任意键按回车退出："))
