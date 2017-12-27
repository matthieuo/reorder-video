# reorder-video

This program try to reorder a video file in which the frames are mixed up.
To find the correct order, the program assumes that the distance (euclidean) between two consecutive frames is small. This strategy is not adapted to all video.

This program also find outliers (if some irrelevant frames have been added) and remove them. Outliers are found using histograms and correlation distance.

## Note

This program cannot find the direction of the video. Therefore, it outputs two videos, the first one is ordered to a particular direction, the second one to the opposite direction.

## Usage

`python reorder.py -vi corrupted_video.mp4 -vo1 outfile_order1.mp4 -vo2 outfile_order2.mp4`

In which `-vi` is the video to reorder, `-vo1` the reordered video in the first direction, `-vo2` the reordered video in the second direction.




