import pandas as pd
import numpy as np
import sys

'''
sampling 
'''

def sampling(trimx_file, trimy_file, outputDataPath):

    ydata_all = np.array(pd.read_excel(trimy_file, header=None, skiprows=None))
    xdata_all = np.array(pd.read_excel(trimx_file, header=None, skiprows=None))

    ydata_rows, _ = ydata_all.shape
    xdata_rows, _ = xdata_all.shape

    uni_bin_size = 256
    # 需要替换掉temp_ydata_rows
    temp_ydata_rows = ydata_rows
    ydata_uni_all = np.zeros((temp_ydata_rows,uni_bin_size))
    ydata_uni = np.zeros((uni_bin_size))

    for fi in range(temp_ydata_rows):
        print('fi:',fi)

        # 提取对应的 力矩（Y轴）、旋角 （X轴）数据
        # 计算数据有效长度
        data_src_len = int(ydata_all[fi,0])
        ydata_row = abs(ydata_all[fi,1: data_src_len+1])  # 数据力矩有负数，感觉应该是不对的，可能是测量误差，所以暂时都取正值
        xdata_row = xdata_all[fi,1: data_src_len+1]

        y_left_limit  = 1.618
        data_left_begin = 0

        # 截取左端数据
        for di in range(data_src_len):
            tmp_data_index = di+1
            if ( ydata_all[fi,tmp_data_index] < y_left_limit ):  # 如果力矩数值小于既定阈值
                data_left_begin = data_left_begin + 1
            else:
                break
        #     print('left begin:',data_left_begin)

        data_left_begin = max(data_left_begin, 1)


        # 截取右端数据，根据 旋角数据(xdata 作为基准）
        flag_end = 0
        right_end = 0
        ydata_max = max(ydata_row)
        dix = data_src_len-1   # 定位到最后一个数据元素
        while(True):
            tmp_xdata_num0 = xdata_row[dix]
            tmp_xdata_num1 = xdata_row[dix-1]
            tmp_ydata_num0 = ydata_row[dix]
            # 后面的坐标 > 前面的坐标 =正常，因为角度旋转是递增
            if(tmp_xdata_num0 > tmp_xdata_num1 and tmp_ydata_num0 >= (0.4 * ydata_max)):
                break
            else:
                dix = dix -1
                right_end = right_end + 1
        #     print('right end:',right_end)

        # ydata_trimed :     存放前、后截取完成的 力矩数据 （Y轴）
        # xdata_trimed:      存放前、后截取完成的 力矩数据 （X轴)
        # data_trimed_len:   截取后的数据长度
        ydata_trimed  = ydata_row[data_left_begin: (data_src_len - max(right_end,6))]
        xdata_trimed  = xdata_row[data_left_begin: (data_src_len - max(right_end,6))]
        data_trimed_len = len(ydata_trimed)
        #         print('data Len:',data_trimed_len)

        # 长度归一化
        draw_flag = 1
        if ( data_trimed_len <= uni_bin_size ):
            uni_gap = 1
        else:
            uni_gap = (data_trimed_len / uni_bin_size)  # uni_gap 等于(数据长度 / uni_bin_size)
        #         print('uni_gap:',uni_gap)

        # gap > 1情况
        from math import floor
        if(uni_gap >1):
            zone_left_pre = 0
            zone_right_pre = max(floor(uni_gap),2)
            tmp_avg = sum ( ydata_trimed[zone_left_pre:zone_right_pre]) / (zone_right_pre - zone_left_pre)
            ydata_uni[0] = tmp_avg

            for uni_i in range(1,uni_bin_size):
                zone_left_cur  = floor( (uni_i-1) * uni_gap) + 1         #  从1开始
                zone_left_cur  = min( zone_left_cur, data_trimed_len)    #  确保不越界
                #             print('zone_left_cur:',zone_left_cur)
                if ( zone_left_cur <= zone_right_pre):          # 当前左边界 同上次的右边界重合
                    zone_left_cur = zone_right_pre              # 重新确定左边界 ，确定不重复取值  +1
                #                 print('zone_left_curs:',zone_left_cur)

                tmp_zone_right = floor(uni_i * uni_gap)        # 数组右边界取整
                if ( tmp_zone_right > zone_left_cur):          # 当前右边界大于左边界，数据有效
                    zone_right_pre = tmp_zone_right
                    zone_right_cur = tmp_zone_right
                else:
                    zone_right_cur = zone_left_cur + floor(uni_gap)
                    zone_right_pre = zone_right_cur

                zone_left_cur =  min (zone_left_cur ,data_trimed_len)
                zone_right_cur = min (zone_right_cur, data_trimed_len)

                if (zone_left_cur == data_trimed_len):
                    ydata_uni[uni_i] = ydata_trimed[uni_bin_size]
                else:
                    tmp_avg = sum ( ydata_trimed[zone_left_cur:zone_right_cur+1]) / (zone_right_cur - zone_left_cur+1)
                    #                 print('zone_left:',zone_left_cur)
                    #                 print('zone_right:',zone_right_cur)
                    ydata_uni[uni_i] = tmp_avg
        else: # gap <= 1情况
            for uni_i in range(data_trimed_len):
                ydata_uni[uni_i] = ydata_trimed[uni_i]
            # 不足uni_bin_size部分用ydata_trimed最后的值填充
            for uni_i in range(data_trimed_len, uni_bin_size):
                ydata_uni[uni_i] = ydata_trimed[data_trimed_len-1]

        # 拷贝ydata_uni
        uni_max= max(ydata_uni)
        ydata_uni = 1000 * ydata_uni / uni_max # 从【0,1】 --> 【0,1000】
        ydata_uni_all[fi,:] = ydata_uni


    #     plt.plot(ydata_uni)
    #     plt.show()

    # 写入文件
    y_write = pd.DataFrame(ydata_uni_all)
    y_writer = pd.ExcelWriter(outputDataPath)
    y_write.to_excel(y_writer,'sheet0',float_format='%.8f', index = False, header=None)
    y_writer.save()

#
#
# if platform.system() == 'Darwin':
#     outputDataPath = '/Users/liujun/Desktop/thesisProj/sampleData100.xlsx'
#     trimy_file = '/Users/liujun/Desktop/thesisProj/separated_zero_padding/ydata1_100.xlsx'
#     trimx_file = '/Users/liujun/Desktop/thesisProj/separated_zero_padding/xdata1_100.xlsx'
#

#  sys.argv[1] xData.xlsx
#  sys.argv[2] yData.xlsx
#  sys.argv[3] outputFileName
sampling(sys.argv[1], sys.argv[2], sys.argv[3])

