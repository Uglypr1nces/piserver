import socket
import threading
import pyttsx3
import time
import subprocess
import pygame
from pygame import mixer
from robot.robot_actions import Robot

pygame.init()
pygame.mixer.init()

engine = pyttsx3.init()
alarmSound = "sounds/quck.mp3"

class Server:
    def __init__(self, host, port, header=64, format="utf-8", disconnect_cmd="!bye"):
        self.host = host
        self.port = port
        self.header = header
        self.format = format
        self.disconnect_cmd = disconnect_cmd
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        
        # Robot
        self.servoangle = 3
        self.pan_angle = 0
        self.tilt_angle = 0
        self.direction = None
        self.robot = Robot()
        self.lock = threading.Lock()

    def cleanup(self):
        self.robot.set_servo_angle(0)
        self.robot.set_camera_angles(0, 0)
        self.robot.stop()
        time.sleep(0.2)

    def start(self):
        self.server_socket.listen()
        print(f"Server started on {self.host}:{self.port}...")
        try:
            while True:
                conn, addr = self.server_socket.accept()
                print(f"Connected to {addr}")
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.cleanup()

    def handle_client(self, conn, addr):
        print(f"New connection from {addr}")
        connected = True
        while connected:
            try:
                msg_length = conn.recv(self.header).decode(self.format)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(self.format)
                    print(f"Received message: {msg}")
                    self.process_message(msg)
                    if msg == self.disconnect_cmd:
                        connected = False
            except (ConnectionResetError, ConnectionAbortedError):
                break
        conn.close()

    def process_message(self, msg):
        with self.lock:
            if msg == "forward":
                self.direction = "forward"
            elif msg == "backward":
                self.direction = "backward"
            elif msg == "right":
                self.direction = "right"
            elif msg == "left":
                self.direction = "left"
            elif msg == "stop":
                self.direction = None
            elif msg == "camera_up":
                self.tilt_angle += 4
            elif msg == "camera_down":
                self.tilt_angle -= 4
            elif msg == "camera_left":
                self.pan_angle += 4
            elif msg == "camera_right":
                self.pan_angle -= 4
            elif msg == "over_sound":
                subprocess.call("shutdown.sh")
            elif msg == "alarm_sound":
                mixer.music.load(alarmSound)
                mixer.music.play()
            elif msg.startswith("word"):
                print(msg[4:])
                engine.say(msg[4:])
                engine.runAndWait()

            self.update_robot()

    def update_robot(self):
        if self.direction == "forward":
            self.robot.move_forward()
        elif self.direction == "backward":
            self.robot.move_backward()
        elif self.direction == "right":
            self.servoangle += 3
        elif self.direction == "left":
            self.servoangle -= 3
        else:
            self.robot.stop()

        self.robot.set_servo_angle(self.servoangle)
        self.robot.set_camera_angles(self.pan_angle, self.tilt_angle)

if __name__ == "__main__":
    server = Server("127.0.0.1", 5555)
    server.start()
