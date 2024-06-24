import boto3


def kill_aws_task(
    region_name, aws_access_key_id, aws_secret_access_key, task_arn, cluster_arn
):
    client = boto3.client(
        "ecs",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    response = client.stop_task(
        cluster=cluster_arn, task=task_arn, reason="Killed by orchestrator"
    )

    # print("response : ", response)
    return response["ResponseMetadata"]
