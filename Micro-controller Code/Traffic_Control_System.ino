// Define LED pins for each road
#define ledA1 2 // Green LED for road A
#define ledA2 3 // Yellow LED for road A
#define ledA3 4 // Red LED for road A

#define ledB1 5 // Green LED for road B
#define ledB2 6 // Yellow LED for road B
#define ledB3 7 // Red LED for road B

#define ledC1 8 // Green LED for road c
#define ledC2 9 // Yellow LED for road C
#define ledC3 10 // Red LED for road C

#define ledD1 12 // Green LED for road D
#define ledD2 11 // Yellow LED for road D
#define ledD3 13 // Red LED for road D

int yellowTime = 3000; // Yellow light fixed at 3 seconds
int redDelay = 1000;   // 1-second delay before turning on the red light

void setup() {
  // Initialize LED pins as OUTPUT
  pinMode(ledA1, OUTPUT); pinMode(ledA2, OUTPUT); pinMode(ledA3, OUTPUT);
  pinMode(ledB1, OUTPUT); pinMode(ledB2, OUTPUT); pinMode(ledB3, OUTPUT);
  pinMode(ledC1, OUTPUT); pinMode(ledC2, OUTPUT); pinMode(ledC3, OUTPUT);
  pinMode(ledD1, OUTPUT); pinMode(ledD2, OUTPUT); pinMode(ledD3, OUTPUT);
  
  // Start the serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char road Serial.read();         // Read which road gets the green light (A, B, C, D)
    int greenTime Serial.parseInt(); // Read the green light duration in milliseconds
    
    if (greenTime > 0) {
      controlTrafficLights (road, greenTime); // Control lights for the selected road
    }
  }
}


void controlTrafficLights(char road, int greenTime) {
  // Switch based on the road identifier
  switch (road) {
    case 'A':
      controlRoad(ledA1, ledA2, ledA3, greenTime, ledB3, ledC3, ledD3); // Control Lights for road A
      break;
    case 'B':
      controlRoad(ledB1, ledB2, ledB3, greenTime, ledA3, ledC3, ledD3); // control lights for road B
      break;
    case 'C':
      controlRoad(ledC1, ledC2, ledC3, greenTime, ledB3, ledA3, ledD3); // Control lights for road C
      break;
    case 'D':
      controlRoad(ledD1, ledD2, ledD3, greenTime, ledB3, ledC3, ledA3); // Control lights for road D
      break;
    default:
      break;
  }
}

void controlRoad(int greenPin, int yellowPin, int redPin, int greenTime, int redi, int red2, int red3) {
  // Green Light ON
  digitalWrite(red1, HIGH);
  digitalWrite(red2, HIGH);
  digitalWrite(red3, HIGH);
  
  digitalWrite(greenPin, HIGH);
  digitalWrite(redPin, LOW);   // Turn off red light if it was ON
  delay(greenTime);            // Keep the green light ON for greenTime
  digitalWrite(greenPin, LOW); // Turn off green light
  
  // Yellow Light ON
  digitalWrite(yellowPin, HIGH);
  delay(yellowTime);            // Keep the yellow light ON for 3 seconds
  digitalWrite(yellowPin, LOW); // Turn off yellow light
  
  delay(redDelay);  // Red Light Delay (1 second)
  
  // Red Light ON
  digitalWrite(redPin, HIGH); // Turn ON red light after yellow light
  Serial.println("DONE");
}
