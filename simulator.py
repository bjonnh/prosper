# This is the emulator
# socat -d -d pty,raw,echo=0 pty,raw,echo=0

import prosper_common
from prosper_simulator import Simulator
from prospekt import ProspektBox


box = ProspektBox()
box.set_port("/dev/prospekt")
box.open()
simulator=Simulator()
simulator.set_box(box)
box.codes_false=[0x15,0x18,0x24]
box.end_codes=[0x3,0x6,0x18,0x15]
while 1==1:
    box.wait_request(answer_callback=simulator.answering_machine)
