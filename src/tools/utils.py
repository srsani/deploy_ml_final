import logging
from pathlib import Path
from io import BytesIO
import os
import mlflow
import boto3
from botocore.exceptions import ClientError
import json
import sagemaker.session
import sagemaker
import subprocess
import tarfile


def get_secret(secret_name, secret_key):
    """
    Function to get secrest from aws.
    Arguments:
        * secret_name: string
            secret name on aws
    Outputs:
        * secret_value: string
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager')
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        secrets = json.loads(get_secret_value_response['SecretString'])
    return secrets[secret_key]


def get_session(region, default_bucket):
    """Gets the sagemaker session based on the region.
    Args:
        region: string
            the aws region to start the session
        default_bucket: string
            the bucket to use for storing the artifacts
    Returns:
        sagemaker.session.Session instance
    """
    boto_session = boto3.Session(region_name=region)
    sagemaker_client = boto_session.client("sagemaker")
    runtime_client = boto_session.client("sagemaker-runtime")
    return sagemaker.session.Session(
        boto_session=boto_session,
        sagemaker_client=sagemaker_client,
        sagemaker_runtime_client=runtime_client,
        default_bucket=default_bucket,
    )


def update_py_file(s3_folder_prefix, original_file_path, deploy_file_path):
    """
    Function for updating predictor.py with the current branch_name. 
    The base file need to have "s3_folder_prefix"

    Arguments::
        * branch_name: string
            name of the current branch
        * original_file_path: sting 
            path to the _base file
        * deploy_file_path: string
            path to where the file should go
    Outputs:
         * output: string
             result of pushed ecr
    """
    f1 = open(original_file_path, 'r')
    linelist = f1.readlines()

    # make a new file
    f2 = open(deploy_file_path, 'w')
    for line in linelist:
        line = line.replace('s3_folder_prefix', s3_folder_prefix)
        f2.write(line)
    f2.close()
    f1.close()
    return True


def push_image_ecr(docker_file_path, tag_name=None):
    """
    Function for getting pushing docker image to ecr

    Arguments::
        * ecr_prefix: string
            name for ecr repo
    Outputs:
         * output: string
             result of pushed ecr
    """
    bashCommand = f"chmod +x {docker_file_path}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    bashCommand = f"sh {docker_file_path} {tag_name}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output


def push_image_ecr_deployment(docker_file_path, tag_name, model_artifact_path):
    """
    Function for getting pushing docker image to ecr

    Arguments::
        * ecr_prefix: string
            name for ecr repo
    Outputs:
         * output: string
             result of pushed ecr
    """
    bashCommand = f"chmod +x {docker_file_path}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    bashCommand = f"sh {docker_file_path} {tag_name} {model_artifact_path}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output


def make_deployment_tar():
    tar = tarfile.open(
        f'src/model_deployment/docker.tar.gzip', "w:bz2")
    for name in ["src/model_deployment"]:
        tar.add(name)
    tar.close()
    return True
