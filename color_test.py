import ev3_dc as ev3
import struct

ev3device = ev3.EV3(protocol=ev3.USB, host='00:16:53:83:D8:4D')
ev3device.verbosity = 1

ops = b''.join((
    ev3.opInput_Device,  # operation
    ev3.READY_RAW,  # CMD
    ev3.LCX(0),  # LAYER
    ev3.PORT_2,  # NO
    ev3.LCX(29),  # TYPE (EV3-Color)
    ev3.LCX(4),  # MODE (RGB)
    ev3.LCX(3),  # VALUES
    ev3.GVX(0),  # VALUE1 (R)
    ev3.GVX(4),  # VALUE1 (G)
    ev3.GVX(8),  # VALUE1 (B)
))
reply = ev3device.send_direct_cmd(ops, global_mem=12)
print(reply)
fmt = "<%dI" % 3
values = struct.unpack(fmt, reply)
values = tuple(i//4 for i in values)
print(values)

color = color = (
    'none',
    'black',
    'blue',
    'green',
    'yellow',
    'red',
    'white',
    'brown'
)[ev3.Color(port=ev3.PORT_2, ev3_obj=ev3device).color]
print(color)
