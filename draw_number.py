import cv2
import numpy as np
import os

#ขนาดของรูปภาพที่จะเก็บ
image_size = 280 

save_folder = 'saved_images'
os.makedirs(save_folder, exist_ok=True)

canvas = np.ones((image_size, image_size), dtype='uint8') * 255
cv2.namedWindow('Canvas', cv2.WINDOW_NORMAL)  

# กำหนดค่าเริ่มต้น
drawing = False  # สถานะการวาด
last_point = None  # จุดสุดท้ายที่วาด

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

cv2.setMouseCallback('Canvas', draw_line)

while True:
    cv2.imshow('Canvas', canvas)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # กด 'c' เพื่อล้างภาพ
        canvas[:] = 255
    elif key == ord('s'):  # กด 's' เพื่อบันทึกภาพ
        filename = input("กรุณาป้อนเลขที่วาด (0-9): ")
        filename = filename.strip()
        if filename.isdigit() and len(filename) == 1:
            filename = os.path.join(save_folder, f"{filename}.png")
            cv2.imwrite(filename, canvas)
            print(f"บันทึกภาพเป็น {filename}")
        else:
            print("โปรดป้อนเลข 0-9 เท่านั้น")
    elif key == ord('q'):  # กด 'q' เพื่อออกจากโปรแกรม
        break
cv2.destroyAllWindows()
