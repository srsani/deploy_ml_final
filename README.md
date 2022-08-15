# AWS BYOC pipeline for a text classification application

In the current code repository, you can find the code for the Amazon SageMaker MLOps workflow
for a Text classification application using Bring Your Own Container (BYOC) approach, which means each note in the pipeline is based on docker image that is stored in Elastic Container Registry (ECR).  This work is the final project for Udacity AWS MLOps nano degree.

## Setup

### AWS side

1- setup SageMaker studio in `us-west-1`
2- make IAM `AmazonSageMaker-ExecutionRole` role with:
    - AmazonSageMaker-ExecutionPolicy
    - SecretsManagerReadWrite
    - AutoScalingFullAccess
    - AmazonS3FullAccess
    - AmazonSageMakerFullAccess

3- add the role that was just created to `AWS Secrets Manager`:

### local setup

- `virtualenv venv --python=python3.8`
- `pip install ipykernel`
- `python -m ipykernel install --user --name venv --display-name PYTHON_ENV_NAME`
- `pip install -r requirements.txt`

#### update code

Chenge the prefix for all the ECR repositories form `-redj` to some other prefix

- `processing_repository_uri = f'{account_id}.dkr.ecr.{region}.amazonaws.com/sagemaker-processing-redj:{branch_name}'`
- `model_training_repository_uri = f'{account_id}.dkr.ecr.{region}.amazonaws.com/sagemaker-train-redj:{branch_name}'`
- `model_deployment_repository_uri = f'{account_id}.dkr.ecr.{region}.amazonaws.com/sagemaker-deployment-init-redj:{branch_name}'`
- `model_deployment_server_repository_uri = f'{account_id}.dkr.ecr.{region}.amazonaws.com/sagemaker-deployment-redj:{branch_name}'`

And all the corresponding docker .sh

- `src/data_processing/docker_ecr.sh`
- `src/model_deployment/docker_ecr.sh`
- `src/model_deployment/docker_ecr.sh`

## Run the pipeline

The following command is used to run the pipeline from your local env:

`python src/pipeline.py BRANCH_NAME`
