from aws.get_running_task_info import get_aws_task_details, get_running_tasks_from_aws
from aws.kill_task import kill_aws_task
from aws.Create_task import create_task_and_return_arn
from database.select import (
    check_running_tasks,
    check_task_capacity,
    get_pending_tasks,
)
from config import region_name, aws_access_key_id, aws_secret_access_key, aws_cluster


def get_dict_with_key_value(data, value, key="taskDefinitionArn"):
    result_dict = {}
    for item in data:
        if key in item and item[key] == value:
            result_dict = item
            break
    return result_dict


def create_task(count):
    create_task_and_return_arn(
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        cluster_arn=aws_cluster,
        task_count=count,
        taskDefinition_arn="",
    )
    print(
        "++++++++++++++++++++++++++++++ TASK CREATED ",
        count,
        " +++++++++++++++++++++++++++++++++",
    )


def kill_task(task_count, tasks_in_aws, queue_name):
    print(
        "++++++++++++++++++++++++++++++ TASK Killed ",
        task_count,
        " +++++++++++++++++++++++++++++++++",
    )
    running_task_details = check_running_tasks(queue_name)
    while task_count != 0:
        running_arn_list = []
        for i in running_task_details:
            running_arn_list.append(i["worker_id"])
        print("===")
        for i in tasks_in_aws["taskArns"]:
            if i not in running_arn_list:
                print("kill task arn: ", i)
                kill_respoance = kill_aws_task(
                    region_name=region_name,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    cluster_arn=aws_cluster,
                    task_arn=i,
                )
                print(kill_respoance)
                tasks_in_aws["taskArns"].remove(i)
                task_count -= 1
                break
    return True


def manage_tasks():
    queues = check_task_capacity()
    task_data_from_aws = get_aws_task_details(
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        cluster=aws_cluster,
        task_arn=get_running_tasks_from_aws(
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            cluster_arn=aws_cluster,
        ),
    )
    for row in queues:
        tasks_in_aws = get_dict_with_key_value(
            task_data_from_aws, row["task_definition_arn"]
        )
        if tasks_in_aws == {}:
            continue
        queue_name = row["queue"]
        running_tasks = check_running_tasks(queue_name)
        pending_tasks = get_pending_tasks(queue_name)

        print("Queue: ", queue_name)
        print("Task max Capacity: ", row["max_task"])
        print("Task min Capacity: ", row["min_task"])
        print("tasks_in_aws: ", tasks_in_aws["running_tasks_count"])
        print("Running Tasks: ", len(running_tasks))
        print("Pending Tasks: ", len(pending_tasks))
        total_task = len(running_tasks) + len(pending_tasks)
        print("total_task: ", total_task)

        if tasks_in_aws["running_tasks_count"] < row["min_task"]:
            task_count = abs(tasks_in_aws["running_tasks_count"] - row["min_task"])
            print(
                "create task count a",
                abs(tasks_in_aws["running_tasks_count"] - row["min_task"]),
            )
            create_task(count=task_count)
            print("")
            continue

        if tasks_in_aws["running_tasks_count"] < total_task:
            if tasks_in_aws["running_tasks_count"] < row["max_task"]:
                if row["max_task"] < tasks_in_aws["running_tasks_count"]:
                    print(
                        "create task count: e ",
                        row["max_task"] - tasks_in_aws["running_tasks_count"],
                    )
                    task_count = row["max_task"] - tasks_in_aws["running_tasks_count"]
                    create_task(task_count)
                    print("")
                    continue

                print(
                    "create task count: b ",
                    min(
                        total_task - tasks_in_aws["running_tasks_count"],
                        row["max_task"] - tasks_in_aws["running_tasks_count"],
                    ),
                )
                task_count = min(
                    total_task - tasks_in_aws["running_tasks_count"],
                    row["max_task"] - tasks_in_aws["running_tasks_count"],
                )
                create_task(task_count)
                print("")
                continue

        elif tasks_in_aws["running_tasks_count"] > total_task:
            if tasks_in_aws["running_tasks_count"] > row["max_task"]:
                print(
                    " kill task count when not running c",
                    tasks_in_aws["running_tasks_count"] - total_task,
                )
                task_count = tasks_in_aws["running_tasks_count"] - total_task
                kill_task(
                    task_count=task_count,
                    tasks_in_aws=tasks_in_aws,
                    queue_name=queue_name,
                )
                print("")
                continue

            if (
                tasks_in_aws["running_tasks_count"] < row["max_task"]
                and tasks_in_aws["running_tasks_count"] > row["min_task"]
            ):
                print(
                    " kill task count d : ",
                    min(
                        tasks_in_aws["running_tasks_count"] - total_task,
                        tasks_in_aws["running_tasks_count"] - row["min_task"],
                    ),
                )
                task_count = min(
                    tasks_in_aws["running_tasks_count"] - total_task,
                    tasks_in_aws["running_tasks_count"] - row["min_task"],
                )
                kill_task(
                    task_count=task_count,
                    tasks_in_aws=tasks_in_aws,
                    queue_name=queue_name,
                )
                print("")
                continue

        print("")
    pass
