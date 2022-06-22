#!python3

import argparse
import time
import requests
from irsdk import IRSDK

# this is our State class, with some helpful variables
class State:
  ir_connected = False
  last_car_setup_tick = -1

# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
  if state.ir_connected and not (ir.is_initialized and ir.is_connected):
    state.ir_connected = False
    # don't forget to reset your State variables
    state.last_car_setup_tick = -1
    # we are shutting down ir library (clearing all internal variables)
    ir.shutdown()
    print('irsdk disconnected')
  elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
    state.ir_connected = True
    print('irsdk connected')

# our main loop, where we retrieve data
# and do something useful with it
def loop(ir, url):
  ir.freeze_var_buffer_latest()
  telemetry = ir.get_json()
  requests.post(url, json = telemetry)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--url', help='url of the api to post telemetry to', required=true)

  args = parser.parse_args()

  # initializing ir and state
  ir = IRSDK()
  state = State()

  try:
    # infinite loop
    while True:
      # check if we are connected to iracing
      check_iracing()
      # if we are, then process data
      if state.ir_connected:
        loop(ir, args.url)
      # sleep for 1 second
      # maximum you can use is 1/60
      # cause iracing updates data with 60 fps
      time.sleep(1)
  except KeyboardInterrupt:
    # press ctrl+c to exit
    pass