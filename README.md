# SOP Interview Question Generator

This project generates interview questions based on candidate Statement of Purpose (SOP) text using a local LLM (Ollama).

## Prerequisites

1.  **Ollama**: You need to have [Ollama](https://ollama.com/) installed and running.
2.  **Model**: The project uses `llama3.2:3b`.
    ```bash
    ollama pull llama3.2:3b
    ```
3.  **Python**: Python 3.x is required.

## Setup

The project includes a virtual environment in `venv`.

1.  **Activate the virtual environment**:
    ```bash
    source venv/bin/activate
    ```
    Or use the python executable directly: `./venv/bin/python`.

## Running the Project

To run the generator:

```bash
./venv/bin/python src/main.py
```

## Configuration

-   **Input**: `data/data.csv` - The source CSV file containing candidate data.
-   **Output**: `data/outputs/all_questions.txt` - The generated interview questions.
-   **Settings**: You can modify `src/config.py` to change the model, prompt, or file paths.

## Project Structure

-   `src/`: Source code
    -   `main.py`: Entry point
    -   `ollama_generator.py`: Ollama integration
    -   `text_cleaner.py`: Text processing utilities
    -   `config.py`: Configuration settings
-   `data/`: Data directory
    -   `data.csv`: Input data
    -   `outputs/`: Generated results
-   `venv/`: Python virtual environment with dependencies
