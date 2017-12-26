# reorder-video

This program try to reorder a video file in which the frames was mixed up.
The program assumes that the distance (euclidean) between two consecutive frames is small. 

## Note

The program cannot find the direction of the video. Therfore, it outputs two videos, the first is ordered to one direction, the second to the oposite direction

## Usage

`python reorder.py -vi corrupted_video.mp4 -vo1 outfile_order1.mp4 -vo2 outfile_order2.mp4`

In which `-vi` is the video to reorder, `-vo1` the reordered video in the first direction, `-vo2` the reorderer video in the second direction.




