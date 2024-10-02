import torch
import cv2
import numpy as np

# Load the pre-trained YOLOv5 model from ultralytics
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_objects():
    # Initialize webcam
    camera = cv2.VideoCapture(0)

    while True:
        # Read frame from the camera
        ret, frame = camera.read()
        if not ret:
            break

        # Convert the frame from BGR to RGB (as required by YOLO)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform inference
        results = model(frame_rgb)

        # Parse the results
        labels, confidences, boxes = results.xyxyn[0][:, -1], results.xyxyn[0][:, -2], results.xyxyn[0][:, :-2]

        detected_objects = []
        # Draw bounding boxes and labels on the frame
        for i in range(len(labels)):
            x1, y1, x2, y2 = boxes[i].numpy()
            label = results.names[int(labels[i])]
            confidence = confidences[i].numpy()

            # Draw the bounding box
            cv2.rectangle(frame, (int(x1 * frame.shape[1]), int(y1 * frame.shape[0])),
                          (int(x2 * frame.shape[1]), int(y2 * frame.shape[0])),
                          (0, 255, 0), 2)

            # Put the label and confidence
            cv2.putText(frame, f"{label} {confidence:.2f}",
                        (int(x1 * frame.shape[1]), int(y1 * frame.shape[0]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            detected_objects.append(f"{label} ({confidence:.2f})")

        # Display the frame
        cv2.imshow('YOLOv5 Detection', frame)

        # Speak out detected objects
        if detected_objects:
            say("I see: " + ", ".join(detected_objects))

        # Break if the 'ESC' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release the webcam and close all windows
    camera.release()
    cv2.destroyAllWindows()
