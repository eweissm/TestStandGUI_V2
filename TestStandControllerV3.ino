//Test Stand Controller V3
//By: Eric Weissman
//Date: 05/23/2023

#include "Motor.h"

//Lable Pins
//  actuators
#define r1_A 31
#define r1_B 30

#define r2_A 32
#define r2_B 33

#define l1_A 40
#define l1_B 42

#define l2_A 50
#define l2_B 52

//  wire feeder
#define wf_A 43
#define wf_B 45

//  distance sensors
#define trigPin_L 5
#define trigPin_R 7

#define echoPin_L 4
#define echoPin_R 6

//duration for signal to return from ultrasonic sensor
long duration;

//distance from sensors to z platform
float distance_L;
float distance_R;

//Sensor reading offset (distance between actuator's zero and actual zero
float offset = 10;

//Wire feeder feed rate (0 to 255)
int feedRate = 255;

//allowable error in the positioning of the actuator
float positionTolerance = .2;

//arbitrarily defining the target location for the actuators
float targetPosition = 5;

//The number of sensor reading to keep which will be used for a moving average
const int numValues = 10;

//array of previous sensor values used for moving average
float readings_R[numValues];
float readings_L[numValues];

//sums of readings
float total_R = 0;
float total_L = 0;

//index of current reading
int readIndx = 0;

// variables stores serial data
int incomingByte;
String input;

//bool for slecting between manual and auto control. True = manual control
bool ManualControl = true;

//Actuator selection for manual control. 0=both, 1= Left, 2= right
int ActuatorSelection = 0;

//Create Motor objects
Motor R1(r1_A, r1_B);
Motor R2(r2_A, r2_B);
Motor L1(l1_A, l1_B);
Motor L2(l2_A, l2_B);

Motor WF(wf_A, wf_B);



void setup() {
  Serial.begin(9600);

  //pinmodes for sensor pins
  pinMode(trigPin_L, OUTPUT);  // Sets the trigPin as an Output
  pinMode(echoPin_L, INPUT);   // Sets the echoPin as an Input
  pinMode(trigPin_R, OUTPUT);  // Sets the trigPin as an Output
  pinMode(echoPin_R, INPUT);   // Sets the echoPin as an Input

  //set reading arrays to all zeros
  for (int i = 0; i < numValues; i++) {
    readings_R[i] = 0;
    readings_L[i] = 0;
  }
}


void loop() {

  //Get distance reading from sensors
  distance_L = getUltrasonicSensorDistance(echoPin_L, trigPin_L)-offset;
  distance_R = getUltrasonicSensorDistance(echoPin_R, trigPin_R)-offset;

  //          Computing the rolling avg------------------------------------------------------------------------------------------------------

  //subtract the last value in the loop
  total_R = total_R - readings_R[readIndx];
  total_L = total_L - readings_L[readIndx];

  //Replace last value with new value from sensor
  readings_R[readIndx] = distance_R;
  readings_L[readIndx] = distance_L;

  //add new value to the total
  total_R = total_R + readings_R[readIndx];
  total_L = total_L + readings_L[readIndx];

  //advance the index reading
  readIndx++;

  //check to see if readIndx is greater than the number of values. if so, wrap indx back to 03
  if (readIndx >= numValues) {
    readIndx = 0;
  }

  //compute average of readings
  float avgDist_R = total_R / numValues;
  float avgDist_L = total_L / numValues;

  Serial.print("Left Distance reading:");
  Serial.print(distance_R);

  Serial.print("     Avg:");
  Serial.println(avgDist_R);

  //delay for code stability
  delay(10);
  //run wire feeder forward at specified feed rate--------------------------------------------------------------------------------------
  WF.run(0, feedRate);

  // read GUI and follow Commands------------------------------------------------------------------------------------------------------------
  if (Serial.available()) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();

    //Update manual or automatic control selection
    if (incomingByte == 'M') {
      ManualControl = true;
      R1.run(0, 0);
      R2.run(0, 0);
      L1.run(0, 0);
      L2.run(0, 0);
    } else if (incomingByte == 'A') {
      ManualControl = false;
    }

    //manual control------------------------
    if (ManualControl) {

      if (incomingByte == 'B') {
        ActuatorSelection = 0;

      } else if (incomingByte == 'L') {
        ActuatorSelection = 1;

      } else if (incomingByte == 'R') {
        ActuatorSelection = 2;

      } else if (incomingByte == 'U') {

        switch (ActuatorSelection) {
          case 0:
            R1.run(0, 255);
            R2.run(0, 255);
            L1.run(0, 255);
            L2.run(0, 255);
            break;
          case 1:
            L1.run(0, 255);
            L2.run(0, 255);
            break;
          case 2:
            R1.run(0, 255);
            R2.run(0, 255);
            break;
          default:
            break;
        }
        delay(500);
        R1.run(0, 0);
        R2.run(0, 0);
        L1.run(0, 0);
        L2.run(0, 0);

      } else if (incomingByte == 'D') {

        switch (ActuatorSelection) {
          case 0:
            R1.run(1, 255);
            R2.run(1, 255);
            L1.run(1, 255);
            L2.run(1, 255);
            break;
          case 1:
            L1.run(1, 255);
            L2.run(1, 255);
            break;
          case 2:
            R1.run(1, 255);
            R2.run(1, 255);
            break;
          default:
            break;
        }
        delay(500);
        R1.run(0, 0);
        R2.run(0, 0);
        L1.run(0, 0);
        L2.run(0, 0);
      }
    }
    // Automated Controls--------------------------------------------------------------------------------------------------
    if (!ManualControl) {
      if (incomingByte == 'V') {
        input = Serial.readStringUntil('E');
        targetPosition = input.toInt();
        Serial.println(input);
      }
    }
  }


  //If on automated controls run actuators until they are at the targeted location
  if (!ManualControl) {
    R1.runUntil(avgDist_R, targetPosition, positionTolerance);
    R2.runUntil(avgDist_R, targetPosition, positionTolerance);
    L1.runUntil(avgDist_L, targetPosition, positionTolerance);
    L2.runUntil(avgDist_L, targetPosition, positionTolerance);

  }

}

//This Function takes an echoPin and a trigPin and returns the Distance from an ultrasonic sensor in cm
float getUltrasonicSensorDistance(int echoPin, int trigPin) {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculate and return the distance
  return (duration * 0.034 / 2);
  input = "";
}
