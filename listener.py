import socket, os
import sys

from logger import logger
from utils import phash_from_url

try:
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove("/var/url2phash.sock")
    except OSError:
        pass
    s.bind("/var/url2phash.sock")
    s.listen(1)

    logger.info('Server started.')

    while 1:
        try:
            conn, addr = s.accept()
            logger.debug('Connection established')
            while 1:
                try:
                    url = conn.recv(1024).decode()
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
                    logger.error(err)
                    conn.send(int(1).to_bytes(1, 'big'))
                    raise err
        except (ConnectionResetError, BrokenPipeError) as err:
            logger.debug('Connection reset by peer')

except KeyboardInterrupt:
    logger.info('Stopping server...')
    conn.close()
    sys.exit(1)