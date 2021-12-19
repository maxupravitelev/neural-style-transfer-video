from modules.FrameExtractor import FrameExtractor
from modules.NeuralStyleTransferHandler import NeuralStyleTransferHandler
from modules.ImageResizer import ImageResizer
from modules.FrameCombiner import FrameCombiner

import logging
import os

logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d:%H:%M:%S', format='%(asctime)s | %(levelname)s | %(name)s | LINE %(lineno)d: %(message)s')
log = logging.getLogger(__name__)
log.debug('Logging initialized')


def main():

    input_file_path: str = '1.mp4'

    # extract frames in folder
    #extracted_frames_path, input_video_filename = FrameExtractor(input_file_path).extract_frames()

    # nst all frames in folder
    # styled_frames_path = NeuralStyleTransferHandler(extracted_frames_path, input_video_filename).stylize_batch('stylize_by_filter', place_in_folder=70)
    # styled_frames_path = NeuralStyleTransferHandler(extracted_frames_path='output/extracted_frames/1', input_video_filename='1').stylize_batch('stylize_by_filter', place_in_folder=70)


    # optional: resize all frames in folder
    # resized_frames_path = ImageResizer(styled_frames_path, input_video_filename='1').resize(2)
    # resized_frames_path = ImageResizer(styled_frames_path='output/stylized_frames/1', input_video_filename='1').resize(2)


    # combine all frames in video file
    test = FrameCombiner(styled_frames_path='output/stylized_frames/1', input_video_filename='1').combine_frames()

if __name__ == "__main__":
    main()

