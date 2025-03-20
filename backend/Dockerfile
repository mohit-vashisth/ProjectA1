FROM python:3.11

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files first
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy the rest of the project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app (assuming `main.py` contains `app` for Uvicorn)
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]