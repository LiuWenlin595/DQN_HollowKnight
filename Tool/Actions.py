# Define the actions we may need during training
# You can define your actions here

from Tool.SendKey import PressKey, ReleaseKey
from Tool.WindowsAPI import grab_screen
import time
import cv2
import threading

# Hash code for key we may use: https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN
UP_ARROW = 0x26
DOWN_ARROW = 0x28
LEFT_ARROW = 0x25
RIGHT_ARROW = 0x27

L_SHIFT = 0xA0
A = 0x41
C = 0x43
X = 0x58
Z = 0x5A

# move actions
# 0
def Nothing():
    ReleaseKey(LEFT_ARROW)
    ReleaseKey(RIGHT_ARROW)
    pass

# Move
# 0, 向左移动
def Move_Left():
    PressKey(LEFT_ARROW)
    time.sleep(0.01)

# 1, 向右移动
def Move_Right():
    PressKey(RIGHT_ARROW)
    time.sleep(0.01)

# 2, 面朝左
def Turn_Left():
    PressKey(LEFT_ARROW)
    time.sleep(0.01)
    ReleaseKey(LEFT_ARROW)

# 3, 面朝右
def Turn_Right():
    PressKey(RIGHT_ARROW)
    time.sleep(0.01)
    ReleaseKey(RIGHT_ARROW)

# ----------------------------------------------------------------------

# other actions
# Attack
# 0, 攻击
def Attack():
    PressKey(X)
    time.sleep(0.15)
    ReleaseKey(X)
    Nothing()
    time.sleep(0.01)
# 1
# def Attack_Down():
#     PressKey(DOWN_ARROW)
#     PressKey(X)
#     time.sleep(0.05)
#     ReleaseKey(X)
#     ReleaseKey(DOWN_ARROW)
#     time.sleep(0.01)

# 1, 向上攻击
def Attack_Up():
    # print("Attack up--->")
    PressKey(UP_ARROW)
    PressKey(X)
    time.sleep(0.11)
    ReleaseKey(X)
    ReleaseKey(UP_ARROW)
    Nothing()
    time.sleep(0.01)

#JUMP
# 2, 短跳(+下劈)
def Short_Jump():
    PressKey(C)
    PressKey(DOWN_ARROW)
    PressKey(X)
    time.sleep(0.2) 
    ReleaseKey(X)
    ReleaseKey(DOWN_ARROW)
    ReleaseKey(C)
    Nothing()

# 3, 长跳
def Mid_Jump():
    PressKey(C)
    time.sleep(0.2)
    PressKey(X)
    time.sleep(0.2)
    ReleaseKey(X)
    ReleaseKey(C)
    Nothing()

# Skill
# 4
# def Skill():
#     PressKey(Z)
#     PressKey(X)
#     time.sleep(0.1)
#     ReleaseKey(Z)
#     ReleaseKey(X)
#     time.sleep(0.01)

# 4, 黑吼
def Skill_Up():
    PressKey(UP_ARROW)
    PressKey(Z)
    PressKey(X)
    time.sleep(0.15)
    ReleaseKey(UP_ARROW)
    ReleaseKey(Z)
    ReleaseKey(X)
    Nothing()
    time.sleep(0.15)

# 5, 下砸
def Skill_Down():
    PressKey(DOWN_ARROW)
    PressKey(Z)
    PressKey(X)
    time.sleep(0.2)
    ReleaseKey(X)
    ReleaseKey(DOWN_ARROW)
    ReleaseKey(Z)
    Nothing()
    time.sleep(0.3)

# Rush
# 6, 冲刺
def Rush():
    PressKey(L_SHIFT)
    time.sleep(0.1)
    ReleaseKey(L_SHIFT)
    Nothing()
    PressKey(X)
    time.sleep(0.03)
    ReleaseKey(X)

# Cure, 治疗, 目前没有写进action
def Cure():
    PressKey(A)
    time.sleep(1.4)
    ReleaseKey(A)
    time.sleep(0.1)


# Restart function
# it restart a new game
# it is not in actions space
def Look_up():
    PressKey(UP_ARROW)
    time.sleep(0.1)
    ReleaseKey(UP_ARROW)

# 负责重开游戏的脚本, 根据下箭头调整级别
def restart():
    station_size = (230, 230, 1670, 930)
    print("hunky1")
    while True:
        station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(1000,500))
        if station[187][300][0] != 0: 
            time.sleep(1)
        else:
            break
    print("hunky2")
    time.sleep(1)
    Look_up()
    time.sleep(1.5)
    Look_up()
    time.sleep(1)
    print("hunky3")
    PressKey(C)
    time.sleep(0.1)
    ReleaseKey(C)
    # while True:
    #     station = cv2.resize(cv2.cvtColor(grab_screen(station_size), cv2.COLOR_RGBA2RGB),(1000,500))
    #     if station[187][612][0] > 200: 
    #         # PressKey(DOWN_ARROW)
    #         # time.sleep(0.1)
    #         # ReleaseKey(DOWN_ARROW)
    #         PressKey(C)
    #         time.sleep(0.1)
    #         ReleaseKey(C)
    #         break
    #     else:
    #         Look_up()
    #         time.sleep(0.2)
    print("hunky4")

# List for action functions
# 定义动作空间, 记得更改ACTION_DIM
Actions = [Attack, Attack_Up,
           Short_Jump, Mid_Jump, Skill_Up, 
           Skill_Down, Rush, Cure]
Directions = [Move_Left, Move_Right, Turn_Left, Turn_Right]
# Run the action
def take_action(action):
    Actions[action]()

def take_direction(direc):
    Directions[direc]()



class TackAction(threading.Thread):
    def __init__(self, threadID, name, direction, action):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.direction = direction
        self.action = action
        
    def run(self):
        take_direction(self.direction)
        take_action(self.action)