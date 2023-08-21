# coding:utf-8
# !/usr/bin/python

# Extract images from a bag file.

# PKG = 'beginner_tutorials'
import roslib  # roslib.load_manifest(PKG)
import rosbag
import rospy
import cv2
import numpy as np
import os
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError
from matplotlib import pyplot as plt
# Reading bag filename from command line or roslaunch parameter.
# import os
import sys
from tqdm import tqdm


path= '/home/yc/Desktop/'  #bag包路径, /结尾
filename='room2'
# cameras=['camera1','camera2']

topic_names={'rgb_topics':['/camera/color/image_raw'],
             'depth_topics':['/camera/aligned_depth_to_color/image_raw'],
             'davis_event_topics':['/dvs/events'],
             'davis_rgb_topics':['/dvs/image_raw']}

cam_rgb_path=[path+filename+'/rgbd/'+'/rgb/']
cam_depth_path=[path+filename+'/rgbd/'+'/depth/']
davis_rgb_path=[path+filename+'/346/'+'/rgb/']
davis_event_path=[path+filename+'/346/'+'/event/']

# for camPath in cam_rgb_path:
#     print(camPath)
if os.path.exists(path+filename+'.bag'):
    for path_dir in cam_rgb_path:
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
    for path_dir in cam_depth_path:
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
    for path_dir in davis_rgb_path:
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
    for path_dir in davis_event_path:
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
else:
    print('bag file not exist!!')
    sys.exit()

class ImageCreator():
    def __init__(self):
        self.bridge = CvBridge()
        print("Waiting......")
        import csv
        with open(davis_event_path[0]+"events.csv", 'w') as csvfile:
            fieldnames = ['x', 'y', 'ts_s', 'ts_n', 'polarity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        with rosbag.Bag(path+filename+'.bag','r') as bag:  # 要读取的bag文件；
            for topic, msg, t in bag.read_messages():
                for i in range(len(topic_names['rgb_topics'])):
                    if topic == topic_names['rgb_topics'][i]:  # 图像的topic；
                        try:
                            #cv_image=self.bridge.compressed_imgmsg_to_cv2(msg)
                            cv_image = self.bridge.imgmsg_to_cv2(msg,'bgr8')
                            # a = np.fromstring(msg.data, dtype=np.uint8)
                            # print("/sensor/hugo1/image1/compressed \n")
                            # print(a.size)
                            # # print(a.shape)
                            # print(a[0:6])
                            # img = a.reshape(1280,720,3)
                            # cv_image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                            # cv_image = cv2.imdecode(a, 1)
                            # cv_image = self.bridge.imgmsg_to_cv2(msg,"bgr8")
                        except CvBridgeError as e:
                            print (e)
                        timestr = "%.6f" % msg.header.stamp.to_sec()
                        # %.6f表示小数点后带有6位，可根据精确度需要修改；
                        image_name = timestr + ".jpg"  # 图像命名：时间戳.png
                        cv2.imwrite(cam_rgb_path[i]+image_name , cv_image)  # 保存；
                    print("rgb done")
                
                for i in range(len(topic_names['depth_topics'])):
                    if topic == topic_names['depth_topics'][i]:  # 图像的topic；
                    # if topic == '/camera/depth/image_rect_raw':
                        try:
                            #cv_image=self.bridge.compressed_imgmsg_to_cv2(msg)
                            cv_image = self.bridge.imgmsg_to_cv2(msg,'16UC1')
                            # image = np.array(cv_image, dtype=np.uint16)
                            # image=image*1 #16UC1单位是1mm
                            
                            # NewImg = np.round(image).astype(np.uint8)#错误的！
                            image = cv2.convertScaleAbs(cv_image, alpha=(255.0/65535.0))#1代表65535/255=257mm
                            # plt.subplot(121)
                            # plt.imshow(cv_image,'rainbow')
                            # plt.subplot(122)
                            # plt.imshow(image, 'rainbow')
                            # plt.show()
                        except CvBridgeError as e:
                            print (e)
                        timestr = "%.6f" % msg.header.stamp.to_sec()# %.6f表示小数点后带有6位，可根据精确度需要修改；
                        image_name = timestr + ".png"  # 图像命名：时间戳.png
                        cv2.imwrite(cam_depth_path[i]+image_name , cv_image)  # 保存；
                    print("depth done")
                import csv
                for i in range(len(topic_names['davis_event_topics'])):
                    if topic == topic_names['davis_event_topics'][i]:
                        with open(davis_event_path[i]+"events.csv", 'a') as csvfile:
                            writer = csv.writer(csvfile)
                            for event in msg.events:
                                x_value = event.x
                                y_value = event.y
                                ts_secs_value = event.ts.secs
                                ts_nsecs_value = event.ts.nsecs
                                # ts = ts_secs_value + ts_nsecs_value*1e-9
                                polarity_value = event.polarity
                                writer.writerow([x_value, y_value, ts_secs_value, ts_nsecs_value, polarity_value])
                    print("event done")
                
                for i in range(len(topic_names['davis_rgb_topics'])):
                    if topic == topic_names['davis_rgb_topics'][i]:
                        try:
                            cv_image = self.bridge.imgmsg_to_cv2(msg,'bgr8')
                        except CvBridgeError as e:
                            print (e)
                        timestr = "%.6f" % msg.header.stamp.to_sec()# %.6f表示小数点后带有6位，可根据精确度需要修改；
                        image_name = timestr + ".jpg"  # 图像命名：时间戳.png
                        cv2.imwrite(davis_rgb_path[i]+image_name , cv_image)  # 保存；
                    print("davis_rgb done")
                    
                    
if __name__ == '__main__':
    # rospy.init_node(PKG)
    try:
        image_creator = ImageCreator()
        print("done")
    except rospy.ROSInterruptException:
        pass