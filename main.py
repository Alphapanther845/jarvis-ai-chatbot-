import speech_recognition as sr
import os
import webbrowser
import datetime
import pyttsx3
import pyautogui
import time
import cv2  # Import OpenCV
import torch

# Load YOLOv5 model (you can choose a different model if desired)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Load the small model

chatStr = ""  # Define chatStr globally
browser = None  # To store the browser instance

# Function to vocalize output
def say(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    chatStr += f"shameer: {query}\n Jarvis: "
    
    # Simple keyword-based responses
    keywords = {
        "hello": "Hello! How can I assist you today?",
        "how are you": "I'm just a program, but I'm doing well. How about you?",
        "name": "I am Jarvis, your personal assistant.",
        "time": f"Sir, the time is {datetime.datetime.now().strftime('%H:%M')}.",
        "music": "Playing your music.",
        "youtube": "Opening YouTube.",
        "sleeping": "That sounds nice! Rest is important.",
        "coding interviews": "That's great! Practice makes perfect.",
        "doing": "I'm here to assist you! What do you need help with?"
    }

    response_text = "I'm sorry, I didn't understand that."
    for keyword, response in keywords.items():
        if keyword in query.lower():
            response_text = response
            break

    say(response_text)
    chatStr += f"{response_text}\n"
    return response_text

def play_specific_video():
    global browser
    video_url = "https://www.youtube.com/watch?v=AX6OrbgS8lI&ab_channel=AUR"
    browser = webbrowser.open(video_url)  # Open the specific video URL
    say("Now playing the specified video.")

def stop_video():
    say("Stopping the video.")
    time.sleep(2)  # Wait for a moment to ensure the video is playing
    pyautogui.press('space')  # Press Space to pause/play the video

def open_camera():
    # Open the camera and display the video feed
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    say("Opening the camera. Press 'q' to close the camera.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Camera', frame)  # Show the video feed
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close the video window

def detect_objects(frame):
    # Convert the frame to a format suitable for YOLOv5
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    results = model(img)  # Perform inference
    
    # Parse results
    detected_objects = results.names  # Get class names
    detections = results.xyxy[0]  # Get bounding box coordinates
    detected_labels_with_positions = []

    for *box, conf, cls in detections:
        label = f"{detected_objects[int(cls)]} ({conf:.2f})"  # Get label and confidence
        position = "in front of me"  # You can modify this for more precise positions
        detected_labels_with_positions.append((label, position))  # Store label with position

    return detected_labels_with_positions  # Return the list of detected objects with positions

def detect_and_say_object(frame):
    detected_objects_with_positions = detect_objects(frame)  # Run object detection
    
    if detected_objects_with_positions:
        responses = []
        for obj, position in detected_objects_with_positions:
            responses.append(f"I see a {obj} {position}.")
        response = " ".join(responses)
    else:
        response = "I couldn't detect anything in front of me."

    # Speak the response
    say(response)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"Error: {e}")
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Welcome to Jarvis A.I")
    
    while True:
        query = takeCommand()
        
        if "play video" in query.lower():
            play_specific_video()  # Play the specific video

        elif "stop it" in query.lower():
            stop_video()  # Stop video playback

        elif "open camera" in query.lower():
            open_camera()  # Open the camera

        elif "what is this" in query.lower() or "what is in front of me" in query.lower():
            cap = cv2.VideoCapture(0)  # Open camera for detection
            ret, frame = cap.read()  # Capture a single frame
            if ret:
                detect_and_say_object(frame)  # Detect and say the object
            cap.release()  # Release the camera

        elif "open music" in query.lower():
            musicPath = "path/to/your/music.mp3"  # Update with your music file path
            os.system(f"start {musicPath}")  # Use start for Windows

        elif "the time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes.")

        elif "open facetime" in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass" in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "jarvis quit" in query.lower():
            say("Goodbye sir!")
            exit()

        elif "reset chat" in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
