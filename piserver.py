import pygame
from pygame import mixer
import pyttsx3
from time import sleep
from robot.server_managment import Server
from robot.robot_actions import Robot

class Main:
    def __init__(self):
        self.engine = pyttsx3.init()
        mixer.init()
        self.server = Server(host="192.168.1.71", port=5555)
        self.robot = Robot()

    def start(self):
        try:
            start_sound = pygame.mixer.Sound("sounds/sounds/sounds/start.wav")
            over_sound = pygame.mixer.Sound("sounds/sounds/sounds/over.wav")
            alarm_sound = pygame.mixer.Sound("sounds/sounds/sounds/quack.mp3")
            start_sound.play()
            self.server.start()
        finally:
            self.cleanup()

    def cleanup(self):
        self.robot.set_servo_angle(0)
        self.robot.set_camera_angles(0, 0)
        self.robot.px.stop()
        sleep(0.2)
        over_sound.play()


if __name__ == "__main__":
    main = Main()
    main.start()
