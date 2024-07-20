from time import sleep

ldr_val = 100

LDR = 0  # The pin the LDR is attached to (must be analogue)
BUTTON = 2  # The pin the button is attached to
STEPS_PER_REVOLUTION = 64  # Steps per revolution of your motor
MAX_SPEED = 30  # The maximum RPM for your motor
LIGHT_SUNRISE = 400  # The intensity of light measured by the sensor at
# sunset and sunrise
FULL_STEPS = 10000  # The step amount to get the motor from top to bottom.


class Stepper:
    """A dummy stepper class"""

    def __init__(self, steps_per_revolution, *_):
        """Create the stepper class"""
        self.steps_per_revolution = steps_per_revolution
        self.steps = 0
        self.speed = 1

    def set_speed(self, speed: int):
        """Set the speed of the stepper motor"""
        self.speed = speed

    def step(self, steps: int):
        """Move the motor by a given step number"""
        self.steps += steps
        steps_per_minute = self.steps_per_revolution * self.speed
        step_time = 60 / steps_per_minute
        sleep(step_time * abs(steps))


# Initialize the stepper on pins 8 through 11:
my_stepper = Stepper(STEPS_PER_REVOLUTION, 8, 10, 9, 11)
# my_stepper = Stepper(STEPS_PER_REVOLUTION, 11, 9, 10, 8) # Use this to
# reverse the direction.

# Stepper Motor variables
stepper_pos = 0  # Displacement of the motor in steps
stepper_target = 0  # The target motor displacement
stepper_velocity = 0  # Velocity of the motor in rpm

# LDR variables
ldr_reading = 0  # The non-raw LDR reading
last_raw_ldr_readings = [0] * 100  # The 100 most recent LDR readings
last_raw_ldr_reading_pos = 0  # First empty place in the list of raw LDR


# readings


def setup():
    # Serial.begin(9600)
    #
    # pinMode(8, OUTPUT)
    # pinMode(9, OUTPUT)
    # pinMode(10, OUTPUT)
    # pinMode(11, OUTPUT)
    # pinMode(ldr, INPUT_PULLUP)
    # pinMode(button, INPUT_PULLUP)
    pass


def loop():
    global stepper_target

    if ldr_reading > LIGHT_SUNRISE:
        stepper_target = FULL_STEPS
    else:
        stepper_target = 0

    print(stepper_pos)

    update_motor_speed()
    update_ldr_readings()


def update_ldr_readings():
    global last_raw_ldr_reading_pos, ldr_reading

    # Get the new reading and save it
    new_reading = 1023 - analog_read(LDR)
    last_raw_ldr_readings[last_raw_ldr_reading_pos] = new_reading
    last_raw_ldr_reading_pos += 1
    # Update the ldr reading
    total = 0
    for i in range(100):
        total += last_raw_ldr_readings[i]
    ldr_reading = total / 100
    # Loop the list pointer
    if last_raw_ldr_reading_pos == 100:
        last_raw_ldr_reading_pos = 0


def update_motor_speed():
    global stepper_velocity

    # Calculate the velocity
    steps_left = calculate_steps_left()
    steps_until_slowdown = calculate_steps_until_slowdown()
    if steps_until_slowdown >= 16 and steps_left > 0:
        if stepper_velocity < MAX_SPEED:
            stepper_velocity += 1

    elif steps_until_slowdown <= -16 and steps_left < 0:
        if stepper_velocity > -MAX_SPEED:
            stepper_velocity -= 1

    elif steps_until_slowdown <= 0 < steps_left:
        stepper_velocity -= 1
    elif steps_until_slowdown >= 0 > steps_left:
        stepper_velocity += 1

    # Set the velocity
    my_stepper.set_speed(abs(stepper_velocity) * 16)
    if steps_left == 0:
        return

    # Move the motor
    if 0 < steps_until_slowdown <= 16 and steps_left > 0:
        step(abs(steps_until_slowdown))
    elif 0 > steps_until_slowdown >= -16 and steps_left < 0:
        step(abs(steps_until_slowdown))
    else:
        step(16)


def calculate_steps_left():  # The step number needed to reach the target
    return stepper_target - stepper_pos


def calculate_steps_until_slowdown():  # The step number until the motor
    # starts to slow down
    steps_left = calculate_steps_left()
    if steps_left > 0:
        return steps_left - (16 * MAX_SPEED) + 16
    else:
        return steps_left + (16 * MAX_SPEED) - 16


def step(steps):
    global stepper_pos
    if stepper_velocity > 0:
        my_stepper.step(steps)
        stepper_pos += steps
    elif stepper_velocity < 0:
        my_stepper.step(-steps)
        stepper_pos -= steps


def analog_read(*_):
    return ldr_val


if __name__ == "__main__":
    setup()
    iteration = 0
    while True:
        if iteration == 50:
            ldr_val = 1000
        # elif iteration == 100:
        #     ldr_val = 100
        loop()
        iteration += 1
