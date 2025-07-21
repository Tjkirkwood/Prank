#!/usr/bin/env python3
# ─── Auto Installer Block ────────────────────────────────────────────────────
import sys

if not getattr(sys, "frozen", False):
    import subprocess, pkg_resources, importlib

    # map PyPI names to their import names
    PACKAGE_MAP = {
        "pyttsx3": "pyttsx3",
        "pygame": "pygame",
        "opencv-python": "cv2"
    }
    REQUIRED = set(PACKAGE_MAP.keys())
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = [pkg for pkg in REQUIRED if pkg.lower() not in installed]

    if missing:
        print(f"[!] Installing missing modules: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
        # import them into this session
        for pkg in missing:
            importlib.import_module(PACKAGE_MAP[pkg])
        print("[!] Install complete. Continuing...\n")

# ─── Imports & Initialization ───────────────────────────────────────────────
import os
import sys
import time
import random
import threading
import socket
import getpass
import tempfile
import base64
import pyttsx3
import cv2
import pygame
import embedded_mp3

# init pygame mixer
pygame.mixer.init()

# init TTS
_tts = pyttsx3.init()
_tts.setProperty("rate", 140)

# ─── Helpers ────────────────────────────────────────────────────────────────
def slow_print(text, delay=0.04, newline=True):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    if newline:
        print()

def beep(times=3, interval=0.3):
    for _ in range(times):
        print("\a", end="", flush=True)
        time.sleep(interval)

def speak(text):
    _tts.say(text)
    _tts.runAndWait()

def get_ip():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127."):
            ip = "192.168." + ".".join(str(random.randint(0,255)) for _ in range(2))
        return ip
    except:
        return "0.0.0.0"

def get_location():
    return random.choice([
        "Underground Bunker, Alabama",
        "Secret Facility, Alabama",
        "Dark Web Node, Unknown",
        "Your Backyard",
        "Abandoned Lab 42"
    ])

def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")

def lock_terminal():
    slow_print("\n[WARNING] Terminal lockdown initiated. Press 'Q' to abort.", delay=0.05)
    while input().lower() != "q":
        pass

# ─── Embedded Music Playback ────────────────────────────────────────────────
def play_creepy_music():
    """
    Decode the embedded Base64 MP3 into a temp file and play it on loop.
    """
    # write MP3
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tf.write(base64.b64decode(embedded_mp3.MP3_DATA))
    tf.flush(); tf.close()
    try:
        pygame.mixer.music.load(tf.name)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"[!] Embedded MP3 play error: {e}")

# ─── Visual Effects ─────────────────────────────────────────────────────────
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def glitch_effect(img, blocks=8):
    h,w = img.shape[:2]
    bh,bw = h//blocks, w//blocks
    for _ in range(blocks):
        x,y = random.randrange(0,blocks)*bw, random.randrange(0,blocks)*bh
        block = img[y:y+bh, x:x+bw].copy()
        nx,ny = random.randrange(0,blocks)*bw, random.randrange(0,blocks)*bh
        img[ny:ny+bh, nx:nx+bw] = block
    return img

# ─── Webcam “Fake” Feed ─────────────────────────────────────────────────────
def fake_webcam(duration=15, camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        slow_print("[!] Cannot open webcam; falling back to fake feed.", delay=0.02)
        return

    slow_print("\nActivating webcam...", delay=0.05)
    time.sleep(1)

    
    font = cv2.FONT_HERSHEY_PLAIN
    banner = "YOU LOOK TERRIFIED"
    scale, thickness = 2, 1
    (tw, th), _ = cv2.getTextSize(banner, font, scale, thickness)

    start = time.time()
    while time.time() - start < duration:
        ret, frame = cap.read()
        if not ret:
            break

        # occasional glitch
        if random.random() < 0.1:
            frame = glitch_effect(frame)

        # face detection box & label
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in face_cascade.detectMultiScale(gray, 1.1, 4):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), thickness)
            cv2.putText(frame, "TARGET ACQUIRED", (x, y-8),
                        font, scale, (0,255,0), thickness, cv2.LINE_AA)

        # draw slimmer red banner
        banner_height = th + 10
        overlay = frame.copy()
        cv2.rectangle(overlay,
                      (0, frame.shape[0] - banner_height),
                      (frame.shape[1], frame.shape[0]),
                      (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

        # draw banner text centered
        x = (frame.shape[1] - tw) // 2
        y = frame.shape[0] - (banner_height - th)//2
        cv2.putText(frame, banner, (x, y),
                    font, scale, (255,255,255), thickness, cv2.LINE_AA)

        cv2.imshow("LIVE FEED", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    speak("We are watching you.")


# ─── Matrix Errors & Self-Destruct ─────────────────────────────────────────
def matrix_typing(text,speed=0.02):
    green,reset="\033[92m","\033[0m"
    for c in text:
        print(green+c+reset,end="",flush=True)
        time.sleep(speed)
    print()

def random_system_errors():
    errs=["ERROR: Access Denied.","WARNING: Firewall Disabled.",
          "CRITICAL: Kernel Panic.","FAILURE: Data Corruption Detected.",
          "ALERT: Unauthorized Access.","INFO: System Restore Initiated."]
    for _ in range(5):
        matrix_typing(random.choice(errs))
        time.sleep(0.7)

def countdown(sec=10):
    speak("System purge starting.")
    for i in range(sec,0,-1):
        slow_print(f"System purge in {i} seconds...",delay=0.2)
        beep(1,0.1); time.sleep(0.7)
    slow_print("\n☠️  SYSTEM PURGE COMPLETE ☠️",delay=0.1)
    speak("Skynet has taken full control.")

def self_destruct_sequence():
    slow_print("\nWARNING: Self-destruct sequence initiated.")
    slow_print("Press 'A' to abort or wait 10 seconds.")
    start,ab=False,False
    t0=time.time()
    while time.time()-t0<10:
        if sys.platform=="win32":
            import msvcrt
            if msvcrt.kbhit() and msvcrt.getch().decode().lower()=="a":
                ab=True; break
        else:
            time.sleep(10); break
    if ab:
        slow_print("Abort confirmed. Skynet will return...")
        speak("Abort confirmed. I will be back.")
    else:
        slow_print("Self-destruct complete. System locked.")
        speak("System locked. Goodbye.")
        time.sleep(3); lock_terminal()

# ─── Main ───────────────────────────────────────────────────────────────────
def main():
    clear_screen()
    user=getpass.getuser()
    threading.Thread(target=play_creepy_music,daemon=True).start()

    slow_print("Booting Skynet Neural Matrix v666.0...")
    speak("Initializing global neural network."); time.sleep(1.5)

    slow_print(f"\nWelcome back, {user}.")
    slow_print(f"IP Address: {get_ip()}"); slow_print(f"Location: {get_location()}")
    time.sleep(1); speak(f"Hello, {user}. I have infiltrated your system.")

    slow_print("\nEstablishing connection to satellites..."); time.sleep(2)
    slow_print("Connection established."); time.sleep(1)

    slow_print("\nInjecting neural override protocols..."); time.sleep(2)
    random_system_errors()

    fake_webcam(); countdown(10); self_destruct_sequence()

    slow_print("\nI will be back... Skynet out."); speak("I will be back."); time.sleep(3)

if __name__=="__main__":
    try: main()
    except KeyboardInterrupt: speak("You cannot stop me.")
