import pandas as pd
import numpy as np
import xlrd
import sys

# 分离x-y数据
def separatedXYData(inputRawData, outputData, startFile = 1, endFile = 1):
    # 输出 startFile.xlsx - endFile.xlsx 全闭区间
    maxLength = 2200
    xdata = np.zeros((endFile - startFile + 1, maxLength))  # maxLength长度上限，不足不零
    ydata = np.zeros((endFile - startFile + 1, maxLength))


    for index in range(endFile - startFile + 1):
        print('dealing with...',index + startFile,'th')
        workbook = xlrd.open_workbook(inputRawData)
        booksheet = workbook.sheet_by_index(0)                #用索引取第一个sheet
        rowsLen = booksheet.nrows
        xdata[index, 0] = ydata[index, 0] = rowsLen - 24          # 第一列 数据长度
        for i in range(rowsLen - 24):  # 拷贝数据
            xdata[index, i + 1] = booksheet.cell_value(24+i, 0)
            ydata[index, i + 1] = booksheet.cell_value(24+i, 1)

            # 输出xdata ydata文件 使用pandas直接写入 ！！注意文件名相同时不会覆盖
    x_write = pd.DataFrame(xdata)
    x_writer = pd.ExcelWriter(outputData + 'xdata' + str(startFile) + '_' + str(endFile)+'.xlsx')
    x_write.to_excel(x_writer,'sheet0',float_format='%.5f', index = False, header=None) # float_format 控制精度 index去掉左列索引
    x_writer.save()

    y_write = pd.DataFrame(ydata)
    y_writer = pd.ExcelWriter(outputData + 'ydata' + str(startFile) + '_' + str(endFile)+'.xlsx')
    y_write.to_excel(y_writer,'sheet0',float_format='%.5f', index = False, header=None)
    y_writer.save()


print("hi: ",sys.version)
# import matplotlib.pyplot as plt

separatedXYData(sys.argv[1],sys.argv[2])
print("ddd")