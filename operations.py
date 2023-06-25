from dwis import *


def close_BOP():
    BOP_Opening(0)
    client_write.disconnect()

def open_BOP():
    BOP_Opening(1)

def open_MPD(percent):
    MPD_Opening(percent / 100)

def set_flow_in(lpm):
    Flow_In(lpm / 60000)

def stop_pump():
    Flow_In(0)

def set_rpm(rpm):
    RPM_set(rpm/60)

def stop_rotation():
    set_rpm(0)

def set_pipe_velocity(mps):
    String_velocity(mps)

def stop_drilling():
    set_pipe_velocity(0)
    set_rpm(0)
    stop_pump()

def start_drilling():
    set_rpm(120)
    set_pipe_velocity(-0.4)
    set_flow_in(1000)



stop_drilling()
close_BOP()
