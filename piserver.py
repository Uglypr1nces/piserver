import pygame
from pygame import mixer
import pyttsx3
from time import sleep
from robot.server_managment import Server

pygame.init()
pygame.mixer.init()

class Main:
    def __init__(self):
        self.engine = pyttsx3.init()
        mixer.init()
        self.server = Server(host="192.168.0.40", port=5555)

        self.start_sound = pygame.mixer.Sound("sounds/start.wav")
        self.over_sound = pygame.mixer.Sound("sounds/over.wav")
        self.alarm_sound = pygame.mixer.Sound("sounds/quack.mp3")

    def start(self):
        try:
            self.start_sound.play()
            self.server.start()
        finally:
            self.cleanup()

    def cleanup(self):
        self.server.cleanup()
        self.over_sound.play()


if __name__ == "__main__":
    main = Main()
    main.start()
