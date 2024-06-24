# use taskmeta endpoint of aws conainer adn print the logs using python
#

# ${ECS_CONTAINER_METADATA_URI_V4}/task
import logging
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_meta():
    try:
        response = requests.get(
            "http://169.254.170.2/v4",
            headers={"Metadata": "true"},
            timeout=20,
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error in getting task meta: {e}")
        return None


def get_task_meta():
    try:
        response = requests.get(
            "http://169.254.170.2/v4/task",
            headers={"Metadata": "true"},
            timeout=20,

        )
        return response.json()
    except Exception as e:
        logger.error(f"Error in getting task meta: {e}")
        return None


# read environment veriable using python
for i in range(10):
    logger.info(f"retrying to get task meta: {i}")
    meta = get_meta()
    print(meta)
    logger.info("getting task_meta")
    task_meta = get_task_meta()
    print(task_meta["TaskARN"])
    if task_meta:
        break
    else:
        logger.info("retrying to get task meta")
