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

def stop_rotation():


def stop_drilling():



open_BOP()
