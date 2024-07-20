#include <Stepper.h>

#define ldr A0                 // The pin the LDR is attached to (must be analogue)
#define button 2               // The pin the button is attached to
#define stepsPerRevolution 64  // The number of steps per revolution of your motor
#define maxSpeed 30            // The maximum RPM for your motor
#define lightSunrise 400       // The intensity of light measured by the sensor at sunset and sunrise
#define fullSteps 10000        // The step amount to get the motor from top to bottom


// Initialize the stepper on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);
// Stepper myStepper(stepsPerRevolution, 11, 9, 10, 8);  // Use this to reverse the direction.

// Stepper Motor variables
int stepperPos = 0;       // Displacement of the motor in steps
int stepperTarget = 0;    // The target motor displacement
int stepperVelocity = 0;  // Velocity of the motor in rpm

// LDR variables
int ldrReading = 0;            // The non-raw LDR reading
int lastRawLdrReadings[100];   // The 100 most recent LDR readings
int lastRawLdrReadingPos = 0;  // First empty place in the list of raw LDR readings


void setup() {
  Serial.begin(9600);

  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(ldr, INPUT_PULLUP);
  pinMode(button, INPUT_PULLUP);
}

void loop() {
  if (ldrReading > lightSunrise) {
    stepperTarget = fullSteps;
  } else {
    stepperTarget = 0;
  }
  if (digitalRead(button)) {
    stepperTarget = fullSteps - stepperTarget;
  }

  if (Serial.availableForWrite()) {
    Serial.print(digitalRead(button));
    Serial.print(" ");
    Serial.println(stepperPos);
  }

  update_motor_speed();
  update_ldr_readings();
}

void update_ldr_readings() {
  // Get the new reading and save it
  int newReading = 1023 - analogRead(ldr);
  lastRawLdrReadings[lastRawLdrReadingPos] = newReading;
  lastRawLdrReadingPos++;
  // Update the ldr reading
  long sum = 0;
  for (int i = 0; i < 100; i++) {
    sum += lastRawLdrReadings[i];
  }
  ldrReading = sum / 100;
  // Loop the list pointer
  if (lastRawLdrReadingPos == 100) {
    lastRawLdrReadingPos = 0;
  }
}

void update_motor_speed() {
  // Calculate the velocity
  int stepsLeft = calculate_steps_left();
  int stepsUntilSlowdown = calculate_steps_until_slowdown();
  if (stepsUntilSlowdown >= 16 && stepsLeft > 0) {
    if (stepperVelocity < maxSpeed) {
      stepperVelocity++;
    }
  } else if (stepsUntilSlowdown <= -16 && stepsLeft < 0) {
    if (stepperVelocity > -maxSpeed) {
      stepperVelocity--;
    }
  } else if (stepsUntilSlowdown <= 0 && stepsLeft > 0) {
    stepperVelocity--;
  } else if (stepsUntilSlowdown >= 0 && stepsLeft < 0) {
    stepperVelocity++;
  }
  // Set the velocity
  myStepper.setSpeed(abs(stepperVelocity) * 16);
  if (stepsLeft == 0) { return; }

  // Move the motor
  if (0 < stepsUntilSlowdown && stepsUntilSlowdown <= 16 && stepsLeft > 0) {
    step(abs(stepsUntilSlowdown));
  } else if (0 > stepsUntilSlowdown && stepsUntilSlowdown >= -16 && stepsLeft < 0) {
    step(abs(stepsUntilSlowdown));
  } else {
    step(16);
  }
}

int calculate_steps_left() {  // The step number needed to reach the target
  return stepperTarget - stepperPos;
}

int calculate_steps_until_slowdown() {  // The step number until the motor starts to slow down
  int stepsLeft = calculate_steps_left();
  if (stepsLeft > 0) {
    return stepsLeft - (16 * maxSpeed) + 16;
  } else {
    return stepsLeft + (16 * maxSpeed) - 16;
  }
}

void step(int steps) {
  if (stepperVelocity > 0) {
    myStepper.step(steps);
    stepperPos += steps;
  } else if (stepperVelocity < 0) {
    myStepper.step(-steps);
    stepperPos -= steps;
  }
}
