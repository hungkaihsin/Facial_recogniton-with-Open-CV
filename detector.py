import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER
from tkinter import filedialog

# GUI
# root menu

window = tk.Tk()
window.title('Facial Recognition')
window.geometry('455x90')
window.resizable(False, False)
window.iconbitmap('icon.ico')


# Entry

Entry_load_file = ttk.Entry(width=55)
Entry_load_file.place(x=40, y=1)





# Label
lb_file_path = ttk.Label(text='Route', background='gray', foreground='white')
lb_file_path.place(x=0, y=1)


# function

def load_file():
    if Entry_load_file.get() is None:
        file_path = filedialog.askopenfilename(filetypes=(('jpg files', '*.jpg'), ('all files', '*.*')))
        Entry_load_file.insert(0, file_path)
    else:
        file_path = filedialog.askopenfilename(filetypes=(('jpg files', '*.jpg'), ('all files', '*.*')))
        Entry_load_file.delete(0, 'end')
        Entry_load_file.insert(0, file_path)

def detector():
    image_path = Entry_load_file.get()
    image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    face = face_classifier.detectMultiScale(
    grey_image, scaleFactor = 1.1, minNeighbors = 5, minSize = (40, 40)
    )

    for (x, y, w, h) in face:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    plt.figure(figsize = (5, 5))
    plt.imshow(rgb_image)
    plt.axis('off')
    plt.show()

def test():
    image_path = Entry_load_file.get()
    image = cv2.imread(image_path)
    plt.imshow(image)
    plt.show()



# buttom
Btn_select_file = ttk.Button(text='Select file', command= load_file)
Btn_select_file.place(x=380, y=0)
Btn_detect = ttk.Button(text="Detect", command= detector)
Btn_detect.place(x=230, y=60, anchor= CENTER)


window.mainloop()







