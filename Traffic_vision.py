import threading
import cv2
from ultralytics import YOLO
import tkinter as tk
from tkinter import messagebox
import serial
import time
import logging

# Load the YOLOv8 model and set logging Level to WARNING to suppress info/debug messages
logging.getLogger('ultralytics').setLevel(logging.WARNING)
model = YOLO('yolov8n.pt')

# Initialize global variables
running = False
vehicle_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
vehicle_counts_lock = threading.Lock()
                  
# Set up the serial connection to the Arduino
arduino = serial.Serial('COM6', 9600, timeout=1)
                  
# Define regions of interest (ROIs) for each road (A, B, C, D)
def define_rois(frame):
    height, width, _ = frame.shape
    rois = {
        "A": frame [0:height//2, 0:width//2],
        "B": frame [0:height//2, width//2:width],
        "C": frame [height//2:height, 0:width//2],
        "D": frame [height//2:height, width//2:width]
    }

    return rois
                  
#Function to get vehicle count from the camera feed for each ROI
def update_vehicle_counts():
    global vehicle_counts
    cap = cv2.VideoCapture(0) # Single camera for all four roads
    while running:
        ret, frame = cap.read()
        if not ret:
            continue
                  
        rois = define_rois(frame)
        new_counts = {}

        for road, roi in rois.items():
            results = model(roi)
            new_counts[road] = sum(1 for r in results[0].boxes if r.cls == 2) #Class '2' is for vehicles

        #Lock the variable update to ensure thread safety
        with vehicle_counts_lock:
            vehicle_counts = new_counts

        print(f"Vehicle Counts: {vehicle_counts}")


        # Display the annotated frame for monitoring
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow("Traffic Light Control System", annotated_frame)
                  
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                  
    cap.release()
    cv2.destroyAllWindows()
                  
#Function to send commands to Arduino
def send_command_to_arduino(road, green_time):
    try:
        command = f"{road}{green_time}\n"
        arduino.write(command.encode())
        print(f"Sent command: {command.strip()}")
        while True:
            if arduino.in_waiting > 0:
                response = arduino.readline().decode().strip()
                if response == "DONE":
                    break
    except Exception as e:
        print(f"Error sending command: {e}")
                  
                  
#Function to control traffic Lights based on vehicle counts and print only relevant info
def control_traffic_lights_in_sequence():
    global vehicle_counts
    while running:
        for road in ['A', 'B', 'C', 'D']:
            with vehicle_counts_lock:
                count = vehicle_counts.get(road, 0)
                green_light_duration = max(5, min(30, 5 + 2 * count)) #Calculate green light time
                
                #Print only relevant information
                print(f"Road {road}: Vehicles Detected = {count}, Green Light Duration = {green_light_duration} seconds")
                
                #Send command to Arduino with only green Light duration
                send_command_to_arduino(road, green_light_duration * 1000) # in milliseconds
                time.sleep(green_light_duration + 3 + 1) #Total time before moving to next road
                
                
# Threaded function to run the traffic light system
def start_traffic_light_system():
    global running
    running = True
    
    # Start detection thread
    detection_thread = threading.Thread(target=update_vehicle_counts)
    detection_thread.start()
    
    # Start traffic light control thread
    control_thread = threading.Thread(target=control_traffic_lights_in_sequence)
    control_thread.start()


#Stop the traffic light system
def stop_traffic_light_system():
    global running
    running = False
    messagebox.showinfo("Info", "Traffic light system stopped!")


#Set up the Tkinter window
def create_gui():
    root = tk.Tk()
    root.title("4-Way Smart Traffic Light System with One Camera")
    
    start_button = tk.Button(root, text="Start", command=start_traffic_light_system)
    start_button.pack(pady=20)
    
    stop_button = tk.Button(root, text="Stop", command= stop_traffic_light_system)
    stop_button.pack(pady=20)
    
    root.mainloop()


# Main check to run the GUI
if __name__ == "__main__":
    running = False
    create_gui()