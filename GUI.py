import numpy as np
import pytesseract
import cv2
from PIL import ImageFont, ImageDraw, Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image as PILImage
from PIL import ImageTk

# Khởi tạo giao diện Tkinter
root = tk.Tk()
root.title("Nhận diện chữ viết")
root.geometry("1080x720")

# Cấu hình Tesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Khởi tạo biến lưu văn bản nhận diện
recognized_text = ""

# Hàm chọn ảnh và thực hiện nhận diện chữ viết
def open_image():
    global recognized_text
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        # Đọc và xử lý ảnh
        img = cv2.imread(file_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Nhận diện chữ viết
        custom_config = r'--oem 3 --psm 6'
        boxes = pytesseract.image_to_data(img_rgb, lang="vie", config=custom_config)
        recognized_text = pytesseract.image_to_string(img_rgb, lang="vie")

        # Chuyển ảnh sang định dạng PIL để hiển thị chữ Unicode
        pil_img = PILImage.fromarray(img_rgb)
        draw = ImageDraw.Draw(pil_img)

        # Dùng font tiếng Việt
        font_path = "arial.ttf"  # Đường dẫn tới file font hỗ trợ tiếng Việt
        font = ImageFont.truetype(font_path, 20)

        # Vẽ khung và hiển thị chữ trên ảnh
        for i, b in enumerate(boxes.splitlines()):
            if i != 0:
                b = b.split()
                if len(b) == 12:
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    draw.rectangle(((x, y), (x + w, y + h)), outline="red", width=2)
                    draw.text((x, y - 20), b[11], font=font, fill=(50, 50, 255))

        # Hiển thị ảnh trên giao diện Tkinter
        img_display = ImageTk.PhotoImage(pil_img.resize((500,500)))
        img_label.config(image=img_display)
        img_label.image = img_display

# Hàm lưu văn bản vào file txt
def save_text():
    if recognized_text:
        with open("text.txt", "w", encoding="utf-8") as f:
            f.write(recognized_text)
        messagebox.showinfo("Thông báo", "Đã lưu văn bản vào file text.txt")
    else:
        messagebox.showwarning("Cảnh báo", "Chưa có văn bản nào để lưu")

# Hàm thoát khỏi giao diện
def exit_app():
    root.destroy()


# Tạo các nút trên giao diện
btn_open = tk.Button(root, text="Chọn ảnh", command=open_image)
btn_open.pack(pady=20)

btn_save = tk.Button(root, text="Xuất file", command=save_text)
btn_save.pack(pady=20)

btn_exit = tk.Button(root, text="Thoát", command=exit_app, bg="red", fg="white")
btn_exit.pack(pady=20)

# Khung hiển thị ảnh
img_label = tk.Label(root)
img_label.pack()

# Khởi chạy giao diện
root.mainloop()
