import rospy
import time
from utils import open_desktop, open_rvizweb, run_command, create_marker, publish_marker_array, TracyDemo
from std_msgs.msg import ColorRGBA
import random

def load():
    open_desktop()
    run_command('./canister_mesh_loader.py')