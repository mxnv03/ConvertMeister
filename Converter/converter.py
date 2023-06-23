import subprocess
import pika
from load import download_conv, deleting, uploading_ready
import os
from db import add_file

path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
channel = connection.channel()
channel.queue_declare(queue='hello')


def v_to_a(name):
    input_video = name
    token = name[name.find('/') + 1:name.rfind('.')]
    output_audio = f'Converter/ready/{token}.mp3'
    command = ['/usr/bin/ffmpeg', '-i', input_video, output_audio]
    p = subprocess.run(command)
    if p.returncode == 0:
        add_file('2', token)
        with open(output_audio, 'rb') as out:
            size = os.path.getsize(output_audio)
            uploading_ready(out, f'{token}.mp3', filesize=size, bucket='ready')
        add_file('3', token)
        os.remove(os.path.join('', output_audio))
    else:
        return 'GG'



def a_to_v(name):
    input_audio = name
    token = name[name.find('/') + 1:name.rfind('.')]
    output_video = f"Converter/ready/{token}.mp4"
    command = ['/usr/bin/ffmpeg', '-i', input_audio, '-c:a', 'aac', '-b:a', '192k', '-vf', 'fps=25', output_video]
    p = subprocess.run(command)
    if p.returncode == 0:
        add_file('2', token)
        with open(output_video, 'rb') as out:
            size = os.path.getsize(output_video)
            uploading_ready(out, f'{token}.mp4', filesize=size, bucket='ready')
        add_file('3', token)
        os.remove(os.path.join('', output_video))
    else:
        return 'GG'


def callback(ch, method, properties, body):
    body = body.decode('utf-8')
    ras = str(body).split('.')[-1]
    download_conv(body, directory='Converter/timeout')
    if ras == 'mp4':
        v_to_a(f'timeout/{body}')
    elif ras == 'mp3':
        a_to_v(f'timeout/{body}')
    os.remove(os.path.join('timeout', body))
    deleting('upload', body)


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
