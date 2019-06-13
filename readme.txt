1）打开：EUtranCellTDD
获取MEID,description,
MEID	description	userLabel CI

2）打开EUtranCellMeasurementTDD
1.根据自身获取如下字段：
EnodeB	对象描述	测量配置索引组   eutranMeasParas"


3）打开CellMeasGroupTDD表：
1.根据上张表的eutranMeasParas频点个数s（即[的元素个数为频点个数]），只获取s个元素。在interFHOMeasCfg字段中；
2.获取如下字段：
openRedMeasCfg	intraFHOMeasCfg	interFHOMeasCfg
MEID  description closedInterFMeasCfg openInterFMeasCfg  

用EUtranCellMeasurementTDD表中的[测量配置索引组]匹配CellMeasGroupTDD表中的[MEID]+[description]

3）打开UeEUtranMeasurementTDD
根据测量配置号，获取事件标识，再根据事件标识的数值获取采用什么事件，同时得出门限值；
A3=A3事件偏移(dB)+判决迟滞范围(dB)
A4=事件判决的RSRP门限(dBm)
A5门限1=事件判决的RSRP门限(dBm)
A5门限2=A5事件判决的RSRP绝对门限2(dBm)
**每个小区对应一行记录

最后输出：
小区名称，站号，ci（小区），主频，频段，异频测量频点，A1，A2，同频事件，异频事件，事件门限值


***注意：***
1，执行程序需要4个excel在程序文件同一文件夹下，且仅存在要处理的excel；
2，执行程序，必须保持excel关闭；


EUtranCellMeasurementTDD;32791;10

==============================
pretreatment_excel4()
返回的内容：
MEID                  32791
measCfgIdx               10
eventId                   0
thresholdOfRSRP         -75
a5Threshold2OfRSRP      -90
hysteresis                0
a3Offset                  3
========================================
DataFrame常见问题：
1，如果是从excel中读取数据，输出DataFrame，则自动生成索引；
2，如果是通过字典调用DataFrame()，生成DataFrame类型数据，则需要设置首行的初始索引；设置的索引类型必须为列表类型;
3，如果是DataFrame类型调用append插入字典类型数据，用此方法添加记录且使索引自增，则需添加ignore_index=True;
4，

========================================
numpy
========================================


========================================
pandas
DataFrame
1，重新设置索引
new_index = ['one', 'two', 'three', 'four', 'five']
frame = DataFrame(data,index=new_index)
2, 读取索引的行号, 结果集为列表,首行是字段名，无索引号；
index_num = df.index.values
3，获取字段名；
field_0 = frame.columns[0]
4，loc，iloc，ix
frame.loc[匹配索引自身]
frame.iloc[匹配索引的索引号]
frame.ix[匹配索引的索引号 | 匹配索引自身]
5，获得columns名
frame.columns[:] #返回的是object对象
6，时间花销
izip > zip > itertuples > enumerate > iterrows > range(index)
7，frame.ix
#获取多列多行
frame.ix[[行号],[列名列表]]
#获取多行所有列
frame.ix[:, [列名列表]]
8，将A列作为索引
frame.set_index(列名A)


concat
merge
join
========================================
多线程
multiprocessing
concurrent.futures
