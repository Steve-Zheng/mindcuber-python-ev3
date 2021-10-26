# credit: https://github.com/cavenel/ev3dev_examples/blob/master/python/pyev3/rubiks.py
# Modified to use ev3_dc

import ev3_dc as ev3
from time import sleep
from read_rgb import RGB
import json

class ScanError(Exception):
    pass


class Cube():
    def __init__(self):
        ev3device = ev3.EV3(protocol=ev3.USB, host='00:16:53:83:D8:4D')

        self.flipper = ev3.Motor(ev3.PORT_A, ev3_obj=ev3device)
        self.rotate = ev3.Motor(ev3.PORT_B, ev3_obj=ev3device)
        self.sensor_arm = ev3.Motor(ev3.PORT_C, ev3_obj=ev3device)

        self.rotate_ratio = 3

        self.color_sensor = ev3.Color(ev3.PORT_2, ev3_obj=ev3device)
        self.distance_sensor = ev3.Ultrasonic(ev3.PORT_1, ev3_obj=ev3device)

        self.rgb = RGB(ev3device)
        self.scan_order = [
            5, 9, 6, 3, 2, 1, 4, 7, 8,
            23, 27, 24, 21, 20, 19, 22, 25, 26,
            50, 54, 51, 48, 47, 46, 49, 52, 53,
            14, 10, 13, 16, 17, 18, 15, 12, 11,
            41, 43, 44, 45, 42, 39, 38, 37, 40,
            32, 34, 35, 36, 33, 30, 29, 28, 31]

        self.cube = {}
        self.rotate_speed = 40
        self.hold_cube_pos = 85
        self.corner_to_edge_diff = 10

        self.init_motors()

        self.state = ['U', 'D', 'F', 'L', 'B', 'R']

        self.white = []

        self.colors = {}
        self.k = 0

    def apply_transformation(self, transformation):
        self.state = [self.state[t] for t in transformation]

    def wait_rotate(self):
        while self.rotate.busy:
            pass
        sleep(0.1)

    def wait_flipper(self):
        while self.flipper.busy:
            pass
        sleep(0.1)

    def wait_sensor_arm(self):
        while self.sensor_arm.busy:
            pass
        sleep(0.1)

    def init_motors(self):
        print("Initializing motors")
        self.rotate.position = 0  # reset

        self.flipper.start_move(direction=-1, speed=30)
        self.sensor_arm.start_move(direction=1, speed=30)
        sleep(2)

        self.flipper.stop(brake=True)
        self.flipper.position = 0  # reset

        self.sensor_arm.stop(brake=True)
        self.sensor_arm.position = 0  # reset

        print("Motors initialized")

    def calibrate_rgb(self):
        self.put_arm_edge(8)
        self.white = self.rgb.read_rgb(calibrate=True)
        print("White: ", self.white)

    def scan(self):
        self.calibrate_rgb()

        self.scan_face(1)

        self.flip()
        self.scan_face(2)

        self.flip()
        self.scan_face(3)

        self.rotate_cube(-1, 1)
        self.flip()
        self.scan_face(4)

        self.rotate_cube(1, 1)
        self.flip()
        self.scan_face(5)

        self.flip()
        self.scan_face(6)

        self.rotate_cube(-1,1)
        self.flip()
        self.rotate_cube(1,2)

    def flip(self):
        current_position = self.flipper.position
        if (current_position <= self.hold_cube_pos-10 or current_position >= self.hold_cube_pos+10):
            self.flipper.start_move_to(self.hold_cube_pos, speed=30)
            self.wait_flipper()

        self.flipper.start_move_to(180, speed=30)
        self.wait_flipper()

        self.flipper.start_move_to(self.hold_cube_pos, speed=50, brake=True)
        self.wait_flipper()

        transformation = [2, 4, 1, 3, 0, 5]
        self.apply_transformation(transformation)

    def rotate_cube(self, direction, nb):
        if self.flipper.position > 35:
            self.push_arm_away()

        final_dest = 135 * \
            round((self.rotate.position + 270 * direction * nb) / 135.0)

        self.rotate.start_move_to(
            final_dest, speed=self.rotate_speed, brake=True)
        self.wait_rotate()
        if nb >= 1:
            for i in range(nb):
                if direction > 0:
                    transformation = [0, 1, 5, 2, 3, 4]
                else:
                    transformation = [0, 1, 3, 4, 5, 2]
                self.apply_transformation(transformation)

    def scan_face(self, index):
        print("Scanning face", index)

        if self.flipper.position > 35:
            self.push_arm_away()

        self.put_arm_middle()

        self.colors[str(self.scan_order[self.k])
                    ] = self.rgb.read_rgb(self.white)
        print("Face:", index, "current position: 0", "current color:",
              self.colors[str(self.scan_order[self.k])])

        self.k += 1
        i = 0
        self.put_arm_corner(0)
        i += 1

        self.wait_rotate()
        self.rotate.position = 0
        self.rotate.start_move_to(360*self.rotate_ratio, speed=25, brake=True)

        while self.rotate.busy:
            current_position = self.rotate.position
            if current_position >= (i*135)-5:
                sleep(0.1)
                current_color = self.rgb.read_rgb(self.white)
                self.colors[str(self.scan_order[self.k])] = current_color
                print("Face:", index, "current position:",
                      i, "current color:", current_color)
                i += 1
                self.k += 1

                if i == 9:
                    if index == 6:
                        self.remove_arm()
                    else:
                        self.remove_arm_halfway()
                elif i % 2:
                    self.put_arm_corner(i)
                else:
                    self.put_arm_edge(i)
        if i < 9:
            raise ScanError("i is %d..should be 9" % i)

        self.wait_rotate()
        self.rotate.start_move_to(360*self.rotate_ratio, speed=30, brake=True)
        self.rotate.position = 0

    def push_arm_away(self):
        self.flipper.start_move(direction=-1, speed=30)
        sleep(1)

        self.flipper.stop(brake=True)
        self.flipper.position = 0

    def put_arm_middle(self):
        self.sensor_arm.start_move_to(-750, speed=40, brake=True)
        self.wait_sensor_arm()

    def put_arm_corner(self, i):
        # if i == 3 or i == 5 or i == 7:
        #     diff = self.corner_to_edge_diff
        # elif i == 7:
        #     diff = self.corner_to_edge_diff
        # else:
        #     diff = 0
        if i==1:
            self.sensor_arm.start_move_to(-600, speed=30, brake=True)
        elif i==3:
            self.sensor_arm.start_move_to(-630, speed=30, brake=True)
        elif i==5:
            self.sensor_arm.start_move_to(-600, speed=30, brake=True)
        else:
            self.sensor_arm.start_move_to(-590, speed=30, brake=True)
        self.wait_sensor_arm()

    def remove_arm(self):
        self.sensor_arm.start_move(direction=1, speed=40)
        sleep(2)
        self.sensor_arm.stop(brake=True)
        self.sensor_arm.position = 0

    def remove_arm_halfway(self):
        self.sensor_arm.start_move_to(-400, speed=50, brake=True)
        self.wait_sensor_arm()

    def put_arm_edge(self, i):
        if i == 2:
            self.sensor_arm.start_move_to(-660, speed=40, brake=True)
        elif i == 4:
            self.sensor_arm.start_move_to(-660, speed=40, brake=True)
        elif i == 6:
            self.sensor_arm.start_move_to(-640, speed=40, brake=True)
        elif i == 8:
            self.sensor_arm.start_move_to(-630, speed=40, brake=True)
        self.wait_sensor_arm()

    def disable_brake(self):
        self.rotate.stop(brake=False)
        self.flipper.stop(brake=False)
        self.sensor_arm.stop(brake=False)


if(__name__ == "__main__"):
    cube = Cube()
    # cube.calibrate_rgb()
    # cube.scan_face(1)

    cube.scan()
    #print(cube.colors)
    colors=str(cube.colors)
    colors=colors.replace("'",'"')
    print(colors)
    with open("output.json","w") as output_file:
        output_file.write(colors)
    # cube.flip()
    # cube.push_arm_away()

    # cube.rotate.start_move_to(270*cube.rotate_ratio, speed=25, brake=True)
    # cube.wait_rotate()
    # cube.put_arm_edge(8)

    # cube.rotate.start_move_to(7*135, speed=25, brake=True)
    # cube.wait_rotate()
    # cube.put_arm_corner(7)
    # input()
    # cube.rotate.start_move_to(0, speed=50, brake=True)
    # cube.wait_rotate()

    cube.disable_brake()
