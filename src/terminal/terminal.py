import pyfiglet
import os
import sys
import socket
import netifaces
import cv2
from datetime import datetime
from colorama import Fore

hostname = socket.gethostname()

COLORS = {
    "Error": Fore.RED,
    "Warning": Fore.YELLOW,
    "Success": Fore.GREEN,
    "Info": Fore.BLUE,
    "Reset": Fore.WHITE
}

def conn_camera(ip: str, port: int) -> None:
    try:
        camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        camera_socket.connect((ip, port))
        print(f"{COLORS['Success']}[SUCCESS]: Connected to camera at {ip}:{port}{COLORS['Reset']}")
        cap = cv2.VideoCapture(f"http://{ip}:{port}")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Camera Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            cap.release()
            cv2.destroyAllWindows()
    except ConnectionRefusedError:
        print(f"{COLORS['Error']}[ERROR]: Failed to connect {ip}:{port}. Connection refused.{COLORS['Reset']}")
    except Exception as e:
        print(f"{COLORS['Error']}[ERROR]: An error occurred while connecting to {ip}:{port}: {str(e)}{COLORS['Reset']}")

def find_cameras() -> list[str]:
    interfaces = netifaces.interfaces()
    cameras = []

    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for address in addresses[netifaces.AF_INET]:
                ip = address['addr']
                if ip.startswith('192.168.0.'):
                    cameras.append(ip)
    return cameras

if os.name != "posix":
    print(f"{COLORS['Error']}[ERROR]: This script is designed to run on Linux. Exiting...{COLORS['Reset']}")
    sys.exit()

def show_conn() -> list[str]:
    camera_connections = []
    try:
        if not camera_connections:
            print(f"{COLORS['Info']}[INFO]: No camera connections available.{COLORS['Reset']}")
            return 
        
        for idx, (ip, port) in enumerate(camera_connections, start=1):
            print(f"Connection {idx}: {ip}:{port}")
    except Exception as e:
        print(f"{COLORS['Error']}[ERROR]: An error occurred while finding camera connections: {str(e)}{COLORS['Reset']}")

def help() -> None:
    print("Help Menu:\n")
    print("help\t\t- Shows this menu")
    print("exit\t\t- Exits the terminal")
    print("find\t\t- Finds camera connections on the network")
    print("connect <ip>:<port>\t- Connect to a camera using the specified IP address and port")

def banner() -> None:
    banner = pyfiglet.figlet_format("ISPY", font="bloody")
    print(f"{Fore.RED}{banner}{Fore.WHITE}")

    print('-'*50)
    print(datetime.now())
    print('-'*50)

def terminal(logged_in_user: str) -> None:
    if logged_in_user is not None:
        command_mapping = {
            "exit": exit,
            "help": help,
            "clear": lambda: os.system('clear'),
            "find": lambda: find_cameras(),
            "connect": conn_camera,
            "show": show_conn,
        }

        while True:
            userInput = input(f'{logged_in_user.username}@[{hostname}]~$ ')
            command, *args = userInput.split()
            if command in command_mapping:
                command_function = command_mapping[command]
                try:
                    if args:
                        command_function(*args)
                    else:
                        command_function()
                except Exception as e:
                    print(f"{COLORS['Error']}[ERROR]: An error occurred: {str(e)}{COLORS['Reset']}")
            else:
                print(f"{COLORS['Error']}[ERROR]: '{command}' is not a recognized command.{COLORS['Reset']}")
    else:
        print(f"{COLORS['Error']}[ERROR]: Please log in first.{COLORS['Reset']}")