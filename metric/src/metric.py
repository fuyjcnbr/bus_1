import os
import pika
import json

LOGS_PATH = "/service_data/service_log.csv"

global_y_dict = dict()

if not os.path.isfile(LOGS_PATH):
    with open(LOGS_PATH, "a") as log_file:
        log_file.write("id,y_true,y_pred,absolute_error\n")


def add_to_log(message_id, y_true, y_pred):
    abs_error = abs(y_true - y_pred)
    s = f"{message_id},{y_true},{y_pred},{abs_error}\n"
    with open(LOGS_PATH, "a") as log_file:
        log_file.write(s)


try:
    # Создаём подключение к серверу на локальном хосте
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очередь y_true
    channel.queue_declare(queue='y_true')
    # Объявляем очередь y_pred
    channel.queue_declare(queue='y_pred')


    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f'Из очереди {method.routing_key} получено значение {message}')

        message_id = message["id"]
        if "y_true" in message.keys():
            y_true = message["y_true"]
            if message_id in global_y_dict.keys():
                y_pred = global_y_dict[message_id]["y_pred"]
                add_to_log(message_id, y_true, y_pred)
                del global_y_dict[message_id]
            else:
                global_y_dict[message_id] = {"y_true": y_true}
        else:
            y_pred = message["y_pred"]
            if message_id in global_y_dict.keys():
                y_true = global_y_dict[message_id]["y_true"]
                add_to_log(message_id, y_true, y_pred)
                del global_y_dict[message_id]
            else:
                global_y_dict[message_id] = {"y_pred": y_pred}

    # Извлекаем сообщение из очереди y_true
    channel.basic_consume(
        queue='y_true',
        on_message_callback=callback,
        auto_ack=True
    )
    # Извлекаем сообщение из очереди y_pred
    channel.basic_consume(
        queue='y_pred',
        on_message_callback=callback,
        auto_ack=True
    )

    # Запускаем режим ожидания прихода сообщений
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
except Exception as e:
    print('Не удалось подключиться к очереди')
    print(f"{e}")
