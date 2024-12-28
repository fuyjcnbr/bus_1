import pika
import pickle
import numpy as np
import json

# Читаем файл с сериализованной моделью
with open('/model.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

try:
    # Создаём подключение по адресу rabbitmq:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очередь features
    channel.queue_declare(queue='features')
    # Объявляем очередь y_pred
    channel.queue_declare(queue='y_pred')


    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        print(f'Получено сообщение {body}')

        message_in = json.loads(body)
        message_id = message_in["id"]
        features = message_in["x"]
        print(f'Получено message_id {message_id}')
        print(f'Получен вектор признаков {features}')
        # features = json.loads(body)
        pred = regressor.predict(np.array(features).reshape(1, -1))

        message_out = {
            'id': message_id,
            'y_pred': pred[0]
        }

        channel.basic_publish(
            exchange='',
            routing_key='y_pred',
            body=json.dumps(message_out),
        )
        print(f'Предсказание {pred[0]} отправлено в очередь y_pred')


    # Извлекаем сообщение из очереди features
    # on_message_callback показывает, какую функцию вызвать при получении сообщения
    channel.basic_consume(
        queue='features',
        on_message_callback=callback,
        auto_ack=True
    )
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    # Запускаем режим ожидания прихода сообщений
    channel.start_consuming()
except Exception as e:
    print('Не удалось подключиться к очереди')
    print(f"{e}")
