
# CSE423_Project

🌀 __Subway Runner__

Subway Runner is a 3D OpenGL-based game where the player controls a automated moving car, avoid obstacles on the road, increase points by collecting coins, then activate superpower mode when it reaches a certain point. The game is won when the car crosses the finish line

# Contributors:

[**Mukshitur Rahman Raphy**](https://github.com/loki-ly)

[**Shakhawat Hossain**](https://github.com/shaq-bracu)



🎮 __Gameplay Overview__

* Navigate with the car.
* Move using the keys  ( ←a, d→ ).
* Toggle cameras between first-person and third-person views using the left mouse button.
* Collect 40 points to active superpower mode.
* Avoid humans crossing the road.
* Win by crossing the finishing line.
* Lose when any human is ran over.


🚗 __Car__

* Built using primitive 3D shapes (sphere, cylinder).
* Moves automatically in a straight line.
* Collision with human loses the game.
* Car movement along sideways is smooth.



🚶‍♂️ __Humans__

* Randomly spawns across the road
* Moves left to right, right to left with walking animation.
* In supermode, the humans when hit by bullet, dies and vanishes.



🪙 __Coins__

* Randomly spawns on the road
* Cannot be killed or outrun.
* Collision with it increases the score by 10 points.
* When 40 points are crossed, activated supermode.


🕹️ __Controls__

|       Action              |       Input          |           Description                         |
|---------------------------|----------------------|-----------------------------------------------|
| Move Player               | WASD keys            | Navigate sideways                             |
| Pause Game                |       `P`            | Pauses/resumes the game                       |
| Restart Game              |       `R`            | Restarts the game from the beginning          |
| Exit Game                 |       `Esc`          | Closes the game                               |




📊 __Game States__

* Win Condition: Cross the finishing line
* Lose Condition: Runover a human
* Scoreboard: Live updates on score.
* Console Feedback: Important game events are printed to the terminal.




🔧 __Dependencies__

- Python 3.x
- OpenGL (via PyOpenGL)
- GLUT (FreeGLUT or equivalent)

Ensure PyOpenGL is installed:
pip install PyOpenGL PyOpenGL_accelerate



🧠 __Inspiration & Notes__

This project was created as a Computer Graphics course assignment, focusing on transformation, camera logic, input handling, and game state management in OpenGL using Python. It showcases:

* 3D collision detection
* Object transformations
* Real-time feedback 


📜 __License__

This project is for academic and learning purposes. Feel free to fork, learn from, and build upon it!
