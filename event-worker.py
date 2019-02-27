from lib.redis import get_connection

import json
import logging
import uuid
import time

logging.basicConfig(level=logging.INFO)
redis_connecton = get_connection()


def main():

    while True:
        _, msg = redis_connecton.blpop('todos')

        logging.info('processing => %s', msg)

        try:

            todo = json.loads(msg.decode())

        except Exception:

            continue

        # This is a new todo!
        if 'id' not in todo:
            todo['id'] = str(uuid.uuid4())

        list_id = todo['list']
        serialized = json.dumps(todo)

        redis_connecton.hset(f'{list_id}:todos', todo['id'], serialized)
        redis_connecton.publish(list_id, serialized)
        time.sleep(2)


if __name__ == '__main__':
    main()
