#first learning 

import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)

    pixel_centre = hsv_frame[cy, cx]
    hue_value = pixel_centre[0]
    saturation_value = pixel_centre[1]

    color = "Undefined"

    if saturation_value < 50:
        if hue_value == 0:
            color = "BLACK"
        elif hue_value == 255:
            color = "WHITE"
        else:
            color = "GRAY"
    elif 0 <= hue_value < 5:
        color = "RED"
    elif 5 <= hue_value < 22:
        color = "ORANGE"
    elif 22 <= hue_value < 29:
        color = "Light YELLOW"
    elif 29 <= hue_value < 33:
        color = "YELLOW"
    elif 33 <= hue_value < 78:
        color = "GREEN"
    elif 78 <= hue_value < 100:
        color = "Deep GREEN"
    elif 100 <= hue_value < 130:
        color = "BLUE"
    elif 131 <= hue_value < 170:
        color = "VIOLET"
    elif 170 <= hue_value <= 179:
        color = "DEEP PURPLE"
    else:
        color = "RED"

    print(pixel_centre[0], "0")
    print(pixel_centre[1], "1")
    print(color)
    # print(pixel_centre[1], "1")
    pixel_centre_bgr = frame[cy, cx]
    b, g, r = int(pixel_centre_bgr[0]), int(pixel_centre_bgr[1]), int(pixel_centre_bgr[2])
    # print(b, "b")
    cv2.rectangle(frame, (0,0 ), (cx, 60), (0,0,0), -1)
    cv2.putText(frame, color, (10, 50), 0, 1.5, (b, g, r), 2)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()