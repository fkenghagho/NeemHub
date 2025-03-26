from neem import *
from utils import open_desktop, open_rvizweb, run_command, create_marker, publish_marker_array, TracyDemo
import subprocess


def start():
    open_desktop()
    
def load():
    run_command('roslaunch tracebot_description launch_tracebot_rviz.launch simulation:=true')
    
def play():
    player_proc = subprocess.Popen(['rosbag', 'play', '-r', '5', '/home/jovyan/workspace/ros/src/Action_XNCWVJEL.bag'])