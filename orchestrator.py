# from database.select import check_running_tasks, check_task_capacity, get_all_queues

# a = check_running_tasks()
# b = check_task_capacity(queue_name="calcVol")
# c = get_all_queues()

# for i in a:
#     # print(i[1])
#     print(str(i))

# print(len(a))

# for i in b:
#     # print(i[1])
#     print(str(i))

# print(len(b))

# for i in c:
#     # print(i[1])
#     print(str(i))

# print(len(c))
from core import manage_tasks

manage_tasks()
