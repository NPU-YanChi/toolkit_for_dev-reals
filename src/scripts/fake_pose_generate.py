import os

datapath = "/DATA/DEV-Reals/"
squencename = "test"
folder_path = os.path.join(datapath, squencename, "rgbd/depth")
pose_path = os.path.join(datapath, squencename, "pose", "pose.txt")

# folder_path = "/home/pjlab/DATA/DEV-Reals/room2/rgbd/depth"
files = os.listdir(folder_path)
num_files = len(files)
print(num_files)

with open(pose_path, "w") as f:
    f.write("# TUM format ground truth pose, timestamp x y z q_x q_y q_z q_w\n")
    for i in range(num_files):
        f.write(f"{i:04d} 0.0 0.0 0.0 0.493839 -0.488670 -0.506032 0.511133\n")