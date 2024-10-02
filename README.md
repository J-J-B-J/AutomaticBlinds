# AutomaticBlinds
Blinds that can be controlled with an Arduino.

Concept derived from the [Jaycar tutorial](https://www.jaycar.com.au/automatic-blinds-opener).

## Current Operation
Measures ambient light on an LDR stuck to the window.
When the light measured is greater than a set threshold, the stepper motor will pull the blinds open, and vice versa for low light levels.
Also has a button to override operation.

## Future Operation
Will replace the Arduino with an [ESP32-C3 Mini Dev Board by Waveshare](https://core-electronics.com.au/esp32-c3-mini-dev-board-risc-v-processor-wi-fi-bt5-smd-compatible.html) running [HomeSpan](https://github.com/HomeSpan/HomeSpan), allowing the blinds to be operated by Apple HomeKit.

## Circuit Diagram
![Screenshot 2024-10-02 at 11 02 01 am](https://github.com/user-attachments/assets/23ba6977-0a34-4a51-aa96-4a34931eeda0)
