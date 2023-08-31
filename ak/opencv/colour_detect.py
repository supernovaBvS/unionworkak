import cv2
import numpy as np

def color_detection(image, area):
    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the ranges for different colors in HSV
    color_ranges = {
        'red': ([0, 70, 50], [10, 255, 255]),
        'orange': ([11, 70, 50], [25, 255, 255]),
        'yellow': ([26, 70, 50], [35, 255, 255]),
        'green': ([36, 70, 50], [70, 255, 255]),
        'blue': ([100, 70, 50], [130, 255, 255]),
        'purple': ([131, 70, 50], [160, 255, 255]),
        'pink': ([161, 70, 50], [179, 255, 255]),
        'white': ([0, 0, 200], [179, 30, 255]),
        'black': ([0, 0, 0], [179, 255, 30]),
        'gray': ([0, 0, 31], [179, 30, 230]),
        'brown': ([8, 70, 50], [20, 255, 255]),
        'cyan': ([81, 70, 50], [100, 255, 255]),
        'magenta': ([141, 70, 50], [160, 255, 255]),
        'gold': ([21, 70, 50], [40, 255, 255]),
        'silver': ([0, 0, 111], [179, 30, 190]),
        'maroon': ([0, 70, 50], [10, 255, 255]),
        'navy': ([100, 70, 50], [140, 255, 255]),
        'teal': ([71, 70, 50], [100, 255, 255]),
        'indigo': ([101, 70, 50], [130, 255, 255]),
                                                    }

    
    # Extract the area for color detection
    x, y, w, h = area
    roi = hsv_image[y:y+h, x:x+w]
    
    # Iterate over each color range and check if the image matches
    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(roi, lower, upper)
        percentage = np.sum(mask == 255) / (mask.shape[0] * mask.shape[1])
        
        # Check if a significant portion of the image matches the color
        if percentage > 0.1:
            return color
    
    return 'unknown'  # Return 'unknown' if no color is detected significantly

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

# Define the dimensions and position of the color detection area
area_x = 900
area_y = 600
area_width = 30
area_height = 30

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    
    # Create a black box as the text background
    cv2.rectangle(frame, (10, 10), (300, 70), (0, 0, 0), -1)
    
    # Perform color detection
    detected_color = color_detection(frame, (area_x, area_y, area_width, area_height))

    # Display the color text on the frame
    cv2.putText(frame, 'Detected color: ' + detected_color, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Draw a box in the center for color detection
    cv2.rectangle(frame, (area_x, area_y), (area_x + area_width, area_y + area_height), (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Color Detection', frame)
    
    # Get the key pressed
    key = cv2.waitKey(1)
    
    # Move the color detection area based on arrow key presses
    if key & 0xFF == ord('w') and area_y > 0:  # Up arrow key
        area_y -= 100
    elif key & 0xFF == ord('s') and area_y + area_height < frame.shape[0]:  # Down arrow key
        area_y += 90
    elif key & 0xFF == ord('a') and area_x > 0:  # Left arrow key
        area_x -= 100
    elif key & 0xFF == ord('d') and area_x + area_height < frame.shape[1]:  # Right arrow key
        area_x += 90
    
    # Exit the loop if 'q' is pressed
    if key == 27:
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()
