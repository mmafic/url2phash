import socket, os
import sys

from logger import logger
from utils import phash_from_url

HOST = '0.0.0.0'
PORT = 65101

def listen(s):
    while 1:
        try:
            conn, addr = s.accept()
            logger.debug('Connection established')
            with conn:
                while 1:
                    try:
                        url = conn.recv(1024).decode()
                        if len(url) < 1:
                            conn.send(int(0).to_bytes(1, 'big'))
                            continue

                        logger.debug(f'Received url: {url}')
                        phash = phash_from_url(url)
                        if phash is None:
                            logger.debug('no phash')
                            conn.send(int(0).to_bytes(1, 'big'))
                        else:
                            logger.debug(f'Responding with phash: {phash}')
                            conn.send(phash.to_bytes(64, 'big', signed=True))
                    except ConnectionResetError as err:
                        raise err
                    except BaseException as err:
                        logger.error(f'{type(err)}: {err}')
                        conn.send(int(1).to_bytes(1, 'big'))
                        raise err
        except (ConnectionResetError, BrokenPipeError) as err:
            logger.debug('Connection reset by peer')


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info('Server started.')
        listen(s)
except KeyboardInterrupt:
    logger.info('Stopping server...')
    sys.exit(0)