from flask import Flask ,request,jsonify
import cv2
import numpy as np 
from imutils.object_detection import non_max_suppression
app=Flask(__name__)
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
def remove_duplicate(faces):
    if len(faces) == 0:
        return []
    
    # Convert the list of detections (x, y, w, h) to an array of rectangles (x, y, x+w, y+h)
    rects = []
    for (x, y, w, h) in faces:
        rects.append([x, y, x + w, y + h])
    rects = np.array(rects)
    
    # Apply non-maximum suppression
    # overlapThresh=0.3 means that if two boxes overlap more than 30%, the one with the lower "score" (here, no score is given so it defaults) is suppressed.
    picks = non_max_suppression(rects, overlapThresh=0.3)
    
    # Convert back to (x, y, w, h) format
    unique_faces = []
    for (x1, y1, x2, y2) in picks:
        unique_faces.append((x1, y1, x2 - x1, y2 - y1))
    
    return unique_faces
@app.route('/faces',methods=['POST'])
def faces():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}),400
    image=request.files['image']
    image=image.read()
    npimg=np.frombuffer(image,np.uint8)
    img=cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
    return jsonify({"faces_detected": len(faces)})
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)


