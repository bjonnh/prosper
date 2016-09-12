from pump import PumpBox

box = PumpBox()
box.set_port("/dev/pump")
box.open()

def callbacker(data):
    print("Pump: "+str(data[0:2]))
    if (data[0:2]==[ord("F"),ord("?")]):
        box.write_request("F01.000")
    else:
        box.write_request("OK")

while 1==1:
    box.wait_request(answer_callback=callbacker)
