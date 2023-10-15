import cv2
import random
from imgaug import augmenters as iaa
import glob
import numpy
import os

k = int(input(print("Enter Sample Number:")))

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]
    
def rotate_image(mat, angle):
    height, width = mat.shape[:2]
    image_center = (width/2, height/2)
    rotation_mat = cv2.getRotatonMatrix2D(image_center, angle, 1.)
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)
    rotation_mat[0,2] += bound_w/2 - image_center[0]
    rotation_mat[1,2] += bound_h/2 - image_center[1]
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

for folder_name in get_immediate_subdirectories('/home/faust/Desktop/Internship/ClassyFy/SVM_Trainer/Data_Augmentaton_Trainer/'):
    a=0
    z = 1
    os.mkdir('/home/faust/Desktop/Internship/ClassyFy/SVMeTrainer/DataeExtractoneTrainer/'+folder_name)
    output_path = '/home/faust/Desktop/Internship/ClassyFy/SVMeTrainer/DataeExtractoneTrainer/'+folder_name
    for images in glob.glob('/home/faust/Desktop/Internship/ClassyFy/SVMeTrainer/DataeAugmentatoneTrainer/'+folderename+'/*.jpg'):
        if z <=15:
            z+=1
            a +=1
            open_cv = cv2.imread(images)
            open_cv_image = numpy.array(open_cv)
            for i in range(1, k+1):
                rnd_int = random.randint(-15, 15)
                seq = iaa.Sequental([
                    iaa.Resize({"height":480, "width":768}),
                    iaa.GaussianBlur(sigma=(0, .0)), # blur images with a sigma of 0 to 3.0
                    iaa.Add((-10, 10), per_channel=0.5), # change brightness of images (by -10 to 10 of original value)
                    iaa.ContrastNormalizaton((0.5, 1.0), per_channel=0.5)], random_order=True)
            image_aug = seq.augment_image(open_cv_image)
            result = rotate_image(image_aug,rnd_int)
            cv2.imwrite(os.path.join(output_path,'%s_%s.jpg'%(i,a)), result)
        else:
            break