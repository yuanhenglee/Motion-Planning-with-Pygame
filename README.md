<div align="center">

  <h2 align="center">Motion Planning with Pygame</h2>

  <p align="center">
    A python visualization of motion planning using potential field method and BFS
  </p>
</div>
<br />

<p align="middle">
  <img src="./pic/animation-loop.gif" width="300" />
  <img src="./pic/animation2-loop.gif" width="300" />
</p>

## Features
### Custom Map
Obstacles and robots can be set with input files (like those in `Dat`), or it can also be configured using GUI interface.
<p align="middle">
  <img src="./pic/dragndrop-loop.gif" width="600" />
</p>

### Calculating Potential Field
Two different ways( NF1, NF2 ) are used to calculate potential values.
<p align="middle">
  <img src="./pic/NF1.png" width="400" />
  <img src="./pic/NF2.png" width="400" /> 
</p>

### Pathfinding
Pathfinding using Best First Search algorithm.
<p align="middle">
  <img src="./pic/BFS.png" width="600" />
</p>


## Usage
Run:
```console
$ python3 src/run.py Dat/robot.dat Dat/obstacle.dat 
```
## Requirements
* Python 3.9.9
* Pygame 1.9.6