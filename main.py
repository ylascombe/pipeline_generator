from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import yaml

app = FastAPI()

def generate_github_actions_config():
    config = {
        'name': 'CI/CD Pipeline',
        'on': ['push', 'pull_request'],
        'jobs': {
            'unit_tests': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'name': 'Checkout code', 'uses': 'actions/checkout@v2'},
                    {'name': 'Set up Python', 'uses': 'actions/setup-python@v2', 'with': {'python-version': '3.8'}},
                    {'name': 'Install dependencies', 'run': 'pip install -r requirements.txt'},
                    {'name': 'Run unit tests', 'run': 'pytest tests/unit'}
                ]
            },
            'integration_tests': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'name': 'Checkout code', 'uses': 'actions/checkout@v2'},
                    {'name': 'Set up Python', 'uses': 'actions/setup-python@v2', 'with': {'python-version': '3.8'}},
                    {'name': 'Install dependencies', 'run': 'pip install -r requirements.txt'},
                    {'name': 'Run integration tests', 'run': 'pytest tests/integration'}
                ]
            },
            'acceptance_tests': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'name': 'Checkout code', 'uses': 'actions/checkout@v2'},
                    {'name': 'Set up Python', 'uses': 'actions/setup-python@v2', 'with': {'python-version': '3.8'}},
                    {'name': 'Install dependencies', 'run': 'pip install -r requirements.txt'},
                    {'name': 'Run acceptance tests', 'run': 'pytest tests/acceptance'}
                ]
            },
            'deploy': {
                'runs-on': 'ubuntu-latest',
                'needs': ['unit_tests', 'integration_tests', 'acceptance_tests'],
                'steps': [
                    {'name': 'Checkout code', 'uses': 'actions/checkout@v2'},
                    {'name': 'Set up kubectl', 'uses': 'azure/setup-kubectl@v1'},
                    {'name': 'Deploy to Kubernetes', 'run': 'kubectl apply -f k8s/deployment.yaml'}
                ]
            }
        }
    }
    return yaml.dump(config)

@app.post("/generate-github-actions/")
def create_github_actions_config():
    try:
        config_yaml = generate_github_actions_config()
        response = {
            "status": "success",
            "config": config_yaml
        }
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


