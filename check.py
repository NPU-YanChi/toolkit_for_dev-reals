import os



def check_image_correspondence(folder1_path, folder2_path):
    cor_flag = True
    folder1_files = os.listdir(folder1_path)
    folder2_files = os.listdir(folder2_path)

    for file1 in folder1_files:
        file1_path = os.path.join(folder1_path, file1)
        if os.path.isfile(file1_path) and file1.lower().endswith(('.jpg', '.jpeg', '.png')):
            corresponding_file = find_corresponding_file(file1, folder2_files)
            # print(corresponding_file)
            if not corresponding_file:
                cor_flag = False
                print(file1_path)
                
    if cor_flag is False:
        return False
    
    return True

def find_corresponding_file(file, file_list):
    for f in file_list:
        if f.lower()[:-4] == file.lower()[:-4]:
            return f
    
    # print(f.lower())
    return None

# 检查两个文件夹中的图片是否具有对应关系
folder1_path = "/home/yc/Desktop/room2/rgbd/depth"
folder2_path = "/home/yc/Desktop/room2/rgbd/rgb"
correspondence1 = check_image_correspondence(folder1_path, folder2_path)
correspondence2= check_image_correspondence(folder2_path, folder1_path)

if correspondence1 and correspondence2:
    print("两个文件夹中的图片具有对应关系")
else:
    print("两个文件夹中的图片不具有对应关系")