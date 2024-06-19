import cv2
import numpy as np
import os
from PIL import Image, ImageDraw

def load_images(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
            labels.append(filename.split('.')[0])
    return images, labels

def compare_images(user_img, images, labels):
    min_diff = float('inf')
    best_match = None
    for img, label in zip(images, labels):
        diff = np.sum((user_img - img) ** 2)
        if diff < min_diff:
            min_diff = diff
            best_match = label
    return best_match

def calculate_probability(user_img, images, labels):
    probabilities = []
    for img, label in zip(images, labels):
        diff = np.sum((user_img - img) ** 2)
        probability = 1 / (1 + diff)  
        probabilities.append((label, probability))
    return probabilities

images, labels = load_images("saved_images")

canvas_size = 280
canvas = np.ones((canvas_size, canvas_size), dtype='uint8') * 255
drawing = False
last_point = None

def draw_line(event, x, y, flags, param):
    global drawing, last_point

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(canvas, last_point, (x, y), 0, 10)
            last_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

cv2.namedWindow('Canvas', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Canvas', draw_line)

while True:
    cv2.imshow('Canvas', canvas)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        canvas[:] = 255
    elif key == ord('s'):
        filename = "user_digit.png"
        cv2.imwrite(filename, canvas)
        user_img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        user_img = cv2.resize(user_img, (canvas_size, canvas_size))

        result = compare_images(user_img, images, labels)
        probabilities = calculate_probability(user_img, images, labels)
        
        print(f"ทายว่า: {result}")
        print("ค่าความคล้ายคลึง:")
        for label, prob in probabilities:
            print(f"{label}: {prob:.16f}")
            
        break
cv2.destroyAllWindows()

