import numpy as np
import cv2
import pickle
import os
import glob
from PIL import Image
import numpy
import SVM_Aug_Tester

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

sub_dir = get_immediate_subdirectories('/home/faust/Desktop/Internship/ClassyFy/SVMeTester/DataeExtractoneTester/')

c =np.zeros((1,16000))
a=0
length = []
f=0
size=0
for folder_name in sub_dir:
    print(size)
    length.append(size)
    f += 1
    size = 0
    print(f,size)
    for images in glob.glob('/home/faust/Desktop/Internship/ClassyFy/SVMeTester/DataeExtractoneTester/'+folder_name+'/*'):
        print(folder_name)
        a+=1
        imge = Image.open(images)
        pil_image = imge.convert('RGB')
        open_cv_image = numpy.array(pil_image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        orb = cv2.ORB_create()
        kp = orb.detect(open_cv_image,None)
        kp, des = orb.compute(open_cv_image, kp)
        print(des.shape)
        if des.shape[0] == 500:
            c = np.r_[c, np.ndarray.flatten(des).reshape(1, 16000)]
            size += 1
            print(size,'kj')

length.append(size)
length.pop(0)
c = numpy.delete(c, (0), axis=0)
lab = np.zeros((length[0], 1))
arr_size = len(sub_dir)

for y in range(1,arr_size):
    n = np.full((length[y], 1), y)
    lab = np.r_[lab,n]

data = np.c[c,lab]
np.random.shuffle(data)
print(data.shape)
fileObject = open('/home/faust/Desktop/Internship/ClassyFy/SVMeTester/testedata.pickle', 'wb')
pickle.dump(data, fileObject)
fileObject.close()