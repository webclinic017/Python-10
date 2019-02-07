# 얼굴 검출 후 grayscale로 저장한다.
- cv2 `CascadeClassifier`를 활용
- cv2의 경우 `anaconda` venv 기반에서 사용하므로 path를 `new_path='/home/minkj1992/anaconda3/envs/opencv/share/OpenCV/haarcascades/'` 지정해주어야한다.
- `os.listdir('./professor/image/')]`에 있는 모든 파일들에 대하여 이미지 처리를 한다.

```python
import numpy as np
import cv2
import matplotlib.pyplot as plt
from random import randint
import sys
import os

# path= "/home/minkj1992/다운로드/ceo/"
new_path='/home/minkj1992/anaconda3/envs/opencv/share/OpenCV/haarcascades/'
FACE_CASCADE = cv2.CascadeClassifier(new_path+'haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier(new_path+'haarcascade_eye.xml')
# 

def detect_faces(image_path,cnt):
    image_grey = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    # image_grey=cv2.cvtColor(cv2.imread(image_path),cv2.IMREAD_GRAYSCALE)
    faces = FACE_CASCADE.detectMultiScale(image_grey,scaleFactor=1.16,minNeighbors=5,minSize=(25,25),flags=0)
    path = '/home/minkj1992/code/facial_project/cnn-keras/professor/Extracted/'
    for x,y,w,h in faces:
        sub_img=image_grey[y-10:y+h+10,x-10:x+w+10]
        # 저장할때 gray
        cv2.imwrite(path+str(cnt)+".jpg",sub_img)

        
cnt = 0 
for i in [i for i in os.listdir('./professor/image/')]:
    detect_faces('/home/minkj1992/code/facial_project/cnn-keras/professor/image/'+i,cnt)
    cnt+=1
print("done")
```
