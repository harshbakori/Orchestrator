import subprocess
import json
import boto3


# TODO: get dynamic network config for task
def create_task_and_return_arn(
    region_name,
    task_count,
    aws_access_key_id,
    aws_secret_access_key,
    cluster_arn,
    taskDefinition_arn,
    network_configuration_dict={
        "awsvpcConfiguration": {
            "subnets": [
                "subnet-08670f8cc59627070",  # replace with your subnet id
            ],
        }
    },
):
    """
    Creates and runs a task on Amazon ECS (Elastic Container Service) using the provided parameters.

    Args:
        region_name (str): The AWS region name.
        task_count (int): The number of tasks to run.
        aws_access_key_id (str): The AWS access key ID.
        aws_secret_access_key (str): The AWS secret access key.
        cluster_arn (str): The ARN (Amazon Resource Name) of the ECS cluster.
        taskDefinition_arn (str): The ARN of the task definition.
        network_configuration_dict (dict, optional): The network configuration for the task. Defaults to a sample configuration.

    Returns:
        str: The ARN of the created task.
    """
    client = boto3.client(
        "ecs",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    task_start_response = client.run_task(
        cluster=cluster_arn,
        count=task_count,
        launchType="FARGATE",
        networkConfiguration=network_configuration_dict,
        tags=[
            {"key": "string", "value": "string"},
        ],
        taskDefinition=taskDefinition_arn,
    )

    return task_start_response["tasks"][0]["taskArn"]
