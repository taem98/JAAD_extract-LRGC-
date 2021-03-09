import cv2
from xml.etree.ElementTree import parse
import sys
import pickle


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
    
    xbr = int(float(box.attrib['xbr']))
    xtl = int(float(box.attrib['xtl']))
    ybr = int(float(box.attrib['ybr']))
    ytl = int(float(box.attrib['ytl']))
    c_img = img[ytl:ybr, xtl:xbr]
    
    return c_img


def move(box):
    action = box[0][4].text
    if action == 'standing':
        return 0
    elif action == 'walking':
        return 1




def direction(box):

    if int(box.attrib['pose_left']) == 1:
        return 0
    elif int(box.attrib['pose_right']) == 1:
        return 1
    elif int(box.attrib['pose_front']) == 1:
        return 2
    elif int(box.attrib['pose_back']) == 1:
        return 3


def look(box):
    looking = box[0][2].text
    if looking == 'not-looking':
        return 0
    elif looking == 'looking':
        return 1

def phone(box):
    if int(box.attrib['phone']) == 0:
        return 0
    elif int(box.attrib['phone']) == 1:
        return 1



def make_obj_list(f_num, p_num, ano_track, appearances):

    p_id = ano_track[0][0].text # id of pedestrian

    for track in appearances:
        if track.attrib['id'] == p_id:
            for box in track:
                if box.attrib['frame'] == str(f_num):
                    # add obj list
                    obj_list = [ '{0:04}'.format(p_num),   #[image_num, frame_num, person_ID, move, direction, looking, phone]
                                f_num,
                                p_id,
                                move(ano_track),
                                direction(box),
                                look(ano_track) ,
                                phone(box) ,
                                ]                    

    return obj_list


def make_obj(img, f_num, p_num, vid_name, annotations, appearances, all_person):

    for track in annotations:          # each person
        for box in track:              # each frame
            if box.attrib['frame'] == str(f_num):
                c_img = cut_img(img, f_num, box)
                cv2.imwrite('../images/{}/{}.jpg'.format(vid_name, p_num), c_img)
                
                obj_list = make_obj_list(f_num, p_num, track, appearances)
                # print(obj_list)
                all_person.append(obj_list) #TODO

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
    all_person = [] # each person has [image_num, frame_num, person_ID, move, direction, looking, phone ]
    while True: # while for one frame
        f_counter += 1
        ret, img = cap.read()

        if ret == True:            
            all_person, p_counter = make_obj(img, f_counter, p_counter, vid_name, annotations, appearances, all_person)
        
        else:
            break

    with open('../labels/{}.pickle'.format(vid_name), 'wb') as f:
        pickle.dump(all_person, f, pickle.HIGHEST_PROTOCOL)



if __name__ == "__main__":
    VID_PATH = '/media/taemi/Elements/JAAD/' # JAAD path
    VID_NAME = 'video_0001'
    start(VID_PATH, VID_NAME)
