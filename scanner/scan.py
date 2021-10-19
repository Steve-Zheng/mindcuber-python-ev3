# redit: https://github.com/cavenel/ev3dev_examples/blob/master/python/pyev3/rubiks.py
# Modified to use ev3_dc

import ev3_dc as ev3
from time import sleep


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
        self.corner_to_edge_diff = 60

        self.init_motors()

        self.state = ['U', 'D', 'F', 'L', 'B', 'R']

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
        self.rotate.start_move_to(360*self.rotate_ratio, speed=50, brake=True)
        self.wait_rotate()
        self.rotate.position = 0  # reset

        self.flipper.start_move(direction=-1, speed=30)
        self.sensor_arm.start_move(direction=1, speed=30)
        sleep(3)

        self.flipper.stop(brake=True)
        self.flipper.position = 0  # reset

        self.sensor_arm.stop(brake=True)
        self.sensor_arm.position = 0  # reset

        print("Motors initialized")

    def scan(self):
        self.colors = {}
        self.k = 0
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

    def flip(self):
        current_position = self.flipper.position
        if (current_position <= self.hold_cube_pos-10 or current_position >= self.hold_cube_pos+10):
            self.flipper.start_move_to(self.hold_cube_pos, speed=30)
            self.wait_flipper()

        self.flipper.start_move_to(180, speed=30)
        self.wait_flipper()

        self.flipper.start_move_to(self.hold_cube_pos, speed=50)
        self.wait_flipper()

        transformation = [2, 4, 1, 3, 0, 5]
        self.apply_transformation(transformation)

    def rotate_cube(self, direction, nb):
        if self.flipper.position > 35:
            self.push_arm_away()

        final_dest = 135 * \
            round((self.rotate.position + 270 * direction * nb) / 135.0)

        self.rotate.start_move_to(
            final_dest, speed=self.rotate_speed, ramp_up=0, ramp_down=300, brake=True)
        self.wait_rotate()
        if nb >= 1:
            for i in range(nb):
                if direction > 0:
                    transformation = [0, 1, 5, 2, 3, 4]
                else:
                    transformation = [0, 1, 3, 4, 5, 2]
                self.apply_transformation(transformation)

    def scan_face(self, index):
        print("Scanning face ", index)

        if self.flipper.position > 35:
            self.push_arm_away()

        self.put_arm_middle()

        self.colors[int(self.scan_order[self.k])] = None  # To be implemented

        self.k += 1
        i = 0
        self.put_arm_corner(i)
        i += 1

        self.wait_rotate()
        self.rotate.position = 0
        self.rotate.start_move_to(360*self.rotate_ratio, speed=20, brake=True)

        while self.rotate.busy:
            current_position = self.rotate.position
            if current_position >= (i*135)-5:
                current_color = None  # To be implemented
                self.colors[int(self.scan_order[self.k])] = current_color
                print("Face: ", index, "current position: ",
                      i, "current color: ", current_color)
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
        self.flipper.start_move_to(0, speed=30, brake=True)
        self.wait_flipper()

    def put_arm_middle(self):
        self.sensor_arm.start_move_to(-750, speed=30, brake=True)
        self.wait_sensor_arm()

    def put_arm_corner(self, i):
        if i == 2:
            diff = self.corner_to_edge_diff
        elif i == 6:
            diff = self.corner_to_edge_diff*-1
        else:
            diff = 0
        # diff=0
        self.sensor_arm.start_move_to(-580-diff, speed=50, brake=True)
        self.wait_sensor_arm()

    def remove_arm(self):
        self.sensor_arm.start_move_to(0, speed=50, brake=True)
        self.wait_sensor_arm()

    def remove_arm_halfway(self):
        self.sensor_arm.start_move_to(-400, speed=50, brake=True)
        self.wait_sensor_arm()

    def put_arm_edge(self, i):
        self.sensor_arm.start_move_to(-650, speed=50, brake=True)
        self.wait_sensor_arm()


if(__name__ == "__main__"):
    cube = Cube()
    # cube.put_arm_edge(2)
    cube.scan()
