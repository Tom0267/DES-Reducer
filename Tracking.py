import cv2

cap = cv2.VideoCapture("tomAndSuzi.mp4")

#object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=20)

while True:
    ret, frame = cap.read()

    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    #extract region of interest
    #roi = frame[340: 600,500: 700]



    #object detection
    #cv2.imshow("Mask", mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        #calculate area and remove small objects
        area = cv2.contourArea(cnt)
        if area > 250:
            cv2.drawContours(frame, [cnt], -1, (0,255,0), 2)

    #key = cv2.waitKey(30)
    if cv2.waitKey(30) & 0xFF ==ord('q'):
        break

    cv2.imshow("Frame", frame)

cap.release()
cv2.destroyAllWindows()

