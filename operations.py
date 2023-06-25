import time

from dwis import *


def close_BOP():
    BOP_Opening(0)

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
    stop_rotation()
    stop_pump()
    set_pipe_velocity(+0.1)
    time.sleep(2)
    set_pipe_velocity(0)


def start_drilling():
    set_rpm(120)
    set_pipe_velocity(-0.4)
    set_flow_in(1800)

def save_current_drilling_parameters():
    rpm = eval(RPM_Surf[1])
    flowRate = eval(FlowRateIn[1])
    MPD_value = eval(MPD_ChokeOpening[1])

    return rpm, flowRate, MPD_value

def resume_drilling(rpm, flowRate, pipe_velocity, MPD_value):
    set_rpm(rpm)
    set_pipe_velocity(pipe_velocity)
    set_flow_in(flowRate)
    open_MPD(MPD_value)

def control_kick():
    revpmin, fr, MPD_value = save_current_drilling_parameters()
    print("Kick Detected")
    stop_drilling()
    print("Drilling Stopped")
    close_BOP()
    print("BOP Closed")
    time.sleep(3)
    open_MPD((MPD_value - 0) / 2)
    print("MPD Choke opening decreased")
    time.sleep(3)
    open_BOP()
    resume_drilling(revpmin, fr + 300, -0.4, (MPD_value-0) / 2)
    print("Drilling Resumed")


start_drilling()
set_flow_in(500)





