import Adafruit_DHT
import argparse
import json
import RPi.GPIO as GPIO
import os
import sys
from time import sleep, time
import yaml
import errno


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='hydroping', description='Track temperature and relative humidity!')
    parser.add_argument(
        '-c', '--config', default='hydroping.yml', help='The configuration file')
    return parser.parse_args()


def read_config(filename):
    try:
        with open(filename, 'r') as ymlfile:
            config = yaml.load(ymlfile)
            TARGET_GPIO = int(config['gpio'])
            FILE_PATH = config['log.path']
            LOG_STDOUT = config['log.stdout']
            return (TARGET_GPIO, FILE_PATH, LOG_STDOUT)
    except:
        raise OSError(
            errno.ENOENT, os.strerror(errno.ENOENT), filename)


def getSensorData(pin):
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
    return {'h': RH, 't': T, 'ts': time()}


def archive_readings(path, should_print, data):
    with open(path, 'a') as out:
        json.dump(data, out)
        out.write('\n')
    if should_print:
        print json.dumps(data)


def main():
    args = parse_arguments()
    TARGET_GPIO, FILE_PATH, LOG_STDOUT = read_config(args.config)

    data = getSensorData(TARGET_GPIO)
    archive_readings(FILE_PATH, LOG_STDOUT, data)


if __name__ == '__main__':
    main()
