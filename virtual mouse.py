import tkinter as tk
import pyautogui
import cv2
import mediapipe as mp
import time

def start_moving():
  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles #lines
  mp_hands = mp.solutions.hands #hands

  cap = cv2.VideoCapture(0)
  with mp_hands.Hands(#Hand Model
      model_complexity=0,#model 0
      min_detection_confidence=0.5, #50%
      min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
      success, image = cap.read() #camera read
      if not success:
        print("Ignoring empty camera frame.")
        continue

      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #RGB => BGR
      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          image_height, image_width, _ = image.shape
          screen_width=root.winfo_screenwidth()
          screen_height=root.winfo_screenheight()
          x_one=(screen_width)-(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * (screen_width))
          y_two=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * (screen_height+100)
          pyautogui.moveTo(x_one, y_two) #coordinates => mouse move
          mp_drawing.draw_landmarks( #output
              image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
      cv2.imshow('MediaPipe Hands', cv2.flip(image, 1)) #output video image
      if cv2.waitKey(5) & 0xFF == 27:
       
        break
  cap.release()
  cv2.destroyAllWindows()

def stop_moving():
    root.destroy()


def update_coordinates():
    while True:
        entry_x.delete(0, tk.END)
        entry_x.insert(0, pyautogui.position()[0])
        entry_y.delete(0, tk.END)
        entry_y.insert(0, pyautogui.position()[1])
        root.update()
        time.sleep(0.1)
# GUI
root = tk.Tk()
root.title("Mouse Mover")
root.geometry("500x200")

frame_input = tk.Frame(root)
frame_input.pack(pady=30)

label_x = tk.Label(frame_input, text="X Coordinate:", font=("Helvetica", 12))
label_x.pack(side="left")

entry_x = tk.Entry(frame_input, font=("Helvetica", 12), width=10)
entry_x.pack(side="left")

label_y = tk.Label(frame_input, text="Y Coordinate:", font=("Helvetica", 12))
label_y.pack(side="left", padx=30)

entry_y = tk.Entry(frame_input, font=("Helvetica", 12), width=10)
entry_y.pack(side="left")

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=30)

button_start = tk.Button(frame_buttons, text="Start", font=("Helvetica", 12), command=start_moving)
button_start.pack(side="left", padx=30)

button_stop = tk.Button(frame_buttons, text="Stop", font=("Helvetica", 12), command=stop_moving)
button_stop.pack(side="left")

root.after(0, update_coordinates)
root.mainloop()