# MBRDI-hackathon
This project was created for Mercedes Benz Autonomous Tech Challenge. The project specifications can be found in the .pdf files in the mercedes folder.

## Prerequisites
The scripts use CARLA Simulator's PythonAPI and OpenDrive parser. Hence you need to have CARLA installed on your local machine.

## Installation
Please refer to [CARLA's documentation](https://carla.readthedocs.io/) for installation instructions.

## Usage
Follow CARLA's documentaion to use the .fbx and .xodr files to generate a map on the simulator. Next run the simulator after loading the map.

To run the vehicle and record the depth map and point cloud as .ply files, run the python script vehicle.py as:
```bash
python vehicle.py
```
To extract and segment the point cloud into traffic signs, road markings, etc. , compile and run the opendrive.cpp file.
```bash
g++ -std=c++14 *.h *.cpp parser/*.h parser/*.cpp parser/pugixml/*.hpp parser/pugixml/*.cpp
./a.out
```
