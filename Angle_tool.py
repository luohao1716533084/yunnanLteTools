#coding:utf-8

import pandas as pd
from pandas import DataFrame



excel_path = 'C:\\Users\\luohao\\Desktop\\事件工具\\EUtranCellMeasurementTDD_test.xlsx'
df1 = pd.read_excel(excel_path, sheet_name='华为')
df2 = pd.read_excel(excel_path, sheet_name='FDD')
df3 = pd.read_excel(excel_path,	sheet_name='中兴')
df4 = pd.read_excel(excel_path,	sheet_name='大唐')

col_name = ['区县', 'eNodeBName', 'CellName', '站点类型', 'EARFCN', 'Azimuth']



