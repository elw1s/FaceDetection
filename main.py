import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

app = FaceAnalysis(name = 'antelopev2')
app.prepare(ctx_id=0, det_size=(640, 640))

capture = cv2.VideoCapture(0)  
while True :
    _, frame =capture.read()
    ret = app.get(frame)
    dimg = app.draw_on(frame,ret)
    cv2.imshow('video',dimg) 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break 
capture.release() 
cv2.destroyAllWindows() 


