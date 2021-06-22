#DRONE LAUNCHER


#Import modules

from flask import Flask, render_template, request, jsonify
from roboclaw import Roboclaw
import time
import socket
import time
from neopixel import *
import argparse

#Open serial port

#Linux comport name
#rc = Roboclaw("/dev/ttyACM0",115200)
#Windows comport name
rc = Roboclaw("COM8",115200)
rc.Open()

#Declare variables

host=(([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
port=5000

address = 0x80                #Controller 1, M1=Pitch, M2=Rotation
address_2 = 0x81              #Controller 2, M1=Lift, M2=Launch

pitch_pulses=355000           #Encoder pulses from the linear actuator
pitch_length=90.0             #Degrees
pitch_speed_pulses=7000       #Pulses per second
pitch_speed_manual=127        #From 0 to 127
pitch_ready=70.0              #Pitch degrees for the launch (temporary)

rotation_pulses=950000        #Encoder pulses from the rotation motor
rotation_length=180.0         #Degrees
rotation_speed_pulses=16000   #Pulses per second
rotation_speed_manual=15      #From 0 to 127
rotation_ready=10.0           #Rotation degress for the launch (temporary)

lift_pulses=19000             #Encoder pulses from the lifting colum
lift_length=130.0             #cm
lift_speed_pulses=420         #Pulses per second
lift_speed_manual=127         #From 0 to 127
lift_ready=lift_length        #Lift lenght for the launch (temporary)

launch_pulses=14800           #Encoder pulses from the launch motor
launch_length=111.0           #cm
launch_speed_pulses=6*13400   #Pulses per second during launch (145000 max) (13400 pulses/m)
launch_speed_pulses_slow=2500 #Pulses per second during preparation
launch_speed_manual=12        #From 0 to 127
launch_acceleration=(launch_speed_pulses**2)/13400 #Acceleration during launch (pulses/second2)
launch_max_speed=10           #Maximum launch speed
launch_min_speed=1            #Minimum launch speed
launch_max_acceleration=48    #Maximum launch acceleration
launch_min_acceleration=1     #Minimum launch acceleration
launch_standby=8000           #Drone position during stand-by
launch_mount=17000            #Drone position during mounting
launch_break=21000            #Belt position during breaking
launch_bottom=0               #Drone position at the back part of the capsule
launch_connect=2190           #Belt position for touching the upper part

encoders_ready = 0            #At the beggining, the encoders are not ready


#Create an instance of the Flask class for the web app

app = Flask(__name__)
app.debug = True


#Render HTML template

@app.route("/")
def index():
    return render_template('dronelauncher_web.html')


#Motor controller functions

#rc.ForwardM2(address, rotation_speed_manual)
#rc.ForwardM2(address,0) #Both commands are used to avoid rotation

@app.route('/app_pitch_up', methods=['POST'])
def function_pitch_up():
    rc.BackwardM1(address, pitch_speed_manual)
    return (''), 204 #Returns an empty response

@app.route('/app_pitch_down', methods=['POST'])
def function_pitch_down():
    rc.ForwardM1(address, pitch_speed_manual)
    return (''), 204

@app.route('/app_pitch_position', methods=['POST'])
def function_pitch_position():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403
    pitch_position = request.form.get('pitch_position', type=int)
    if pitch_position > pitch_length or pitch_position < 0:
        return (''), 400
    elif pitch_position == 0:
        pitch_objective = 0
    else:
        pitch_objective = int(pitch_pulses/(pitch_length/pitch_position))
    pitch_actual = rc.ReadEncM1(address)[1]
    pitch_increment = pitch_objective-pitch_actual
    if pitch_increment >= 0:
        rc.SpeedDistanceM1(address,pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
        return (''), 204
    else:
        rc.SpeedDistanceM1(address,-pitch_speed_pulses,-pitch_increment,1)
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
        return (''), 204

@app.route('/app_pitch_stop', methods=['POST'])
def function_pitch_stop():
    rc.ForwardM1(address,0)
    return (''), 204



@app.route('/app_rotation_right', methods=['POST'])
def function_rotation_right():
    rc.ForwardM2(address, rotation_speed_manual)
    return (''), 204

@app.route('/app_rotation_left', methods=['POST'])
def function_rotation_left():
    rc.BackwardM2(address, rotation_speed_manual)
    return (''), 204

@app.route('/app_rotation_position', methods=['POST'])
def function_rotation_position():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403
    rotation_position = request.form.get('rotation_position', type=int)
    if rotation_position > rotation_length or rotation_position < -rotation_length:
        return (''), 400
    elif rotation_position == 0:
        rotation_objective = 0
    else:
        rotation_objective = int((rotation_pulses/(rotation_length/rotation_position))/2)
    rotation_actual = rc.ReadEncM2(address)[1]
    rotation_increment = rotation_objective-rotation_actual
    if rotation_increment >= 0:
        rc.SpeedDistanceM2(address,rotation_speed_pulses,rotation_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration
        return (''), 204
    else:
        rc.SpeedDistanceM2(address,-rotation_speed_pulses,-rotation_increment,1)
        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration
        return (''), 204

@app.route('/app_rotation_stop', methods=['POST'])
def function_rotation_stop():
    rc.ForwardM2(address,0)
    return (''), 204



@app.route('/app_lift_up', methods=['POST'])
def function_lift_up():
    rc.ForwardM1(address_2, lift_speed_manual)
    return (''), 204

@app.route('/app_lift_down', methods=['POST'])
def function_lift_down():
    rc.BackwardM1(address_2, lift_speed_manual)
    return (''), 204

@app.route('/app_lift_position', methods=['POST'])
def function_lift_position():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403
    lift_position = request.form.get('lift_position', type=int)
    if lift_position > lift_length or lift_position < 0:
        return (''), 400
    elif lift_position == 0:
        lift_objective = 0
    else:
        lift_objective = int(lift_pulses/(lift_length/lift_position))
    lift_actual = rc.ReadEncM1(address_2)[1]
    lift_increment = lift_objective-lift_actual
    if lift_increment >= 0:
        rc.SpeedDistanceM1(address_2,lift_speed_pulses,lift_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
        return (''), 204
    else:
        rc.SpeedDistanceM1(address_2,-lift_speed_pulses,-lift_increment,1)
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
        return (''), 204

@app.route('/app_lift_stop', methods=['POST'])
def function_lift_stop():
    rc.ForwardM1(address_2,0)
    return (''), 204



@app.route('/app_launch_forwards', methods=['POST'])
def function_launch_forwards():
    rc.ForwardM2(address_2, launch_speed_manual)
    #rc.SpeedM2(address_2,launch_speed_pulses_slow) #Using the speed control instead of the duty cycle because the friction changes in the tube
    return (''), 204

@app.route('/app_launch_backwards', methods=['POST'])
def function_launch_backwards():
    rc.BackwardM2(address_2, launch_speed_manual)
    #rc.SpeedM2(address_2,-launch_speed_pulses_slow) #Using the speed control instead of the duty cycle because the friction changes in the tube
    return (''), 204

@app.route('/app_launch_position', methods=['POST'])
def function_launch_position():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403
    launch_position = request.form.get('launch_position', type=int)
    if launch_position > launch_length or launch_position < 0:
        return (''), 400
    else:
        launch_objective = launch_bottom
        launch_actual = rc.ReadEncM2(address_2)[1]
        launch_increment = launch_objective-launch_actual
        if launch_increment >= 0:
            rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
            rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
        else:
            rc.SpeedDistanceM2(address_2,-launch_speed_pulses_slow,-launch_increment,1)
            rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration

        buffer_2 = (0,0,0)
        while(buffer_2[2]!=0x80):   #Loop until all movements are completed
            buffer_2 = rc.ReadBuffers(address_2)

        if launch_position == 0:
            launch_objective = 0
        else:
            launch_objective = int(launch_pulses/(launch_length/launch_position))
        launch_actual = rc.ReadEncM2(address_2)[1]
        launch_increment = launch_objective-launch_actual+launch_connect
        if launch_increment >= 0:
            rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_increment,0) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
            rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
            return (''), 204
        else:
            rc.SpeedDistanceM2(address_2,-launch_speed_pulses_slow,-launch_increment,0)
            rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
            return (''), 204


@app.route('/app_launch_stop', methods=['POST'])
def function_launch_stop():
    rc.ForwardM2(address_2,0)
    return (''), 204



@app.route('/app_max_pitch', methods=['POST'])
def function_max_pitch():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403
    pitch_objective = pitch_pulses
    pitch_actual = rc.ReadEncM1(address)[1]
    pitch_increment = pitch_objective-pitch_actual
    if pitch_increment >= 0:
        rc.SpeedDistanceM1(address,pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
        return (''), 204
    else:
        rc.SpeedDistanceM1(address,-pitch_speed_pulses,-pitch_increment,1)
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
        return (''), 204

@app.route('/app_min_pitch', methods=['POST'])
def function_min_pitch():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403
    pitch_objective = 0
    pitch_actual = rc.ReadEncM1(address)[1]
    pitch_increment = pitch_objective-pitch_actual
    if pitch_increment >= 0:
        rc.SpeedDistanceM1(address,pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
        return (''), 204
    else:
        rc.SpeedDistanceM1(address,-pitch_speed_pulses,-pitch_increment,1)
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
        return (''), 204

@app.route('/app_max_lift', methods=['POST'])
def function_max_lift():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403
    lift_objective = lift_pulses
    lift_actual = rc.ReadEncM1(address_2)[1]
    lift_increment = lift_objective-lift_actual
    if lift_increment >= 0:
        rc.SpeedDistanceM1(address_2,lift_speed_pulses,lift_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
        return (''), 204
    else:
        rc.SpeedDistanceM1(address_2,-lift_speed_pulses,-lift_increment,1)
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
        return (''), 204

@app.route('/app_min_lift', methods=['POST'])
def function_min_lift():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403
    lift_objective = 0
    lift_actual = rc.ReadEncM1(address_2)[1]
    lift_increment = lift_objective-lift_actual
    if lift_increment >= 0:
        rc.SpeedDistanceM1(address_2,lift_speed_pulses,lift_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
        return (''), 204
    else:
        rc.SpeedDistanceM1(address_2,-lift_speed_pulses,-lift_increment,1)
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
        return (''), 204



@app.route('/app_home', methods=['POST'])
def function_home():
    rc.BackwardM1(address, pitch_speed_manual)
    rc.BackwardM1(address_2, lift_speed_manual)
    rc.BackwardM2(address_2, launch_speed_manual)
    #rc.SpeedM2(address_2,-launch_speed_pulses_slow) #Using the speed control instead of the duty cycle because the friction changes in the tube
    #Missing rotation limit switch
    return (''), 204

@app.route('/app_reset_encoders', methods=['POST'])
def function_reset_encoders():
    #rc.ResetEncoders(address)
    #rc.ResetEncoders(address_2)
    global encoders_ready
    encoders_ready = 1 #Encoders have been reset
    return (''), 204

@app.route('/app_battery_voltage', methods=['POST'])
def function_battery_voltage():
    voltage = round(0.1*rc.ReadMainBatteryVoltage(address)[1],2)
    return jsonify(voltage=voltage)



@app.route('/app_stop', methods=['POST'])

def function_stop():
    rc.ForwardM1(address,0)
    rc.ForwardM2(address,0)
    rc.ForwardM1(address_2,0)
    rc.ForwardM2(address_2,0)
    return (''), 204



@app.route('/app_standby', methods=['POST'])
def function_standby():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403

    pitch_objective = 0
    pitch_actual = rc.ReadEncM1(address)[1]
    pitch_increment = pitch_objective-pitch_actual
    if pitch_increment >= 0:
        rc.SpeedDistanceM1(address,pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM1(address,-pitch_speed_pulses,-pitch_increment,1)
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration

    rotation_objective = 0
    rotation_actual = rc.ReadEncM2(address)[1]
    rotation_increment = rotation_objective-rotation_actual
    if rotation_increment >= 0:
        rc.SpeedDistanceM2(address,rotation_speed_pulses,rotation_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM2(address,-rotation_speed_pulses,-rotation_increment,1)
        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration

    lift_objective = 0
    lift_actual = rc.ReadEncM1(address_2)[1]
    lift_increment = lift_objective-lift_actual
    if lift_increment >= 0:
        rc.SpeedDistanceM1(address_2,lift_speed_pulses,lift_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM1(address_2,-lift_speed_pulses,-lift_increment,1)
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration

    launch_objective = launch_bottom
    launch_actual = rc.ReadEncM2(address_2)[1]
    launch_increment = launch_objective-launch_actual
    if launch_increment >= 0:
        rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM2(address_2,-launch_speed_pulses_slow,-launch_increment,1)
        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
    rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_standby,0) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
    rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
    return (''), 204

@app.route('/app_prepare', methods=['POST'])
def function_prepare():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403

    if pitch_ready == 0:
        pitch_objective = 0
    else:
        pitch_objective = int(pitch_pulses/(pitch_length/pitch_ready))
    pitch_actual = rc.ReadEncM1(address)[1]
    pitch_increment = pitch_objective-pitch_actual
    if pitch_increment >= 0:
        rc.SpeedDistanceM1(address,pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM1(address,-pitch_speed_pulses,-pitch_increment,1)
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration

    if rotation_ready == 0:
        rotation_objective = 0
    else:
        rotation_objective = int(rotation_pulses/(rotation_length/rotation_ready))
    rotation_actual = rc.ReadEncM2(address)[1]
    rotation_increment = rotation_objective-rotation_actual
    if rotation_increment >= 0:
        rc.SpeedDistanceM2(address,rotation_speed_pulses,rotation_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM2(address,-rotation_speed_pulses,-rotation_increment,1)
        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration

    if lift_ready == 0:
        lift_objective = 0
    else:
        lift_objective = int(lift_pulses/(lift_length/lift_ready))
    lift_actual = rc.ReadEncM1(address_2)[1]
    lift_increment = lift_objective-lift_actual
    if lift_increment >= 0:
        rc.SpeedDistanceM1(address_2,lift_speed_pulses,lift_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM1(address_2,-lift_speed_pulses,-lift_increment,1)
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration

    launch_objective = launch_bottom
    launch_actual = rc.ReadEncM2(address_2)[1]
    launch_increment = launch_objective-launch_actual
    if launch_increment >= 0:
        rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM2(address_2,-launch_speed_pulses_slow,-launch_increment,1)
        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration

    return (''), 204

@app.route('/app_launch', methods=['POST'])
def function_launch():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403

    launch_objective = launch_bottom
    launch_actual = rc.ReadEncM2(address_2)[1]
    launch_increment = launch_objective-launch_actual
    if launch_increment >= 0:
        rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM2(address_2,-launch_speed_pulses_slow,-launch_increment,1)
        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration

    rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_connect,0) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
    rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration

    launch_objective = launch_break
    launch_actual = launch_connect
    launch_increment = launch_objective-launch_actual
    rc.SpeedAccelDistanceM2(address_2,launch_acceleration,launch_speed_pulses,launch_increment,0)
    rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration

    return (''), 204

@app.route('/app_mount', methods=['POST'])
def function_mount():
    if encoders_ready == 0: #Not execute if the encoders are not ready
        return (''), 403

    pitch_objective = pitch_pulses
    pitch_actual = rc.ReadEncM1(address)[1]
    pitch_increment = pitch_objective-pitch_actual
    if pitch_increment >= 0:
        rc.SpeedDistanceM1(address,pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM1(address,-pitch_speed_pulses,-pitch_increment,1)
        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration

    rotation_objective = 0
    rotation_actual = rc.ReadEncM2(address)[1]
    rotation_increment = rotation_objective-rotation_actual
    if rotation_increment >= 0:
        rc.SpeedDistanceM2(address,rotation_speed_pulses,rotation_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM2(address,-rotation_speed_pulses,-rotation_increment,1)
        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration

    lift_objective = 0
    lift_actual = rc.ReadEncM1(address_2)[1]
    lift_increment = lift_objective-lift_actual
    if lift_increment >= 0:
        rc.SpeedDistanceM1(address_2,lift_speed_pulses,lift_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM1(address_2,-lift_speed_pulses,-lift_increment,1)
        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration

    launch_objective = launch_bottom
    launch_actual = rc.ReadEncM2(address_2)[1]
    launch_increment = launch_objective-launch_actual
    if launch_increment >= 0:
        rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
    else:
        rc.SpeedDistanceM2(address_2,-launch_speed_pulses_slow,-launch_increment,1)
        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
    rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_mount,0) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
    rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration

    return (''), 204

# Automatic launch works, but it is disabled becuase the loop while prevents
# the motors to stop when the button Stop is pressed, making it dangerous

##@app.route('/app_automatic_launch', methods=['POST'])
##def function_automatic_launch():
##    if encoders_ready == 0: #Not execute if the encoders are not ready
##        return (''), 403
##
##    #Prepare
##    if pitch_ready == 0:
##        pitch_objective = 0
##    else:
##        pitch_objective = int(pitch_pulses/(pitch_length/pitch_ready))
##    pitch_actual = rc.ReadEncM1(address)[1]
##    pitch_increment = pitch_objective-pitch_actual
##    if pitch_increment >= 0:
##        rc.SpeedDistanceM1(address,pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
##    else:
##        rc.SpeedDistanceM1(address,-pitch_speed_pulses,-pitch_increment,1)
##        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
##
##    if rotation_ready == 0:
##        rotation_objective = 0
##    else:
##        rotation_objective = int(rotation_pulses/(rotation_length/rotation_ready))
##    rotation_actual = rc.ReadEncM2(address)[1]
##    rotation_increment = rotation_objective-rotation_actual
##    if rotation_increment >= 0:
##        rc.SpeedDistanceM2(address,rotation_speed_pulses,rotation_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration
##    else:
##        rc.SpeedDistanceM2(address,-rotation_speed_pulses,-rotation_increment,1)
##        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration
##
##    if lift_ready == 0:
##        lift_objective = 0
##    else:
##        lift_objective = int(lift_pulses/(lift_length/lift_ready))
##    lift_actual = rc.ReadEncM1(address_2)[1]
##    lift_increment = lift_objective-lift_actual
##    if lift_increment >= 0:
##        rc.SpeedDistanceM1(address_2,lift_speed_pulses,lift_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
##    else:
##        rc.SpeedDistanceM1(address_2,-lift_speed_pulses,-lift_increment,1)
##        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
##
##    launch_objective = launch_bottom
##    launch_actual = rc.ReadEncM2(address_2)[1]
##    launch_increment = launch_objective-launch_actual
##    if launch_increment >= 0:
##        rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
##    else:
##        rc.SpeedDistanceM2(address_2,-launch_speed_pulses_slow,-launch_increment,1)
##        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
##    rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_connect,0) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##    rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
##
##    buffer_1 = (0,0,0)
##    buffer_2 = (0,0,0)
##    while(buffer_1[1]!=0x80): #Loop until pitch is completed
##        buffer_1 = rc.ReadBuffers(address)
##    while(buffer_1[2]!=0x80): #Loop until rotation is completed
##        buffer_1 = rc.ReadBuffers(address)
##    while(buffer_2[1]!=0x80): #Loop until lift is completed
##        buffer_2 = rc.ReadBuffers(address_2)
##    while(buffer_2[2]!=0x80): #Loop until launch is completed
##        buffer_2 = rc.ReadBuffers(address_2)
##    #The loop does not work with AND conditions
##    time.sleep(2)
##
##    #Launch
##    launch_objective = launch_break
##    launch_actual = rc.ReadEncM2(address_2)[1]
##    launch_increment = launch_objective-launch_actual
##    rc.SpeedDistanceM2(address_2,launch_speed_pulses,launch_increment,0) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##    rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
##
##    while(buffer_2[2]!=0x80): #Loop until launch is completed
##        buffer_2 = rc.ReadBuffers(address_2)
##    #The loop does not work with AND conditions
##    time.sleep(2)
##
##    #Standby
##    pitch_objective = 0
##    pitch_actual = rc.ReadEncM1(address)[1]
##    pitch_increment = pitch_objective-pitch_actual
##    if pitch_increment >= 0:
##        rc.SpeedDistanceM1(address,pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
##    else:
##        rc.SpeedDistanceM1(address,-pitch_speed_pulses,-pitch_increment,1)
##        rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
##
##    rotation_objective = 0
##    rotation_actual = rc.ReadEncM2(address)[1]
##    rotation_increment = rotation_objective-rotation_actual
##    if rotation_increment >= 0:
##        rc.SpeedDistanceM2(address,rotation_speed_pulses,rotation_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration
##    else:
##        rc.SpeedDistanceM2(address,-rotation_speed_pulses,-rotation_increment,1)
##        rc.SpeedDistanceM2(address,0,0,0) #To avoid deceleration
##
##    lift_objective = 0
##    lift_actual = rc.ReadEncM1(address_2)[1]
##    lift_increment = lift_objective-lift_actual
##    if lift_increment >= 0:
##        rc.SpeedDistanceM1(address_2,lift_speed_pulses,lift_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
##    else:
##        rc.SpeedDistanceM1(address_2,-lift_speed_pulses,-lift_increment,1)
##        rc.SpeedDistanceM1(address_2,0,0,0) #To avoid deceleration
##
##    launch_objective = launch_bottom
##    launch_actual = rc.ReadEncM2(address_2)[1]
##    launch_increment = launch_objective-launch_actual
##    if launch_increment >= 0:
##        rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
##    else:
##        rc.SpeedDistanceM2(address_2,-launch_speed_pulses_slow,-launch_increment,1)
##        rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
##    rc.SpeedDistanceM2(address_2,launch_speed_pulses_slow,launch_standby,0) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
##    rc.SpeedDistanceM2(address_2,0,0,0) #To avoid deceleration
##
##    return (''), 204


@app.route('/app_change_pitch', methods=['POST'])
def function_change_pitch():
    pitch_position_prepare = request.form.get('pitch_position_prepare', type=int)
    if pitch_position_prepare > pitch_length or pitch_position_prepare < 0:
        return (''), 400
    global pitch_ready
    pitch_ready = float(pitch_position_prepare)
    return (''), 204

@app.route('/app_change_lift', methods=['POST'])
def function_change_lift():
    lift_position_prepare = request.form.get('lift_position_prepare', type=int)
    if lift_position_prepare > lift_length or lift_position_prepare < 0:
        return (''), 400
    global lift_ready
    lift_ready = float(lift_position_prepare)
    return (''), 204

@app.route('/app_change_rotation', methods=['POST'])
def function_change_rotation():
    rotation_position_prepare = request.form.get('rotation_position_prepare', type=int)
    if rotation_position_prepare > rotation_length or rotation_position_prepare < 0:
        return (''), 400
    global rotation_ready
    rotation_ready = float(rotation_position_prepare)
    return (''), 204

@app.route('/app_change_speed', methods=['POST'])
def function_change_speed():
    speed = request.form.get('speed', type=int)
    if speed > launch_max_speed or speed < launch_min_speed:
        return (''), 400
    global launch_speed_pulses
    global launch_acceleration
    if speed > 7:
        launch_speed_pulses = speed*13400
        launch_acceleration = 655360 #Maximum value
        return (''), 204
    else:
        launch_speed_pulses = speed*13400
        launch_acceleration = (launch_speed_pulses**2)/13400
        return (''), 204

@app.route('/app_change_acceleration', methods=['POST'])
def function_change_acceleration():
    acceleration = request.form.get('acceleration', type=int)
    if acceleration > launch_max_acceleration or acceleration < launch_min_acceleration:
        return (''), 400
    acceleration = acceleration*13400
    global launch_acceleration
    launch_acceleration = acceleration
    return (''), 204


@app.route('/app_disable_buttons', methods=['POST'])
def function_disable_buttons():
    return jsonify(encoders_ready=encoders_ready)


#Specify IP address and port for the server

if __name__ == "__main__":
    ##app.run(host=host,port=port)
    app.run(debug=True)
