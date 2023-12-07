import cv2 
import numpy as np

def getAngle(points):
    h=np.sqrt(np.sum((np.square(data[3]-data[0]))))
    a=data[3][0]-data[0][0]
    o=data[3][1]-data[0][1]
    angle=np.degrees(np.arcsin(a/h))
    return angle


cap = cv2.VideoCapture(0) 
# initialize the cv2 QRCode detector 
detector = cv2.QRCodeDetector()
while True:
    _, image = cap.read()
    data, bbox, _ = detector.detectAndDecode(image)
    if bbox is not None:
        # Draw bounding boxes around QR codes
        for i in range(len(bbox)):
            data=bbox[i].astype(int)
            cv2.rectangle(image, tuple(bbox[i][0].astype(int)), tuple(bbox[i][2].astype(int)), color=(0, 255, 0), thickness=2)
            print(getAngle(data))
        # Display the image with bounding boxes
    cv2.imshow("QRCODEscanner", image)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release() 
cv2.destroyAllWindows()
