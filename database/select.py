from database import UserSingleton, OrcSingleton


# def get_all_queues():
#     orc = OrcSingleton()
#     cursor = orc.cursor
#     query = """SELECT queue FROM queue_capacity;"""
#     cursor.execute(query)
#     result = cursor.fetchall()

#     # Convert the result to a list of dictionaries
#     result_dict = [
#         dict(zip([column[0] for column in cursor.description], row)) for row in result
#     ]

#     return result_dict
#     # return [{"queue": "calcVol"}]


def get_pending_tasks(queue_name):
    user = UserSingleton()
    cursor = user.cursor
    query = (
        """SELECT id,queue,payload,reserved_at,attempts,available_at,worker_id FROM job_queues WHERE reserved_at IS NULL and errors is NULL and queue = '%s';"""
        % queue_name
    )
    cursor.execute(query)
    result = cursor.fetchall()

    # Convert the result to a list of dictionaries
    result_dict = [
        dict(zip([column[0] for column in cursor.description], row)) for row in result
    ]

    return result_dict


def check_running_tasks(queue_name):
    user = UserSingleton()
    cursor = user.cursor
    query = (
        """SELECT id,queue,payload,reserved_at,attempts,available_at,worker_id FROM job_queues WHERE reserved_at IS NOT NULL and errors is NULL and queue = '%s';"""
        % queue_name
    )
    cursor.execute(query)
    result = cursor.fetchall()

    # Convert the result to a list of dictionaries
    result_dict = [
        dict(zip([column[0] for column in cursor.description], row)) for row in result
    ]

    return result_dict


def check_task_capacity():

    orc = OrcSingleton()
    cursor = orc.cursor
    query = (
        """SELECT id,queue,min_task,max_task,task_definition_arn FROM queue_capacity;"""
    )
    cursor.execute(query)
    result = cursor.fetchall()

    # Convert the result to a list of dictionaries
    result_dict = [
        dict(zip([column[0] for column in cursor.description], row)) for row in result
    ]
    # print(result_dict)
    # return [{"id": 1, "queue": "calcVol", "min_task": 0, "max_task": 3}]
    return result_dict
