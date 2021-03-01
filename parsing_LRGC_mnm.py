import cv2
from xml.etree.ElementTree import parse
import sys


def parsing_annotation(path, name):
    '''
    - xtl : x top
    - ytl : y top
    - xbr : x lower
    - ybr : y lower

    - look : looking / non-looking
    - action : standing / warking
    '''
    tree = parse(path+name)
    root = tree.getroot()

    annotations = root.findall("track") # read pedestrian , ped
    new_annotations = []
    
    # removed ped

    for x in annotations:
        if x.attrib['label'] == 'pedestrian':
            new_annotations.append(x)
            

    # for track in new_annotations:
    #     for box in track:
            # print(box[0].text) # 0_1_2b
            # print(box.attrib)
    #         ## result ex {'frame': '69', 'keyframe': '1', 'occluded': '1', 'outside': '0', 
    #                   'xbr': '1919.0', 'xtl': '1894.0', 'ybr': '1079.0', 'ytl': '529.0'}
    return new_annotations
   

def parsing_appearance(path, name):
    '''
    - direction : left / right / front / back
    '''

    print(path+name)
    tree = parse(path+name)
    root = tree.getroot()

    appearances = root.findall("track") # read pedestrian , ped
    new_appearnaces = []

    # removed ped
    for x in appearances:
        if x.attrib['label'] == 'pedestrian':
            new_appearnaces.append(x)

    # for track in new_appearnaces:
    #     for box in track:
    #         print(box.attrib)
    #         ## result ex {'baby': '0', 'backpack': '0', 'bag_elbow': '0', 'bag_hand': '0', 
    #         # 'bag_left_side': '0', 'bag_right_side': '0', 'bag_shoulder': '0',
    #         #  'bicycle_motorcycle': '0', 'cap': '0', 'clothes_below_knee': '0',
    #         #  'clothes_lower_dark': '1', 'clothes_lower_light': '0', 'clothes_upper_dark': '0',
    #         #  'clothes_upper_light': '1', 'frame': '69', 'hood': '0', 'object': '0',
    #         #  'phone': '0', 'pose_back': '0', 'pose_front': '1', 'pose_left': '0', 'pose_right': '0',
    #         #  'stroller_cart': '0', 'sunglasses': '0', 'umbrella': '0'}

    return new_appearnaces

def cut_img(img, f_num, box):
    xbr = box.attrib['xbr']
    xtl = box.attrib['xtl']
    ybr = box.attrib['ybr']
    ytl = box.attrib['ytl']

    c_img = img[xtl:xbr, ytl:ybr]
    
    return c_img

def make_obj(img, f_num, p_num, annotations, appearances, all_person):

    for annotation in annotations:          # each person
        for box in annotation:              # each frame
            if box.attrib['frame'] == str(f_num):
                cut_img = cut_img(img, f_num, box)
                p_num += 1
                break
            # img and other things write
            



    return all_person, p_num

def start(vid_path, vid_name):
    '''
    [lrgc] - str

    [mnm] - str
    '''
    cap = cv2.VideoCapture(vid_path+'JAAD_clips/'+vid_name+'.mp4')
    
    annotations = parsing_annotation(vid_path+"annotations/", vid_name+'.xml') 
    
    # checking the existence of a person
    if not len(annotations):
        print("'{}' doesn't have person".format(vid_name))
        sys.exit()

    appearances = parsing_appearance(vid_path+'annotations_appearance/', vid_name+"_appearance.xml")

    f_counter = -1    # frame start 0 
    p_counter = 0     # person nuber (img name)
    all_person = [] # each person has [image_num, frame_num, person_ID, move, direction, looking ]
    while True: # while for one frame
        f_counter += 1
        ret, img = cap.read()

        if ret == False:
            continue
        
        all_person, p_counter = make_obj(img, f_counter, p_counter, annotations, appearances, all_person)

        # if cv2.waitKey(1)&0xFF == 27:
        #     break
        break

    cap.release()
    # cv2.destroyAllWindows()




if __name__ == "__main__":
    VID_PATH = '/media/taemi/Elements/JAAD/' # JAAD path
    VID_NAME = 'video_0001'
    start(VID_PATH, VID_NAME)
