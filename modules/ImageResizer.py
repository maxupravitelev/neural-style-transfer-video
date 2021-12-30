import PIL
import os
import os.path
from PIL import Image
import logging



log = logging.getLogger(__name__)

class ImageResizer:
    def __init__(self, styled_frames_path:str, input_video_filename:str) -> None:

        self.styled_frames_path = styled_frames_path
        self.files_in_folder = len([file for file in os.listdir(f'{self.styled_frames_path}/')])

        self.input_video_filename = input_video_filename
        
        self.resized_frames_path = ''

        self.create_subfolder()


    def create_subfolder(self):

        # path_string_length:str = len(self.input_video_filename)

        # self.input_video_filename = self.input_video_filename[:path_string_length - 4] # delete file extension from string

        parent_dir = 'output/resized_frames/'

        self.resized_frames_path = os.path.join(parent_dir, self.input_video_filename)

        if not os.path.exists(self.resized_frames_path):
            try:
                os.makedirs(self.resized_frames_path)
                log.debug(f'Output path for resized frames: {self.resized_frames_path}')
            except Exception as e:
                log.error(f'Output path for resized frames FAILED: {e}')


    def resize(self, resize_factor=2):

        for file_count in range(self.files_in_folder):
            image_path = self.styled_frames_path + '/' + f'frame{file_count}.png'

            img = Image.open(image_path)
            img = img.resize((img.size[0] * resize_factor, img.size[1] * resize_factor)) # (width, height)

            img.save(self.resized_frames_path + '/' + f'frame{file_count}.png')
            
            log.debug(f"{file_count} frames resized")

        return self.resized_frames_path





    def resize_superres(self, resize_factor):

        import numpy as np
        # import sys
        # sys.path.append('..')
        from ISR.models import RDN, RRDN

        #model = RDN(weights='noise-cancel')
        #model = RRDN(weights='gans')
        model = RDN(weights='psnr-small')
        #model = RDN(weights='psnr-large')

        for file_count in range(self.files_in_folder):
            image_path = self.styled_frames_path + '/' + f'frame{file_count}.png'

            img = Image.open(image_path)

            img.resize(size=(img.size[0]*resize_factor, img.size[1]*resize_factor), resample=Image.BICUBIC)
            sr_img = model.predict(np.array(img))

            new_image = Image.fromarray(sr_img)
            new_image.save(f'{self.resized_frames_path}/frame{file_count}.png')
            
            log.debug(log.debug(f"{file_count} frames resized"))

        return self.resized_frames_path





