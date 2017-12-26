import argparse
import numpy as np
import cv2
from scipy.spatial import distance


def write_video_full_resolution(video_file_in, video_file_out, frames, l_coresp):
    """Write a video reordered and in its original resolution

    Args:
      video_file_in: original file
      video_file_out: reorderd file
      frames: frames order
      l_coresp: links between the initial video and the video without the outliers
    """
    cap = cv2.VideoCapture(video_file_in)

    info = {}
    info['fps'] = cap.get(cv2.CAP_PROP_FPS)
    info['codec'] = cap.get(cv2.CAP_PROP_FOURCC)
    info['frame'] = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    print(info)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_file_out,fourcc, info['fps'], info['frame'])

    for el in frames:
        idx = 0
        while 1:
            ret, frame_f = cap.read()
            if ret:
                if idx == l_coresp[el]:
                    out.write(frame_f)
                    print("rr")
            else:
                break
            idx+=1
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

def import_video_for_analysis(video_file):
    """Read the original video file, outputs two lists
    
    Args:
      video_file: the file to read

    Returns:
      frame_list: the frame in low resolution (64x64)
      histo_list: one histogram per frames
    """
    
    cap = cv2.VideoCapture(video_file)
    frame_list_dim = []

    while 1:
        ret, frame_f = cap.read()
        if ret:
            frame_f = cv2.resize(frame_f, (64,64))
            frame_list_dim.append(frame_f)
        else:
            break

    frame_list = [x.flatten() for x in frame_list_dim]
    histo_list = [cv2.calcHist([x], [0, 1, 2], None, [8, 8, 8],
                               [0, 256, 0, 256, 0, 256]).flatten()
                  for x in frame_list_dim]

    return frame_list, histo_list



def remove_outliers(histo_list, frame_list):
    """remove outilers from frame_list

    Args:
      histo_list: the histograms computed for each frame
      frame_list: the frames, the function modifies this argument

    Returns
      l_coresp: maintain the corespondance between the initial video and the video without outiliers
   """
    
    histo_med = np.median(histo_list, axis=0)
    dist_to_med = [cv2.compareHist(histo_med,x,
                                   cv2.HISTCMP_CORREL) for x in histo_list]

    excl_list = [idx for idx, _ in enumerate(histo_list) if dist_to_med[idx] < 0.85]

    #0.85 is an empirical value

    #remove outilers from the list
    l_coresp = [x for x in range(len(frame_list))]

    for i in sorted(excl_list, reverse=True):
        del frame_list[i]
        del l_coresp[i]
        
    return l_coresp


def reord_frames(frame_list):
    """returns a list of frame in correct order"""
    
    Y = distance.cdist(frame_list, frame_list, 'euclidean')

    start_img = 0 #start at 0 arbitraly

    #algorithm
    #search a frames order based on distance between frame. We assume if two frames has a small distance, they should be consecutive
    #search the largest distance between two consecutive frames (to find the begining of the video. We iter 10 times to find this value
    
    for _ in range(10):
        cur_im = start_img
        seen_im = [cur_im]
        last_img = len(frame_list)-len(seen_im)

        for _ in range(last_img):
            arg_l = np.argsort(Y[cur_im])
            idx = 0
            while(cur_im in seen_im):
                cur_im = arg_l[idx]
                idx += 1
            seen_im.append(cur_im)


        #search the largest distance between consecutive frames

        im1 = seen_im[-1]
        maxi = 0
        im_max = 0

        for im2 in seen_im:
            if Y[im1][im2] > maxi:
                im_max = im1
                maxi = Y[im1][im2]
            im1 = im2

        start_img = im_max

    return seen_im

def main():
    parser = argparse.ArgumentParser(description='Reorder video')
    parser.add_argument("-vi", "--video_in", required=True,
                        help="Input video file")
    parser.add_argument("-vo1", "--video_out_order_1", required=True,
                        help="Output video file 1")
    parser.add_argument("-vo2", "--video_out_order_2", required=True,
                        help="Output video file 2")
    
    args = parser.parse_args()

    frame_list, histo_list = import_video_for_analysis(args.video_in)
    l_coresp = remove_outliers(histo_list, frame_list)
    frame_ordo = reord_frames(frame_list)

    write_video_full_resolution(args.video_in,
                                args.video_out_order_1,
                                frame_ordo,
                                l_coresp)

    write_video_full_resolution(args.video_in,
                                args.video_out_order_2,
                                frame_ordo[::-1],
                                l_coresp)

if __name__ == "__main__":
    main()
