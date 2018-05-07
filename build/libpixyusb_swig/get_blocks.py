from pixy import *
from ctypes import *
import paho.mqtt.client as mqtt


broker = "172.29.103.87"
start = "OFF"

# on_message function for reaction to game starting #
def on_message(client, userdata, msg):
    if msg.topic == "game/start1":
        global start
        start = str(msg.payload)

# Pixy Python SWIG get blocks example #

print ("Pixy Python SWIG Example -- Get Blocks")

# Initialize Pixy Interpreter thread #
pixy_init()

# Start the mqtt client #
client = mqtt.Client("notgreen")
client.connect(broker, 1883, 60)
client.subscribe("game/start1")
client.on_message = on_message
client.loop_start()

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

blocks = BlockArray(100)
frame  = 0

# Wait for blocks #
while 1:

    count = pixy_get_blocks(100, blocks)
    if count > 0 and start == "ON":
        # Blocks found #
        for index in range (0, count):
            print '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height)
            coords = str(blocks[index].x) + ',' + str(blocks[index].y)
            client.publish("game/pixy", payload=coords)
