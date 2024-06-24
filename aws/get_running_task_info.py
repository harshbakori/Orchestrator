import boto3


def get_running_tasks_from_aws(
    region_name, aws_access_key_id, aws_secret_access_key, cluster_arn
):
    client = boto3.client(
        "ecs",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    response = client.list_tasks(cluster=cluster_arn)
    return response["taskArns"]


def group_by_task_defination(input_list_of_dict):
    from itertools import groupby
    from operator import itemgetter

    grouped_list_of_dict = []
    input_list_of_dict = sorted(input_list_of_dict, key=itemgetter("taskDefinitionArn"))
    for key, value in groupby(input_list_of_dict, key=itemgetter("taskDefinitionArn")):
        # print(key)
        vals = []
        for k in value:
            # print(k)
            vals.append(k["taskArn"])

        grouped_list_of_dict.append(
            {
                "taskDefinitionArn": key,
                "taskArns": vals,
                "running_tasks_count": len(vals),
            }
        )
    return grouped_list_of_dict


def extract_taskArn_and_taskDefinitionArn(response):
    result = []
    for i in response["tasks"]:
        result.append(
            {"taskArn": i["taskArn"], "taskDefinitionArn": i["taskDefinitionArn"]}
        )

    formatted_result = group_by_task_defination(result)
    return formatted_result


def get_aws_task_details(
    region_name, aws_access_key_id, aws_secret_access_key, cluster, task_arn
):
    client = boto3.client(
        "ecs",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    response = client.describe_tasks(cluster=cluster, tasks=task_arn)

    extrated_data = extract_taskArn_and_taskDefinitionArn(response)
    return extrated_data
