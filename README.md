# Vision-based-smart-traffic-controller
A smart traffic light control system that utilizes Computer vision to determine green light duration times.

# Components:
1. Arduino Mega
2. LED's for traffic light simulation
3. Web Cam (External Camera)

# Data Flow and Communication 
1. Vehicle Detection: YOLOv8 processes camera input and sends vehicle counts for each road to Python.
2. Decision Making: Python calculates green light durations based on vehicle counts  and transitions the results to the Arduino via serial communication.
3. Traffic Control: Arduino implements the traffic light sequence (green → yellow → red) for the specified durations.
