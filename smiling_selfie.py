import cv2   # pip install opencv-python
import mediapipe as mp  # pip install mediapipe - a machine learning framework that offers fast and accurate face tracking
import pyautogui
import winsound    # library used for producing sound when a photo is captured
import os # for making new directory to save the captured pictures
import time


x1=0
x2=0
y1=0
y2=0

# create a directory to save the captured pictures
save_dir = "Captured_selfies"
if not os.path.exists(save_dir):
   os.makedirs(save_dir)

# checking if the folder is empty or filled, if filled from where the numbering of new saved selfies shall begin
existing_files= os.listdir(save_dir)

if existing_files:
   photo_count = max([int(f.split("_")[1].split(".")[0]) for f in existing_files if f.startswith("selfie_")]) + 1
else:
   photo_count=1
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks= True) # capturing accurate images
camera = cv2.VideoCapture(0)  # here only one camera is there so '0' else 1,2 3, etc can be used

# if camera is successfully capturing then the while loop will be true and hence will run
while True:
    _ , image =camera.read()   # camera read is a function with two variables in which we dont want first variable hence we keep it as ' _ ' and other we need is image, this function returns captured image
    image = cv2.flip(image,1)#to avoid lateral inversion, and 1 is used because we are fliping it in respect to y axis 
    fh, fw, _ = image.shape
    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # since image captured is in BGR, we need to convert into RGB image
    output = face_mesh.process(rgb_image)
    landmark_points= output.multi_face_landmarks # capturing the landmarks of multiple faces but we need only our face so we keep if condition
    if landmark_points:
        landmarks = landmark_points[0].landmark  # capturing only the first landmark 
        for id, landmark in enumerate(landmarks):
            x=int(landmark.x * fw)
            y= int(landmark.y * fh)
            if id == 43:
               x1 = x
               y1 = y
            if id == 287:
               x2=x
               y2=y 
        dist = int(((x2-x1)**2 + (y2-y1)**2 ) ** (0.5))
        print(dist)  # distance if more then 100 means you are smiling
        if dist >55:
           
           image_path = os.path.join(save_dir, f"selfie_{photo_count}_clicked.png")
           cv2.imwrite(image_path,image)
           print(f"Saved: {image_path}")
           
           winsound.PlaySound("clicksound.wav",winsound.SND_FILENAME)
           photo_count +=1
           #time.sleep(1)
           cv2.waitKey(100)

    cv2.imshow(' auto selfie for smiling face', image)
    key = cv2.waitKey(1)  & 0xFF # any value/ key wll work but if the key is 'esc' = 27 ascii value
    if key== 27:
       break
 # close window of the camera
camera.release()
cv2.destroyAllWindows()


