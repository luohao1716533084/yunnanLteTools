#coding:utf-8


from win32com.client import *

import win32com.client

class easyExcel:
	def __init__(self, filename=None):   #打开文件或者新建文件（如果不存在）
		self.xlapp = win32com.client.Dispatch('Excel.Application')
		if filename:
			self.filename = filename
			self.xlBook = self.xlapp.Workbooks.Open(filename)
		else:
			self.xlBook = self.xlapp.Workbooks.Add()
			self.filename = ''

	def save(self, newfilename=None):    #保存文件
		if newfilename:
			self.filename = newfilename
			self.xlBook.SaveAs(newfilename)
		else:
			self.xlBook.Save()

	def close(self):                        #关闭文件
		self.xlBook.Close(SaveChanges=0)
		del self.xlapp

	def getCell(self, sheet, row, col):       #获取单元格数据
		sheet_data = self.xlBook.Worksheets(sheet)
		return sheet_data.Cells(row, col).Value

	def setCell(self, sheet, row, col, value):    #设置单元格的数据
		sht = self.xlBook.Worksheets(sheet)
		sht.Cells(row, col).Value = value

	def getRange(self, sheet, row1, col1, row2, col2):                     #获得一块区域的数据，返回一个二维元组
		sht = self.xlBook.Worksheets(sheet)
		return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value

	def addPicture(self, sheet, pictureName, Left, Top, Width, Height):     #插入图片
		sht = self.xlBook.Worksheets(sheet)
		sht.Shapes.AddPicture(pictureName, 1, 1, Left, Top, Width, Height)

	def cpSheet(self, before):                    #复制工作表
		shts = self.xlBook.Worksheets
		shts(1).Copy(None, shts(1))

	def insertRow(self, sheet, row):               #
		sht = self.xlBook.Worksheets(sheet)
		sht.Rows(row).Insert(1)

	def addSheet(self,sheetName):
		sht = self.xlBook.Worksheets
		sht.Add().Name = sheetName

if __name__ == '__main__':
	xls = easyExcel(r'C:\Users\luohao\Desktop\事件工具\test_data.xlsx')
	print(xls.getCell('sheet1', 1,1))
	xls.insertRow('sheet1', 7)
	xls.save()
	xls.close()


"""
xls = easyExcel(r'C:\\Users\\luohao\\Desktop\\事件工具\\test_data2.xlsx')
xls.addSheet('test1')
xls.addSheet('test2')
xls.save()
xls.close()
"""
