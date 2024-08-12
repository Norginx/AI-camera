import asyncio
import edge_tts
import requests
import cv2
import base64
import pygame
import Hobot.GPIO as GPIO
import time

VOICE = "zh-CN-XiaoyiNeural"
OUTPUT_FILE = "output.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(string, VOICE)
    await communicate.save(OUTPUT_FILE)



GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

while True:
    if GPIO.input(11)!=GPIO.HIGH:
        time.sleep(0.01)
        if GPIO.input(11)!=GPIO.HIGH:
            print("get")
            cap = cv2.VideoCapture(8)
            if not cap.isOpened():
                print("camera is not opened")
                exit()
    		
            ret, frame = cap.read()
            if not ret:
                print("camera is not opened")
                exit()
            cv2.imwrite('output.jpg', frame)
            buffer = cv2.imencode('.jpg', frame)[1].tobytes()
            base64_image = base64.b64encode(buffer).decode('ascii')
            cap.release()
            url = 'http://192.168.1.189:11434/api/generate'
            data = {
                "model": "llava",
                "prompt": "请使用中文，详细地回答我图片中有什么?",
                "stream": False,
                "images": [base64_image]
            }
            response = requests.post(url, json=data)
            buf = response.json()
            string = f"{buf['response']}"
            print(string)

            loop = asyncio.get_event_loop_policy().get_event_loop()
            loop.run_until_complete(amain())

            pygame.mixer.init()
            devices = pygame.mixer.get_init()
            print(devices)
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.quit()
            print("done")
