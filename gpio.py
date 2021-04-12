from gpiozero import DistanceSensor
from time import sleep
import socketio

sio = socketio.Client()
sio.connect("ws://localhost:3000")

distance_sensor = DistanceSensor(echo=21, trigger=20, max_distance=1)

threshold = 0.3

previous_action = "right"

def move(direction):
    sio.emit("set_direction", direction)

def main():
    global previous_action

    while True:
        distance = distance_sensor.distance

        if distance >= threshold:
            move("up")
            sleep(0.5)
            move("")
        else:
            if previous_action == "right":
                move("left")
                sleep(0.5)
                move("")
                previous_action = "left"
                print("moving left to avoid obstacle")
            elif previous_action == "left":
                move("right")
                sleep(1)
                move("")
                previous_action = "right"
                print("moving right to avoid obstacle")

        print("Distance: {}".format(distance_sensor.distance))
        sleep(0.1)

if __name__ == "__main__":
    main()
