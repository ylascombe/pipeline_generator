

## Setup
```
virtualenv .venv --python python3
pip install -r requirements.txt
```

## Run application
To run FastAPI app, run the following command:
```
uvicorn main:app --reload
```

## Test endpoint
When app is running, you can query by sending a POST on  http://localhost:8000/generate-github-actions/. 
```
curl -X POST "http://localhost:8000/generate-github-actions/"
```
