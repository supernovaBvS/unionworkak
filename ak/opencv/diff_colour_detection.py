import cv2
import numpy as np
import glob

color_ranges = {
    # 'red': (np.array([0, 70, 50]), np.array([10, 255, 255])),
    # 'orange': (np.array([11, 70, 50]), np.array([25, 255, 255])),
    'yellow': (np.array([26, 70, 50]), np.array([35, 255, 255])),
    'green': (np.array([36, 70, 50]), np.array([70, 255, 255])),
    'blue': (np.array([100, 70, 50]), np.array([130, 255, 255])),
    # 'purple': (np.array([131, 70, 50]), np.array([160, 255, 255])),
    # 'pink': (np.array([150, 70, 50]), np.array([179, 255, 255])),
    # 'white': (np.array([0, 0, 200]), np.array([179, 30, 255])),
    'black': (np.array([0, 0, 0]), np.array([179, 255, 30])),
    # 'gray': (np.array([0, 0, 31]), np.array([179, 30, 230])),
    'brown': (np.array([8, 70, 50]), np.array([20, 255, 255])),
    # 'cyan': (np.array([81, 70, 50]), np.array([100, 255, 255])),
    # 'magenta': (np.array([141, 70, 50]), np.array([160, 255, 255])),
    'gold': (np.array([21, 70, 50]), np.array([40, 255, 255])),
    # 'silver': (np.array([0, 0, 111]), np.array([179, 30, 190])),
    # 'maroon': (np.array([0, 70, 50]), np.array([10, 255, 255])),
    # 'navy': (np.array([100, 70, 50]), np.array([140, 255, 255])),
    # 'teal': (np.array([71, 70, 50]), np.array([100, 255, 255])),
    # 'indigo': (np.array([101, 70, 50]), np.array([130, 255, 255])),
}

color_names = {
    'red': (0, 0, 255),
    'orange': (0, 165, 255),
    'yellow': (0, 255, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'purple': (255, 0, 255),
    'pink': (255, 192, 203),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'brown': (165, 42, 42),
    'cyan': (255, 255, 0),
    'magenta': (255, 0, 255),
    'gold': (0, 215, 255),
    'silver': (192, 192, 192),
    'maroon': (0, 0, 128),
    'navy': (128, 0, 0),
    'teal': (128, 128, 0),
    'indigo': (130, 0, 75),
}

def detect_colors(frame, color_ranges):
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv_image, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color_names[color], 5)
                cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_names[color], 2)

    return frame


# cam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    processed_frame = detect_colors(frame, color_ranges)

    cv2.imshow('frame', processed_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

# **********************************************************************************************

# image
# image_dir = '/Users/dev/Desktop/*.[jJ][pP][gG,EG]'
# image_paths = glob.glob(image_dir)

# image_path = '/Users/dev/Desktop/Screenshot 2023-03-13 at 12.03.53.png'

# # Iterate over the image paths
# # for image_path in image_paths:
#     # Read the image
# image = cv2.imread(image_path)

# # Convert the image to HSV color space
# hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # Iterate over the color range and perform color detection
# for color, (lower_limit, upper_limit) in color_ranges.items():
#     mask = cv2.inRange(hsv_image, lower_limit, upper_limit)
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     if len(contours) > 0:
#         # Calculate the bounding box for the contours
#         x, y, w, h = cv2.boundingRect(contours[0])
        
#         # Draw the bounding box and label on the image
#         cv2.rectangle(image, (x, y), (x + w, y + h), lower_limit.tolist(), 2)
#         cv2.putText(image, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, lower_limit.tolist(), 2)

# # Display the image
# cv2.imshow('Color Detection', image)
# cv2.waitKey(0)

# cv2.destroyAllWindows()
