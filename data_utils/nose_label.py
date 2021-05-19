import cv2
from glob import glob

"""
鼻梁 43-46, 鼻子下沿 47-51, 鼻子外侧 78-83
43  44  45  46  47  48  49  50  51  78  79  80  81  82  83  46与49中心点  48与80中心点  50与81中心点
0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15           16          17
"""
nose_index_list = [43, 44, 45, 46, 47, 48, 49, 50, 51, 78, 79, 80, 81, 82, 83]

img_list = glob('../data/temp/celeb_ori_img/' + '*.jpg')

for img_path in img_list:
    nose_point_list = []
    img_name = (img_path.split('/')[-1]).split('.')[0]
    img = cv2.imread(img_path)

    txt_path = '../data/temp/106points/' + img_name + '.txt'
    with open(txt_path, "r") as f:
        for index, line in enumerate(f.readlines()):
            line = line.strip('\n')

            point_x = int(float(line.split(',')[0]))
            point_y = int(float(line.split(',')[1]))

            if index in nose_index_list:
                nose_point_list.append([point_x, point_y])
    if f:
        f.close()

    """
    自增点
    """
    point1_index_list = [3, 5, 7]
    point2_index_list = [6, 11, 12]
    assert len(point1_index_list) == len(point2_index_list)
    for index in range(len(point1_index_list)):
        point1, point2 = nose_point_list[point1_index_list[index]], nose_point_list[point2_index_list[index]]
        new_point_x = int(point1[0] + point2[0]) // 2
        new_point_y = int(point1[1] + point2[1]) // 2
        nose_point_list.append([new_point_x, new_point_y])

    """
    line_point_index_list = [[0, 1], [1, 2], [2, 3], [3, 6],
                             [4, 5], [5, 6], [6, 7], [7, 8],
                             [9, 11], [11, 13], [13, 4],
                             [10, 12], [12, 14], [14, 8]]
    """

    line_point_index_list = [
        [4, 16], [16, 6], [6, 17], [17, 8],
        [11, 13], [13, 4],
        [12, 14], [14, 8]]

    for line_point_index in line_point_index_list:
        point1 = (nose_point_list[line_point_index[0]][0], nose_point_list[line_point_index[0]][1])
        point2 = (nose_point_list[line_point_index[1]][0], nose_point_list[line_point_index[1]][1])
        cv2.line(img, point1, point2, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imwrite('../data/temp/nose_merge/nose_test_1617_' + img_name + '.jpg', img)
