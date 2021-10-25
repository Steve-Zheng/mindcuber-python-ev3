import ev3_dc as ev3
import struct
import numpy as np

class RGB():
    def __init__(self,ev3_obj):
        self.ev3device = ev3_obj
    
    def read_rgb(self,white):
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
        reply = self.ev3device.send_direct_cmd(ops, global_mem=12)
        fmt = "<%dI" % 3
        values = struct.unpack(fmt, reply)
        values = np.array(tuple(i//4 for i in values))
        return tuple(255* values//np.array(white))