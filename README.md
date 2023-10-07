# Elevator App

The Elevator App is a Python project that simulates the operation of an elevator system. It includes an elevator class, passenger interactions, and a simple asynchronous event loop to manage elevator movement and passenger actions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/elevator-app.git
   cd elevator-app
   ```

2. ```python -m venv venv
   source venv/bin/activate 
   pip install -r requirements.txt
   ```

## Usage

To run the Elevator App, follow these steps:

1. Make sure you have Python 3.x installed on your system.

2. Open a terminal and navigate to the project directory:

   ```
   cd /path/to/elevator-app
   python main.py
   ```

## Project Structure

The project is organized as follows:

- `main.py`: The main script that starts the elevator simulation.
- `app/`:
  - `elevator.py`: Defines the Elevator class and its methods.
  - `misc/`: Contains utility modules such as `logger.py`, `helpers.py`, and `singleton.py`.
  - `models/`: Defines the Passenger class and related modules.
  - `passenger.py`: Contains the `PassengerAction` class for passenger interactions.
- `requirements.txt`: Lists project dependencies.
- `tests`: Unittests.


