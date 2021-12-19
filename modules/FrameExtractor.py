import os
import cv2
import logging

log = logging.getLogger(__name__)


class FrameExtractor:
    def __init__(self, input_video_path:str) -> None:

        self.input_video_path:str = input_video_path

        self.input_video_filename:str = ''

        self.extracted_frames_path:str = ''

        # if not os.path.exists(self.extracted_frames_path):
        #     try:
        #         os.makedirs(self.extracted_frames_path)
        #         log.debug(f'Output path for extracted frames: {self.extracted_frames_path}')
        #     except Exception as e:
        #         log.error(f'Output path for extracted frames FAILED: {e}')

        log.debug('FrameExtractor initialized')

    def create_subfolder(self):
        path_string_length:str = len(self.input_video_path)

        self.input_video_filename = self.input_video_path[:path_string_length - 4] # delete file extension from string

        parent_dir = 'output/extracted_frames/'

        self.extracted_frames_path = os.path.join(parent_dir, self.input_video_filename)

        log.debug(f'Output path for extracted frames: {self.extracted_frames_path}')

        if not os.path.exists(self.extracted_frames_path):
            try:
                os.makedirs(self.extracted_frames_path)
                log.debug(f'Output path for extracted frames: {self.extracted_frames_path}')
            except Exception as e:
                log.error(f'Output path for extracted frames FAILED: {e}')



    def extract_frames(self) -> str:
                
        cap = cv2.VideoCapture(self.input_video_path)

        ret, frame = cap.read()
        
        if not ret:
            log.error(f'File is not available at: {self.input_video_path}')

        self.create_subfolder()
        
        cap = cv2.VideoCapture(self.input_video_path)

        count:int = 0

        while True:
            ret, image = cap.read()

            if not ret:
                break

            cv2.imwrite(os.path.join(self.extracted_frames_path, f"frame{count}.png"), image)     
            log.info(f"{count} frames extracted")
            count += 1

        log.info(f"{count} images are extracted in {self.extracted_frames_path}.")

        return self.extracted_frames_path, self.input_video_filename


# FrameExtractor('1.mp4').extract_frames()
