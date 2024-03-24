import cv2
import matplotlib.pyplot as plt



image_path = 'input_image.jpg'
image = cv2.imread(image_path)
'''
print(image.shape)

'''
# in order to elavate the efficency, turn image to grayscale

grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

'''

print(grey_image.shape)

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
