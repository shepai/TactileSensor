# TactileSensor

This repository focuses on the development of soft tactile sensors utilizing pressure resistors and soft padding. The project follows the successful development of software for controlling [high-resolution tactile sensors](https://github.com/shepai/RoboSkin).

## Overview

Low-resolution tactile sensors have been evaluated for performance, offering a cost-effective alternative to their high-resolution counterparts. Specifically designed for tasks involving feet, where the resolution difference has minimal impact, these sensors present an economical and practical solution.

## Project Structure

- **/code**: Holds the source code for the software controlling the low-resolution tactile sensors.
- **/assets**: Contains documentation related to the 3d print, laser cut and PCB files used

## Related Publications

Explore our related publications:

- [Slip Detection and Surface Prediction Through Bio-Inspired Tactile Feedback](https://arxiv.org/abs/2310.08192)

## Getting Started

Follow these steps to set up the project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/shepai/TactileSensor.git

## Using the code

Within the code there are two folders, sensor example code and Tactile Sensor. Tactile Sensor has the code for running on the board and on the the PC. If you are using a device with micropython select the <a href="https://github.com/shepai/TactileSensor/Code/TactileSensor/Board side/Tactile_MP.py">_MP</a> file, otherwise select the <a href="https://github.com/shepai/TactileSensor/Code/TactileSensor/Board side/Tactile_CP.py">_CP</a> one for circuitpython. If you are using Circuitpython you will not be able to use the main PC code, as it is designed to interface with a a micropython device. Circuitpython for this task is better if you are only working on hardware. 

Make sure to run the <a href="https://github.com/shepai/TactileSensor/Code/TactileSensor/Board side/boardSide.py">boardSide.py</a> on the micropython device so that it imports the library correctly.