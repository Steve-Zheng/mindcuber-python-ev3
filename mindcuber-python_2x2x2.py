# Source: https://github.com/Pedro-Beirao/mindcuber-python/blob/main/mindcuber-python.py


import ev3_dc as ev3
import time

from scanner.scan_2x2x2 import Cube
import kociemba


def wait():
    while rotate.busy:
        pass
    time.sleep(0.1)


def waitT():
    while turnn.busy:
        pass
    time.sleep(0.1)


# holds the upper layers
def hold():
    rotate.start_move_to(100, speed=25, brake=True)
    # wait()
    # rotate.start_move_to(120, speed=10, brake=True)
    # wait()

# larga as layers de cima


def release():
    rotate.start_move_to(20, speed=35, brake=True)
    wait()
    rotate.start_move_for(1, speed=5, direction=-1)
    wait()

# roda o cubo usando o braco
# "dir" = quantas vezes roda
# "release" = -1 : roda e segura
# "release" = 1 : roda e larga
# "release" = 0 : roda


def rot(dir=1, release=0):
    for i in range(dir):
        cube.flip()

    if release == 0 or release == 1:
        cube.push_arm_away()


# roda a plataform
# "dir" = 1 ou -1 : sentido ponteiros relogio ou contra relogio
# "times" = quantas vezes roda (rodar 3 vezes é igual a rodar uma vez no sentido contrario)
def turn(dir=1, times=1):

    if times == 1:
        turnn.start_move_by(-310*dir, speed=60, brake=True)
        waitT()
        turnn.start_move_by(40*dir, speed=60, brake=True)
        waitT()
    if times == 2:
        turnn.start_move_by(-580*dir, speed=60, brake=True)
        waitT()
        turnn.start_move_by(40*dir, speed=60, brake=True)
        waitT()
    if times == 3:
        turnn.start_move_by(310*dir, speed=60, brake=True)
        waitT()
        turnn.start_move_by(-40*dir, speed=60, brake=True)
        waitT()


# solve the cube
def solve():
    print("-------------------------")

    timeItTakes = time.time()

    stepCount = 1

    steps = stepstr.split()

    faceDown = "D"

    hold()

    stepIndex = 0

    for step in steps:
        print("Step: "+str(stepCount) + " of "+str(len(steps)) + " - " + step)
        stepCount += 1

        if step.endswith("'"):
            turnTimes = 3
        elif step.endswith("2"):
            turnTimes = 2
        else:
            turnTimes = 1

        try:
            if faceDown == "D":
                if step.startswith("D"):
                    turn(1, turnTimes)
                    faceDown = "D"
                elif step.startswith("U"):
                    rot(2, -1)
                    turn(1, turnTimes)
                    faceDown = "U"
                elif step.startswith("F"):
                    rot(1, -1)
                    turn(1, turnTimes)
                    faceDown = "F"
                elif step.startswith("B"):
                    rot(3, -1)
                    turn(1, turnTimes)
                    faceDown = "B"
                elif step.startswith("R"):
                    release()
                    turn(-1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(-1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold()
                    faceDown = "U"
                elif step.startswith("L"):
                    release()
                    turn(1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold()
                    faceDown = "U"

            elif faceDown == "U":
                if step.startswith("U"):
                    turn(1, turnTimes)
                    faceDown = "U"
                elif step.startswith("D"):
                    rot(2, -1)
                    turn(1, turnTimes)
                    faceDown = "D"
                elif step.startswith("F"):
                    rot(3, -1)
                    turn(1, turnTimes)
                    faceDown = "F"
                elif step.startswith("B"):
                    rot(1, -1)
                    turn(1, turnTimes)
                    faceDown = "B"
                elif step.startswith("R"):
                    release()
                    turn(-1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(-1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold()
                    faceDown = "D"
                elif step.startswith("L"):
                    release()
                    turn(1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold()
                    faceDown = "D"

            elif faceDown == "F":
                if step.startswith("F"):
                    turn(1, turnTimes)
                    faceDown = "F"
                elif step.startswith("B"):
                    rot(2, -1)
                    turn(1, turnTimes)
                    faceDown = "B"
                elif step.startswith("U"):
                    rot(1, -1)
                    turn(1, turnTimes)
                    faceDown = "U"
                elif step.startswith("D"):
                    rot(3, -1)
                    turn(1, turnTimes)
                    faceDown = "D"
                elif step.startswith("R"):
                    release()
                    turn(-1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(-1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold()
                    faceDown = "B"
                elif step.startswith("L"):
                    release()
                    turn(1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold()
                    faceDown = "B"

            elif faceDown == "B":
                if step.startswith("B"):
                    turn(1, turnTimes)
                    faceDown = "B"
                elif step.startswith("F"):
                    rot(2, -1)
                    turn(1, turnTimes)
                    faceDown = "F"
                elif step.startswith("D"):
                    rot(1, -1)
                    turn(1, turnTimes)
                    faceDown = "D"
                elif step.startswith("U"):
                    rot(3, -1)
                    turn(1, turnTimes)
                    faceDown = "U"
                elif step.startswith("R"):
                    release()
                    turn(-1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(-1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold()
                    faceDown = "F"
                elif step.startswith("L"):
                    release()
                    turn(1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold()
                    faceDown = "F"
        except:
            pass
        time.sleep(0.1)
        stepIndex += 1

    seconds = time.time()-timeItTakes
    minutes, seconds = divmod(seconds, 60)
    if str(seconds)[1] == ".":
        seconds = "0"+str(seconds)[0]
    else:
        seconds = str(seconds)[:2]
    print("Final time = " + str(minutes)[0] + ":" + str(seconds))

    release()

    # jukebox = ev3.Jukebox(ev3_obj=ev3device)
    # jukebox.song(ev3.TRIAD, volume=20).start()
    # jukebox.change_color(ev3.LED_RED_FLASH)
    # time.sleep(5)
    # jukebox.change_color(ev3.LED_GREEN)


if __name__ == "__main__":
    ev3device = ev3.EV3(protocol=ev3.USB, host='00:16:53:83:D8:4D')

    rotate = ev3.Motor(ev3.PORT_A, ev3_obj=ev3device)  # big motor (arm)
    turnn = ev3.Motor(ev3.PORT_B, ev3_obj=ev3device)  # big motor (platform)
    ultrasonic = ev3.Ultrasonic(ev3.PORT_1, ev3_obj=ev3device)

    cube = Cube(ev3device, rotate, turnn)

    while True:
        if ultrasonic.distance < 1.5:
            break
        time.sleep(0.1)

    cubestr = cube.scan()
    stepstr = kociemba.solve(cubestr)

    solve()
    # rot(1,1)

    cube.disable_brake()
