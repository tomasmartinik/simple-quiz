# Simple Quiz

Simple Quiz is an interactive flashcard application built with Streamlit. It allows users to study and review flashcards, track their progress, and load custom sets of flashcards.

## Features

- **Interactive Flashcards**: View questions, reveal answers, and mark them as known or unknown.
- **Progress Tracking**: Track the number of cards viewed, known, and unknown.
- **Customizable Sets**: Load custom flashcard sets from the `sets` folder.
- **Review Mode**: Focus on cards marked as unknown.
- **Shuffle and Reset**: Shuffle cards or reset their order.

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:tomasmartinik/simple-quiz.git
   cd simple-quiz
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run main.py
   ```

## Folder Structure

- `main.py`: The main application file.
- `conf/`: Configuration files for custom sets.
- `sets/`: Folder containing JSON files for flashcard sets.
  - Example: `sample_set.json`

## Usage

1. Start the application by running `streamlit run main.py`.
2. Use the sidebar to:
   - Shuffle cards.
   - Reset the order of cards.
   - Review unknown cards.
   - Load a custom set of flashcards.
3. View the question, reveal the answer, and mark it as known or unknown.
4. Track your progress with the stats displayed under each card.

## Creating Custom Flashcard Sets

1. Create a new JSON file in the `sets/` folder.
2. Use the following format:
   ```json
   {
       "Question 1": "Answer 1",
       "Question 2": "Answer 2"
   }
   ```
3. Save the file and reload the application to see the new set in the sidebar.

## Configuration

You can customize the title and background color for each set by creating a corresponding JSON file in the `conf/` folder. Use the following format:

```json
{
    "title": "Custom Set Title",
    "background_color": "#FF5733"
}
```

## Requirements

- Python 3.7+
- Streamlit

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/).
- Inspired by traditional flashcard learning methods.