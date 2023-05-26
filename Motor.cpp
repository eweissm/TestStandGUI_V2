
#include "Arduino.h"
#include "Motor.h"

Motor::Motor(int pin1, int pin2) {

  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);

  _pin1 = pin1;
  _pin2 = pin2;
}

void Motor::run(int direction, int speed) {

 // run the motor object in the directions (0= forward; 1= backwards)
  // at the specified speed (0 to 255)

  if (direction == 0)  //if direction is forward
  {
    digitalWrite(_pin1, speed);
    digitalWrite(_pin2, 0);
  } else if (direction == 1)  //if direction is backwards
  {
    digitalWrite(_pin2, speed);
    digitalWrite(_pin1, 0);
  } else { 
    digitalWrite(_pin2, 0);
    digitalWrite(_pin1, 0);   
    Serial.println("Invalid direction called in 'run' function");
  }

}


void Motor::runUntil(float currentLocation, float targetLocation, float positionTolerance) {
 if(currentLocation-positionTolerance >= targetLocation) //move up
  {
    digitalWrite(_pin2, HIGH);
    digitalWrite(_pin1, LOW);
  }else if(currentLocation+positionTolerance <= targetLocation){//move down
    digitalWrite(_pin1, HIGH);
    digitalWrite(_pin2, LOW);
  }else{ //stop
    digitalWrite(_pin1, LOW);
    digitalWrite(_pin2, LOW);
  }
}



