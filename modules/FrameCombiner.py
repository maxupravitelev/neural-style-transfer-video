import cv2
import os
import logging


log = logging.getLogger(__name__)

class FrameCombiner:
    def __init__(self, styled_frames_path:str, input_video_filename:str) -> None:
        
        self.styled_frames_path:str = styled_frames_path
        self.input_video_filename:str = input_video_filename
        
        log.debug('FrameCombiner initialized')
        

    def combine_frames(self, filtername):

        img = cv2.imread(f'{self.styled_frames_path}/frame0.png', 0)

        # choose codec according to format needed
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        video = cv2.VideoWriter(f'{self.input_video_filename}_stylized_filter{filtername}.mp4', fourcc, 24, (img.shape[1], img.shape[0]))

        files_in_folder = len([file for file in os.listdir(f'{self.styled_frames_path}/')])

        for frame_count in range(0, files_in_folder):
            img = cv2.imread(f'{self.styled_frames_path}/frame{frame_count}.png')
            video.write(img)
            log.debug(f'{frame_count} frames combined')

        cv2.destroyAllWindows()
        video.release()