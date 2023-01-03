import configparser
import os


def get_path():
    path = os.path.dirname(__file__)
    return os.path.relpath('..\\subfldr1\\testfile.txt', path)

def palo_compile():
    return
    