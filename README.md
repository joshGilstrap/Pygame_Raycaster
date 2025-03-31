# Pygame Raycaster

This project is a simple 3D raycaster implemented using Pygame, inspired by classic first-person shooters. It renders a basic 3D environment from a 2D map, allowing the player to move and rotate within the generated world.
![Recording2025-03-31052848-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/100f16cf-74ea-471f-83a1-65950d80de93)


## Features

* **3D Raycasting:** Renders a 3D environment from a 2D map.
* **Player Movement:** Allows the player to move forward, backward, left, and right, as well as rotate.
* **Collision Detection:** Prevents the player from moving through walls.
* **Minimap:** Displays a small minimap in the corner of the screen.
* **FPS Display:** Shows the current frames per second.
* **Movement Instructions:** Displays movement instructions on screen.
* **Normalized Diagonal Movement:** Ensures consistent movement speed regardless of direction.

## Getting Started

### Prerequisites

* Python 3.x
* Pygame (`pip install pygame`)

### Installation

1.  Clone the repository:

    ```bash
    git clone [https://github.com/joshgilstrap/pygame-raycaster.git](https://www.google.com/search?q=https://github.com/joshgilstrap/pygame-raycaster.git)
    cd pygame-raycaster
    ```

2.  Run the game:

    ```bash
    python raycaster.py
    ```

### Controls

* `W`: Move forward
* `S`: Move backward
* `A`: Move left
* `D`: Move right
* `Left Arrow`: Rotate left
* `Right Arrow`: Rotate right

## Code Structure

* `raycaster.py`: Contains the main game logic and rendering code.

## Code Explanation

* **`is_wall(x, y)`:** Checks if a given coordinate is a wall in the game map.
* **`handle_player_input(elapsed_time)`:** Handles player movement and rotation based on key presses.
* **`perform_raycasting()`:** Performs the raycasting algorithm to render the 3D environment.
* **`draw_mini_map()`:** Draws the minimap in the corner of the screen.
* **`draw_info(fps)`:** Displays the FPS and movement instructions.

## Contributing

Contributions are welcome! Please feel free to submit a pull request with any improvements or bug fixes.

## License

This project is licensed under the MIT License.
