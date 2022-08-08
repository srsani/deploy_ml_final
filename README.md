# AWS BYOC pipeline for a text classification application

In the current code repository, you can find the code for the Amazon SageMaker MLOps workflow
for a Text classification application using Bring Your Own Container (BYOC) approach, which means each note in the pipeline is based on docker image that is stored in Elastic Container Registry (ECR).  This work is the final project for Udacity AWS MLOps nano degree.

## Setup

### local setup

- `virtualenv venv --python=python3.8`
- `pip install ipykernel`
- `python -m ipykernel install --user --name venv --display-name PYTHON_ENV_NAME`
- `pip install -r requirements.txt`

## Run the pipeline

The following command is used to run the pipeline from your local env:

`python src/pipeline.py BRANCH_NAME`
