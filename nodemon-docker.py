#!python3
#encoding=utf-8
from __future__ import print_function, division


import os
import sys
import json
import time
import argparse

def touch():
    print('Touched in:', now)
    os.system('docker-machine ssh default touch ../..'+filePath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nodemon dosen\'t work with Docker on Windows. Use this to make it works.')
    parser.add_argument('filePath', metavar='file to touch', type=str,
                        help='example: "/c/Users/<your user>/file.js"')
    parser.add_argument('--touch', action='store_true', help='reserved, you don\'t need to use')
    args = parser.parse_args()


    filePath = args.filePath

    if not args.touch:
        # inicie o nodemon e termine
        try:
            os.system('nodemon --exec nodemon-docker "'+filePath+'" --touch')
        except KeyboardInterrupt as e:
            pass
        sys.exit(0)


    # entre no diretório do script
    os.chdir(os.path.dirname(__file__))

    if not os.path.exists('config.json'):
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump({}, file)
            config = {}
    else:
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)

    # Variável que diz se eu devo
    # tocá-lo
    mustTouch = False

    # se esse arquivo não está no config
    # insere-o
    now = int(time.time())
    if filePath not in config:
        config[filePath] = -1
        mustTouch = True
    else:
        # se a diferença de tempo entre agora e antes for menor
        # do que 2 segundos
        # não toco
        if now - config[filePath] >= 2:
            mustTouch = True
            config[filePath] = now
        else:
            print('Already touched')


    # salva o arquivo de configuração
    with open('config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file)


    if mustTouch:
        touch()