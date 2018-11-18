import sys
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
import argparse
import yaml
import json
from time import time

def parse_arguments():
  parser = argparse.ArgumentParser(prog='hydroping', description='Track temperature and relative humidity!')
  parser.add_argument('-c', '--config', default='hydroping.yml', help='The configuration file')
  return parser.parse_args()

def read_config(filename):
  try:
    with open(filename, 'r') as ymlfile:
      return yaml.load(ymlfile)
  except:
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

def getSensorData(pin):
  RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
  return (RH, T)

def main():
  print('reading args')
  args = parse_arguments()
  print('reading config')
  config = read_config(args.config)
  print(config)
  print(config['gpio'])
  GPIO = int(config['gpio'])
  FILE_PATH = config['log.path']
  LOG_STDOUT = config['log.stdout']
  print(GPIO)
  print('File path: ' + FILE_PATH)
  print(LOG_STDOUT)
  print(json.dumps({'foo': ['bar', 23, True]}))
  try:
    print('trying')
    RH, T = getSensorData(GPIO)
    log_data = {'h': RH, 't': T, 'ts': time()}
    print(json.dumps(log_data))
    with open(FILE_PATH, 'a') as out:
      json.dump(log_data, out)
      out.write('\n')
    print('after')
    print(RH)
    print(T)
  except:
    print ('failure')
    print(sys.exc_info()[0])

if __name__ == '__main__':
  main()

