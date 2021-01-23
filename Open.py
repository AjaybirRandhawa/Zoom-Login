import pyautogui as auto
import time
from datetime import datetime
import calendar
import cv2
import os

monday_times = {}
tuesday_times = {}
wednesday_times = {}
thursday_times = {}
friday_times = {}
saturday_times = {}
sunday_times = {}

days = {
        'monday': monday_times,
        'tueday': tuesday_times,
        'wednesday': wednesday_times,
        'thursday': thursday_times,
        'friday': friday_times,
        'saturday': saturday_times,
        'sunday': sunday_times
    }

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\u001b[37m'

def isnum(s, hour=False):
    try:
        x = int(s)
        if hour:
            if x >= 0 and x <= 24:
                return True
            return False
        return True
    except ValueError:
        return False

def recordVideo():
    pass

def readFile():
    file = open("config.txt", "r")
    lines = file.read()
    lines = lines.split("!")
    lines.pop()
    all_results = []
    for x, line in enumerate(lines):
        if x != len(line):
            items = line.split('+')
            items.pop()
            items[0], items[1], items[2] = items[0].lower(), int(items[1]), int(items[2])
            all_results.append(items)
    for clas in all_results:
        time = (clas[1], clas[2])
        day = clas[0]
        meeting = clas[3]
        if len(clas) == 5:
            password = clas[4]
            for index in range(clas[1], clas[2]):
                days[day][index] = [meeting, password]
        for index in range(clas[1], clas[2]):
            days[day][index] = [meeting]
    
def getInfo():
    print(bcolors.WHITE + """
Please enter the day, starting time (24h format), ending time (24h format), meeting number, 
and password if required separated by commas. Once you're done, type DONE. 
NOTE: No overlap and the order of classes does not matter.""" + bcolors.OKCYAN +"""
    
Examples:
    Monday, 8, 9, 12345567890, 00000
    The above will be seen as: Monday, 8AM to 9 AM, Meeting id: 12345567890, Password: 00000
    Friday, 15, 17, 1234567890
    The above will be seen as: Friday, 3PM to 5 PM, Meeting id: 12345567890 with no password
    """ + bcolors.WHITE)
    info = []
    overlap = False
    all_input = []
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        line = str(input("Enter:"))
        if line.lower() == "done":
            break
        info = line.split(',')
        if (len(info) > 5) or (len(info) < 4):
            print("You entered incorrect information, please look at the examples.")
            continue
        if info[0].lower() not in weekdays:
            print("You entered an invalid day, please try again.")
            continue
        if not(isnum(info[1], True) and isnum(info[2], True) and isnum(info[3])):
            print("You entered incorrect numbers.")
            continue
        info[0], info[1], info[2], info[3] = info[0].lower(), int(info[1]), int(info[2]), int(info[3])
        if (info[1] >= info[2]):
            print("Start time can not be bigger or same as end time!")
            continue
        for ans in all_input:
            if (ans[0] == info[0]) and ((ans[1] <= info[1] < ans[2]) or (ans[1] < info[2] <= ans[2])):
                overlap = True
        if overlap == True:
            overlap = False
            print("There is an overlap, please re check and re enter.")
            continue
        if len(info) == 5:
            if not (isnum(info[4])):
                print("You entered incorrect password.")
                continue
            info[4] = int(info[4])
        all_input.append(info)
    file = open("config.txt", "w")
    for items in all_input:
        for item in items:
            file.write(str(item) + "+")
        file.write("!")
    file.close()

def stop():
    print(bcolors.HEADER + """
      ________                     .___ _________                 
     /  _____/   ____    ____    __| _/ \_____   \ ___.__.  ____  
    /   \  ___  /  _ \  /  _ \  / __ |   |   |  _/<   |  |_/ __ \ 
    \    \_\  \(  <_> )(  <_> )/ /_/ |   |   |   \ \___  |\  ___/ 
     \______  / \____/  \____/ \____ |   |_____  / / ____| \___  >
            \/                      \/         \/  \/          \/ 
    """ + bcolors.WHITE)
    print(bcolors.OKCYAN + """
    ------------------------------------------------------------
                      BY: Ajaybir Randhawa
                    Ryerson University, 2021
    ------------------------------------------------------------""" + bcolors.WHITE)

def timeChecker(now, weekday):
    for key in days[weekday]:
        if now.hour == key:

            return days[weekday][key]

    return None
def starting(turn_vid, turn_audio):
    readFile()
    while True:
        now = datetime.now()
        current_day = now.weekday()
        current_day = calendar.day_name[current_day].lower()
        password = timeChecker(now, current_day)
        if password != None:
            openZoom(password, turn_vid, turn_audio)
            break
        ctrlAbort = cv2.waitKey(1) & 0xFF
        if ctrlAbort == ord("a"):
            break
    stop()
    quit()

def Intro():
    os.system("cls")
    print(bcolors.OKBLUE + """
__      __       .__                               
/  \    /  \ ____ |  |      ____    _____    _____    _____ 
\   \/\/   // __ \|  |    _/ ___\  /  _  \  /     \__/ __  \  
 \        /\  ___/|  |___ \  \___ (  <_>  )/   Y Y   \  ___/ 
  \__/\  /  \___  >______/ \_____> \_____/ \ |__|_|  /\___  >
       \/       \/          \/              \/     \/     \/ 
    
    """+ bcolors.WHITE)
    print(bcolors.OKBLUE + """
Logger is a Python program developed by Ajaybir Randhawa making use of the PyautoGUI library
to better focus in Zoom classes, providing a virtual background, subtitles and automatic
logging functionality. Users must have downloaded zoom, be using windows, and be logged in 
with school credentials prior to starting the program. That aside, please follow the 
instructions below carefully.

Notes:
Github: https://github.com/AjaybirRandhawa/Zoom-Login
Download Zoom: https://zoom.us/client/latest/ZoomInstaller.exe
Icon by: https://icons8.com

""" + bcolors.WHITE)
    if not(os.path.exists("config.txt")):
        print(bcolors.OKBLUE + "Since this is your first time, please enter your information as follows:" + bcolors.WHITE)
        getInfo()
    else:
        #Ask user regarding information change
        ans = str(input(bcolors.OKBLUE + "Do you wish to change your class information? NOTE: Doing so will remove previous information completely. [Yes/No]" + bcolors.WHITE)).lower()
        while ("yes" != ans) and ("no" != ans):
            print(bcolors.FAIL + "Invalid input! Please enter Yes or No."+ bcolors.WHITE)
            ans = str(input(bcolors.OKBLUE + "Do you wish to change your class information? NOTE: Doing so will remove previous information completely. [Yes/No]" + bcolors.WHITE)).lower()
        if ans == "yes":
            getInfo()
    turn_vid = str(input(bcolors.OKBLUE + "Do you wish to turn on video? [Yes/No]" + bcolors.WHITE)).lower()
    while ("yes" != turn_vid) and ("no" != turn_vid):
        print(bcolors.FAIL + "Invalid input! Please enter Yes or No."+ bcolors.WHITE)
        turn_vid = input(bcolors.OKBLUE + "Do you wish to turn on video? [Yes/No]" + bcolors.WHITE).lower()
    turn_audio = str(input(bcolors.OKBLUE + "Do you wish to turn on audio? [Yes/No]" + bcolors.WHITE)).lower()
    while ("yes" != turn_audio) and ("no" != turn_audio):
        print(bcolors.FAIL + "Invalid input! Please enter Yes or No."+ bcolors.WHITE)
        turn_audio = str(input(bcolors.OKBLUE + "Do you wish to turn on audio? [Yes/No]" + bcolors.WHITE)).lower()
    starting(turn_vid, turn_audio)

def error():
    print("An error occurred")
    quit()


def openZoom(password, turn_vid, turn_audio):
    auto.press('winleft')
    auto.write('zoom')
    diff = 0
    time.sleep(2)
    while not(auto.locateOnScreen(os.path.join("imgs", "zoom_Button.png")) and (diff < 50)):
        diff += 1
        time.sleep(1)
    if (diff >= 50):
        print("Took too long to load zoom! Please check internet and try again later!")
        error()
    zoom_button = auto.locateOnScreen(os.path.join("imgs", "zoom_Button.png"))
    auto.click(zoom_button[0], zoom_button[1])
    diff = 0
    while not(auto.locateOnScreen(os.path.join("imgs", "check_button.png")) and (diff < 50)):
        diff += 1
        time.sleep(1)
    if (diff >= 50):
        print("Took too long to load zoom!")
        error()

    check_button = auto.locateOnScreen(os.path.join("imgs", "check_button.png"))
    auto.click(check_button[0], check_button[1])
    diff = 0

    while not(auto.locateOnScreen(os.path.join("imgs", "join_button.png")) and (diff < 50)):
        diff+=1
        time.sleep(1)
        if(auto.locateOnScreen(os.path.join("imgs", "join_button.png"))):
            break 
    if (diff >= 50):
        print("Took too long to load zoom!")
        error()
    join_click = auto.locateOnScreen(os.path.join("imgs","join_button.png"))
    auto.write(password[0])
    WIDTH, HEIGHT = auto.size()
    turn_vid = True if turn_vid.lower() == 'yes' else False
    turn_audio = True if turn_audio.lower() == 'yes' else False
    if auto.pixelMatchesColor(int(WIDTH*0.4), int(HEIGHT*0.55)+40, (14, 114, 235)) == turn_vid:
        auto.click(int(WIDTH*0.4), int(HEIGHT*0.55)+40)
    if auto.pixelMatchesColor(int(WIDTH*0.4), int(HEIGHT*0.55), (14, 114, 235)) == turn_audio:
        auto.click(int(WIDTH*0.4), int(HEIGHT*0.55))
    auto.click(join_click[0], join_click[1])
    if len(password) > 1:
        diff = 0
        while not(auto.locateOnScreen(os.path.join("imgs", "meeting_button.png")) and (diff < 50)):
            diff+=1
            time.sleep(1)
        if (diff >= 50):
            print("Took too long to load zoom!")
            error()

        auto.write(password[1])
        auto.press('enter')

Intro()