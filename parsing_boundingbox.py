import cv2
from xml.etree.ElementTree import parse
import sys
import os 

def parsing_BB(path, name):
    print(path+name)
    tree = parse(path+name+'.xml')
    root = tree.getroot()

    appearances = root.findall("track") # read pedestrian , ped
    new_appearnaces = []

    for x in appearances:
        if x.attrib['label'] == 'pedestrian' or x.attrib['label'] == 'ped':
            new_appearnaces.append(x)

    # for track in new_appearnaces:
    #     print(track.attrib['label']) # "pedestrian /  ped"
    #     for box in track:
    #         print(box.attrib) 
    #         '''
    #         {'frame': '383', 'keyframe': '1', 'occluded': '1', 'outside': '0',
    #          'xbr': '196.0', 'xtl': '148.0', 'ybr': '796.0', 'ytl': '684.0'}
    #         '''
    #         break

    return new_appearnaces


def make_objs(new_appearances):
    save_objs = {}

    for track in new_appearances:
        label = track.attrib['label']
        for box in track:
            frame = box.attrib['frame']
            xbr = box.attrib['xbr']
            xtl = box.attrib['xtl']
            ybr = box.attrib['ybr']
            ytl = box.attrib['ytl']
            obj = [label, xtl, ytl, xbr, ybr]

            if frame not in save_objs:
                save_objs[frame] = []

            save_objs[frame].append(obj)
    
    return save_objs


def save(save_objs, video_name):
    save_path = '../input/ground-truth/'
    
    for frame in save_objs:
        save_name = video_name + '_' + frame + '.txt'
        
        with open(save_path + save_name, 'w') as f:
            for obj in save_objs[frame]:
                line = ""
                for i in obj:
                    line += str(i) + " "
                f.write(line[:-1]+'\n')
                
        


if __name__=="__main__":
    path = '/media/taemi/Elements/JAAD/annotations/'
    # video_name = 'video_0001'
    names  = os.listdir(path)
    for name in names:
        new_appearances = parsing_BB(path, name[:-4])
        save_objs = make_objs(new_appearances)
        save(save_objs, name[:-4])

