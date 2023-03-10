# Smart Green Island 2023

Repository for the 2023 Smart Green Island Challenge "Autonomous Ocean Garbage Collector"

## Installation

__*Uses Python 3.10*__

Create a virtual environment:

```bash
python -m venv venv
```

Active the virtual environment:

```bash
./venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment variables:

```bash
bash create_dotenv.sh
```

## Run Application

Run the application with:

```bash
python -m app
```

## Typechecks and Linter

Run Mypy for static typechecking:

```bash
mypy -m app
```

Run flake8 for linting:

```bash
flake8
```
