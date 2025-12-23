# Flask To-Do App with PocketBase

This is a simple To-Do application built with Flask and PocketBase.

## Prerequisites

- Python 3.8+
- PocketBase (included in the start script for Linux, or download manually)

## Installation and Running

### Quick Start (Linux/Mac)

1.  Run the start script:

    ```bash
    ./start.sh
    ```

    This script will:
    - Download PocketBase (if not present).
    - Create a Python virtual environment and install dependencies.
    - Start PocketBase in the background.
    - Start the Flask application.

2.  Open your browser and navigate to `http://127.0.0.1:5000`.

### Manual Setup

1.  **Download PocketBase**:
    Download the appropriate version for your OS from [PocketBase Releases](https://github.com/pocketbase/pocketbase/releases) and extract the `pocketbase` executable to the project root.

2.  **Install Dependencies**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Copy `.env.example` to `.env`:

    ```bash
    cp .env.example .env
    ```

4.  **Run PocketBase**:

    ```bash
    ./pocketbase serve --http=127.0.0.1:8090
    ```

5.  **Run Flask App**:
    In a new terminal (activate venv):

    ```bash
    python app.py
    ```

## Project Structure

- `app.py`: Main Flask application.
- `init_db.py`: Database initialization script.
- `init_schema.sql`: SQL template for schema creation.
- `pb_data/`: Directory where PocketBase stores data (created automatically).
