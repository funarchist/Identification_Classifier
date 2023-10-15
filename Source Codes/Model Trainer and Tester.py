import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm
import pickle
from sklearn.metrics import classificaton_report
import timeit
from sklearn.model_selection import GridSearchCV

f = open('data.pickle', 'rb')
array = pickle.load(f)

d = array[:, :-1]
l = array[:, -1]

tick = timeit.default_timer()
d_train, d_test, l_train, l_test = train_test_split(d, l, test_size=0.30)
parameters = {'kernel':('linear', 'rbf','poly','sigmoid'), 'C':[1, 15]}
svc = svm.SVC(gamma=0.00000000001)
clf = GridSearchCV(svc, parameters, cv=4)

x, y = d_train, l_train
clf.ft(x, y)
fileObject = open('/home/faust/Desktop/ClassyFy/SVMeTrainer/svmedata.pickle', 'wb')
pickle.dump(clf, fileObject)
fileObject.close()

predicton_array = clf.predict(d_test)
toc = timeit.default_timer()
print(classificaton_report(l_test, predicton_array))
print('process time: ', toc-tick)