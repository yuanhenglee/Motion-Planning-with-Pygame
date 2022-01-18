<div align="center">

  <h2 align="center">GRA Final Project</h2>

  <p align="center">
    A python visualization of motion planning using potential field method and BFS
  </p>
</div>
<br />

## Features

### Calculating Potential Field
Two different ways( NF1, NF2 ) are used to calculate the potential values.

### Pathfinding
Pathfinding using Best First Search algorithm.

### Custom Map
Obstacles and robots can be set with input files (like those in `Dat`), or it can also be configured using GUI interface.

## Usage
```shell
python3 src/run.py Dat/robot.dat Dat/obstacle.dat 
```
## Requirements
* Python 3.9.9
* Pygame 1.9.6