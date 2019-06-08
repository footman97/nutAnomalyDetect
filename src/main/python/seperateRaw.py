import pandas as pd
import numpy as np
import xlrd
import sys
import os


def seperateData(inputRawDir, outputDir, filesNum):

    maxLength = 2200
    filesNum = int(filesNum)
    xdata = np.zeros((filesNum, maxLength))  # maxLength长度上限，不足不零
    ydata = np.zeros((filesNum, maxLength))

    files = os.listdir(inputRawDir) #列出文件夹下所有的目录与文件
    files.sort() #排序
    index = 0
    for tempIndex in range(0,len(files)):
        path = os.path.join(inputRawDir, files[tempIndex])
        if os.path.isfile(path):
            print(path)
            workbook = xlrd.open_workbook(path)
            booksheet = workbook.sheet_by_index(0)                #用索引取第一个sheet
            rowsLen = booksheet.nrows
            xdata[index, 0] = ydata[index, 0] = rowsLen - 24          # 第一列 数据长度
            for i in range(rowsLen - 24):  # 拷贝数据
                xdata[index, i + 1] = booksheet.cell_value(24+i, 0)
                ydata[index, i + 1] = booksheet.cell_value(24+i, 1)
            index += 1

    # 输出xdata ydata文件 使用pandas直接写入 ！！注意文件名相同时不会覆盖
    x_write = pd.DataFrame(xdata)
    x_writer = pd.ExcelWriter(outputDir + 'xData' + '.xlsx')
    x_write.to_excel(x_writer,'sheet0',float_format='%.8f', index = False, header=None) # float_format 控制精度 index去掉左列索引
    x_writer.save()

    y_write = pd.DataFrame(ydata)
    y_writer = pd.ExcelWriter(outputDir + 'yData' + '.xlsx')
    y_write.to_excel(y_writer,'sheet0',float_format='%.8f', index = False, header=None)
    y_writer.save()

seperateData(sys.argv[1],sys.argv[2],sys.argv[3])