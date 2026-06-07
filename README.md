# AI Coding Agent 🤖

A terminal-based AI agent that accepts a coding task, picks the right tools to tackle it, and keeps going until the job is done (or it spectacularly fails — both are possible).

## How It Works

1. **You give it a task** — e.g., `"fix my calculator app, it's not starting correctly"`
2. **It picks from a set of predefined functions** to work on the task:
   -  **Scan files in a directory** — explore the project structure
   -  **Read a file's contents** — inspect source code
   -  **Overwrite a file's contents** — apply fixes
   -  **Execute the Python interpreter on a file** — run & verify the code
3. **It repeats step 2** until the task is complete (or it gives up after too many attempts)

## Setup

1. **Clone the repo and install dependencies** using [uv](https://github.com/astral-sh/uv):

   ```bash
   uv sync
   uv add google-genai==1.12.1
   uv add python-dotenv==1.1.0
   ```

2. **Set your Gemini API key** — create a `.env` file in the project root:

   ```bash
   echo "GEMINI_API_KEY=your_key_here" > .env
   ```

## Running the Agent

```bash
python main.py "your task description here"
```

**Examples:**

```bash
python main.py "strings aren't splitting in my app, pweeze fix 🥺👉🏽👈🏽"

python main.py "the calculator is returning wrong results for division"

python main.py "add error handling to the main function"
```

**Verbose mode** (shows token usage and step-by-step function calls):

```bash
python main.py "fix the bug in calculator.py" --verbose
```

## Configuration

Edit `config.py` to tweak the agent's behavior:

| Setting             | Default                  | Description                              |
|---------------------|--------------------------|------------------------------------------|
| `MODEL_NAME`        | `gemini-2.0-flash-001`   | The Gemini model to use                  |
| `WORKING_DIR`       | `./calculator`           | Directory the agent operates in          |
| `MAX_RETRY_ATTEMPTS`| `15`                     | Max iterations before the agent gives up |
| `MAX_CHAR_LIMIT`    | `10000`                  | Max characters read from a file          |
