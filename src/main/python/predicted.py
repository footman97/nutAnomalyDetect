from keras.models import Model, load_model
import sys
import pandas as pd
import numpy as np

'''
加载model并预测
'''

def loadModel(path, sampleData, classifyDir):
    # load model
    try:
        classifier = load_model(path)
        # load sampleData
        xset = np.array(pd.read_excel(sampleData, header=None, skiprows=None))
        xset = xset.reshape((-1, 1, 256))
        # predict
        resOne_hot = classifier.predict(xset)
        res = np.argmax(resOne_hot, axis=1)

        x_write = pd.DataFrame(res)
        x_writer = pd.ExcelWriter(classifyDir + 'predicted.xlsx')
        x_write.to_excel(x_writer,'sheet0', index = False, header=None)  #  控制精度 index去掉左列索引
        x_writer.save()
    except Exception as e:
        print(e)


loadModel(sys.argv[1], sys.argv[2], sys.argv[3])


