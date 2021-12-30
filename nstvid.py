from modules.FrameExtractor import FrameExtractor
from modules.NeuralStyleTransferHandler import NeuralStyleTransferHandler
from modules.ImageResizer import ImageResizer
from modules.FrameCombiner import FrameCombiner

import logging
import os

logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d:%H:%M:%S', format='%(asctime)s | %(levelname)s | %(name)s | LINE %(lineno)d: %(message)s')
log = logging.getLogger(__name__)
log.debug('Logging initialized')


input_file_path = "testvid.mp4" #@param {type:"string"}
filter_path = "filter/67.jpg" #@param {type:"string"}
output_max_size = 512 #@param {type:"number"}
resize_factor = 2 #@param {type:"number"}
use_superres = True #@param {type:"boolean"}


def main():

    # extract frames in folder
    extracted_frames_path, input_video_filename = FrameExtractor(input_file_path).extract_frames()

    # nst all frames in folder
    styled_frames_path = NeuralStyleTransferHandler(extracted_frames_path, input_video_filename, output_max_size).stylize_batch('stylize_by_filter', filter_path)

    # optional: resize all frames in folder
    if resize_factor is not 1:
        if use_superres is True:
            resized_frames_path = ImageResizer(styled_frames_path, input_video_filename).resize_superres(resize_factor)
            styled_frames_path = resized_frames_path
        else:
            resized_frames_path = ImageResizer(styled_frames_path, input_video_filename).resize(resize_factor)
            styled_frames_path = resized_frames_path


    # combine all frames in video file
    output_video_path = FrameCombiner(styled_frames_path, input_video_filename).combine_frames(filter_path)



if __name__ == "__main__":
    main()

