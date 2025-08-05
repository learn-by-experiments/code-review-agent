# Code Review Agent

a simple code review agent to review PRs
connect your repos and see the magic

# Setup

- Fastapi
- Pipenv
- git
- Postgres
- LangGraph
- GitHub toolkit
- Ollama
- LLM Model="llama3.1"

# Initial Setup

- clone the repo
  ```bash
  git clone https://github.com/learn-by-experiments/code-review-agent.git
  ```
- install dependencies

  ```bash
  pipevn install
  ```

- create a `.env` file with the following fields
  - Postgres Database connection details
  ```bash
  DB_NAME=      <-- Database Name -->
  USER_NAME=    <-- Database User Name -->
  PASSWORD=     <-- Database Password -->
  HOST=         <-- Database Host -->
  PORT=         <-- Database PORT -->
  ```
- pull the `llama3.1` model
  ```bash
  ollama pull llama3.1
  ```
- run the llm model using ollama
  ```bash
  ollama run llama3.1
  ```
