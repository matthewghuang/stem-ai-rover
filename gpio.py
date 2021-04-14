from gpiozero import DistanceSensor
from time import sleep
import socketio

sio = socketio.Client()
sio.connect("ws://localhost:3000")

echo_1, trigger_1 = 21, 20
echo_2, trigger_2 = 21, 20
echo_3, trigger_3 = 21, 20

distance_sensor_1 = DistanceSensor(echo=echo_1, trigger=trigger_1)
distance_sensor_2 = DistanceSensor(echo=echo_2, trigger=trigger_2)
distance_sensor_3 = DistanceSensor(echo=echo_3, trigger=trigger_3)

#    d2
# d1----d3
#  /    \
# /      \

threshold = 0.25

def move(direction, sleep_time):
    sio.emit("set_direction", direction)
    sleep(sleep_time)
    sio.emit("set_direction", sleep_time)

def move_routine():
    distance_1 = distance_sensor_1.distance
    distance_2 = distance_sensor_2.distance
    distance_3 = distance_sensor_3.distance

    if distance_1 >= threshold and distance_2 >= threshold and distance_3 >= threshold:
        print("moving forward")
        move("up", 1)
    elif distance_1 < threshold:
        print("Moving right")
        move("right", 1)
    elif distance_2 < threshold:
        print("Moving back")
        move("back", 1)
    elif distance_3 < threshold:
        print("Moving left")
        move("left", 1)


def main():
    while True:
        move_routine()
                    
        sleep(0.5)

if __name__ == "__main__":
    main()
