from roboclaw import Roboclaw
from time import sleep

rc = Roboclaw("/dev/ttyACM0",115200)
rc.Open()

address=0x80

#rc.ForwardM1(address, 50)

# sleep (5)

rc.ForwardM1(address, 0)