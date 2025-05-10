# Game Zone: Command-Line Guessing Games

Welcome to **Game Zone**, a fun and interactive command-line game built in Python! This game offers two exciting guessing games: **Number Guessing Game** and **Word Guessing Game**. Test your wits as the computer tries to guess your number or word through a series of questions, or challenge it to guess correctly in as few attempts as possible!

## Overview

Game Zone is a Python-based command-line application that provides two games:
1. **Number Guessing Game**: Think of a number between 1 and 50, and the computer will try to guess it by asking if its guess is correct, higher, or lower.
2. **Word Guessing Game**: Choose a word from a predefined list, and the computer will attempt to guess it by asking yes/no/maybe questions about its properties (e.g., "Is it a living thing?").

The game tracks how many times you’ve played each game and displays a summary when you exit. It’s simple to run, easy to play, and a great way to explore interactive Python applications!

## Prerequisites

To play Game Zone, you need:
- **Python 3.11 or higher** installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- A terminal or command-line interface (e.g., Command Prompt on Windows, Terminal on macOS/Linux).
- The required Python packages (listed below).

## Installation

1. **Clone or Download the Repository**:
   - If using Git, clone the repository:
     ```bash
     git clone <repository-url>
     cd game-zone
     ```
   - Alternatively, download the project as a ZIP file and extract it.
     ```


## Usage

1. **Run the Game**:
   - Navigate to the project directory in your terminal:
     ```bash
     cd game-zone
     ```
   - Start the game by running:
     ```bash
     python main.py
     ```

2. **Follow the Instructions**:
   - The game will display a menu:
     ```
     Welcome to the Game Zone!
     Choose a game to play:
     1. Number Guessing Game
     2. Word Guessing Game
     3. Exit
     Enter your choice (1-3):
     ```
   - Enter `1`, `2`, or `3` to select an option.

3. **Playing the Games**:
   - **Number Guessing Game**:
     - Think of a number between 1 and 50.
     - The computer guesses a number and asks if it’s correct, higher, or lower (e.g., "Is your number 25? (yes/higher/lower):").
     - Respond with `yes`, `higher`, or `lower` until the computer guesses your number or reaches the maximum attempts (10).
     - On success, you’ll see a celebratory message (e.g., "Woohoo! I nailed it!").
   - **Word Guessing Game**:
     - Choose a word from the displayed list (e.g., `apple, chair, elephant, guitar, rocket, pencil, pizza, tiger`).
     - The computer asks up to 5 yes/no/maybe questions (e.g., "Is your word something you can eat?").
     - Respond with `yes`, `no`, or `maybe`.
     - The computer guesses a word (up to 2 guesses per attempt) and asks if it’s correct (e.g., "I think your word is: pencil. Was I correct? (yes/no):").
     - If wrong, it may try another guess or start a new attempt with new questions.

4. **Exiting the Game**:
   - Select option `3` from the main menu.
   - The game displays a summary of your play history:
     ```
     Great!
     You have played Number Game X times and Word Game Y times.
     ```


## Dependencies

- `langgraph`: Used for state graph management to handle game flow and transitions.
  Install with:
  ```bash
  pip install langgraph
  ```

You can create a `requirements.txt` file with:
```
langgraph
```
Then install dependencies using:
```bash
pip install -r requirements.txt
```


## Contributing

Feel free to contribute by:
- Adding new game modes or features.
- Improving the user interface (e.g., colored output with `colorama`).
- Enhancing the AI guessing algorithms.
- Fixing bugs or improving documentation.

To contribute:
1. Fork the repository.
2. Create a branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to your fork (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details (if included).

## Acknowledgments

- Built with [LangGraph](https://langchain-ai.github.io/langgraph/) for state management.
- Inspired by classic guessing games like 20 Questions and Number Guessing.
- Thanks to the Python community for excellent libraries and resources.

Enjoy playing Game Zone, and have fun outsmarting the computer!
