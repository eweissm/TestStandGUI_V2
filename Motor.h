#ifndef Motor_h
#define Motor_h

#include <Arduino.h>


class Motor {

public:
  Motor(int pin1, int pin2);

  void run(int direction, int speed);

  void runUntil(float currentLocation, float targetLocation, float positionTolerance);


private:
  int _pin1;
  int _pin2;
};

#endif