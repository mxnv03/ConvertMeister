from minio import Minio

client = Minio('minio:9000',
               access_key='minioadmin',
               secret_key='minioadmin',
               secure=False)


def uploading_ready(file, name: str, filesize, bucket: str):
    client.put_object(bucket, name, file, filesize)
    return 'Success'


def download_conv(filename: str, directory: str = 'saving'):
    file_stream = client.get_object('upload', filename)
    # Генерация временного имени файла для сохранения
    temp_filename = f"Converter/{directory}/{filename}"
    with open(temp_filename, "wb") as temp_file:
        # Запись содержимого файла во временный файл
        for data in file_stream.stream(32 * 1024):
            temp_file.write(data)
    return 'Success'


def deleting(bucket: str, name: str):
    client.remove_object(bucket, name)
