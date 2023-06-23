import uuid
from minio import Minio
import pika
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from db import add_file, add_name, get_orig, check_user

# docker run -d -p 5672:5672 --name rabbit rabbitmq
# docker run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"
client = Minio('minio:9000',
               access_key='minioadmin',
               secret_key='minioadmin',
               secure=False)

if 'ready' not in list(client.list_buckets()):
    client.make_bucket('ready')
if 'upload' not in list(client.list_buckets()):
    client.make_bucket('upload')


def token_creating():
    return str(uuid.uuid1())


def uploading(file, bucket: str, nickname: str):
    token = token_creating()

    add_file('1', token)  # статус 1 - файл загружен, токен - уникальный
    add_name(token, f"{str(file.filename[:str(file.filename).rfind('.')])}", nickname)  # сохранение оригинального
    # названия для токена

    name = token + '.' + str(file.filename).split('.')[-1]
    client.put_object(bucket, name, file.file, file.size, file.content_type)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=name)  # присылаем в конвертер
    connection.close()
    ras = str(file.filename).split('.')[-1]
    return f"{token}.{'mp3' if ras == 'mp4' else 'mp4'}"


def download(nickname: str, filename: str):
    def iter_file():
        try:
            # Получение объекта файла из MinIO
            obj = client.get_object('ready', filename)
            while True:
                data = obj.read(4096)
                if not data:
                    break
                yield data
        except Exception as error:
            raise HTTPException(status_code=404, detail=error)

    if check_user(nickname, filename):
        return StreamingResponse(iter_file(), media_type="application/octet-stream",
                                 headers={
                                     "Content-Disposition": f"attachment; filename={get_orig(filename[:filename.rfind('.')]) + '.' + filename.split('.')[-1]}"})
    else:
        raise HTTPException(status_code=404, detail="User don't have such file")
