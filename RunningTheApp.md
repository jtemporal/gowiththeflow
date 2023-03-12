# Go with the flow

## Requirements

To create the virtual environment and install the require packages run:

```
python -m venv .env
source .env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Copy the .example.config file to .config and fill out the values with the information from your Auth0 dashboard.

## Run the demo

```
flask --debug run
```