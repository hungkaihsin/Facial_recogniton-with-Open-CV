import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER

# GUI
# root menu

window = tk.Tk()
window.title('GUI')
window.geometry('455x140')
window.resizable(False, False)
window.iconbitmap('icon.ico')


# Entry

load_file = ttk.Entry(width=55)
load_file.place(x=40, y=0)



# buttom

# Label
lb_file_path = ttk.Label(text='Route', background='gray', foreground='white')
lb_file_path.place(x=0, y=0)


window.mainloop()






















# facial recognition function

'''
image_path = 'input_image.jpg'
image = cv2.imread(image_path)



# in order to elavate the efficency, turn image to grayscale

grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

'''
'''
print(grey_image.shape)

'''


'''

# load classifier in cv2
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

face = face_classifier.detectMultiScale(
    grey_image, scaleFactor = 1.1, minNeighbors = 5, minSize = (40, 40)
)

for (x, y, w, h) in face:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)

rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure(figsize = (20, 10))
plt.imshow(rgb_image)
plt.axis('off')
plt.show()

'''