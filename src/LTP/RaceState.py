from LTP.TrackMap import TrackMap
import rospy
from geometry_msgs.msg import PoseArray, Pose, Point
from geometry_msgs.msg import PoseStamped

# TODO: Right now there is no way to know when the Race is finished
#       and also to know when we complete a lap.
class RaceState():
    def __init__(self, subscribe=False):
        self.track_map = TrackMap()
        self.track_map_updated = False
        self.finished = False # Is the race over?
        self.current_lap = 1

        # Subscribe to the left and right cones
        self.is_left_cones_updated = False
        self.is_right_cones_updated = False
        self.left_cones = []
        self.right_cones = []
        self.car_position = (0,0)
        rospy.Subscriber("/cone_right", PoseArray, self.update_right_cones)
        rospy.Subscriber("/cone_left", PoseArray, self.update_left_cones)
        rospy.Subscriber("/pose_stamped", PoseStamped, self.update_car_position)

    def is_last_lap(self):
        return True # TODO: Right now there is no way to know the current lap (KB)

    def update_left_cones(self, msg):
        poses = msg.poses
        self.left_cones = []
        for pose in poses:
            point: Point = pose.position
            self.left_cones.append((point.x, point.y))
        self.is_left_cones_updated = True
        self.try_update_track_map()

    def update_right_cones(self, msg):
        poses = msg.poses
        self.right_cones = []
        for pose in poses:
            point: Point = pose.position
            self.right_cones.append((point.x, point.y))
        self.is_right_cones_updated = True
        self.try_update_track_map()
    
    def update_car_position(self, msg):
        point = msg.pose.position
        self.car_position = (point.x, point.y)
    
    def get_car_position(self):
        return self.car_position

    def try_update_track_map(self):
        if self.is_left_cones_updated and self.is_right_cones_updated:
            self.track_map = TrackMap(self.left_cones, self.right_cones)
            self.track_map_updated = True
            self.is_left_cones_updated = False
            self.is_right_cones_updated = False

    def set_finished_status(self, finished):
        self.finished = finished
        
    def get_finished_status(self):
        return self.finished

    def get_track_map(self):
        return self.track_map

    def is_track_map_complete(self):
        return False

    def is_track_map_new(self):
        return self.track_map_updated