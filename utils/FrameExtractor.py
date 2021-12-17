import os
import cv2


class FrameExtractor:
    def __init__(self, input_video_path):

        self.input_video_path = input_video_path

        self.output_folder_path = ''


    def create_subfolder(self):
        path_string_length = len(self.input_video_path)

        self.output_folder_path = self.input_video_path[:path_string_length - 4] # delete file extension from string

        if not os.path.exists(self.output_folder_path):
            os.mkdir(self.output_folder_path)


    def extract_frames(self):
                
        cap = cv2.VideoCapture(self.input_video_path)

        ret, frame = cap.read()
        
        if not ret:
            print(f'File is not available at: {self.input_video_path}')

        self.create_subfolder()
        
        cap = cv2.VideoCapture(self.input_video_path)

        count = 0
        while True:
            ret, image = cap.read()

            if not ret:
                break

            cv2.imwrite(os.path.join(self.output_folder_path, f"frame{count}.png"), image)     
            print(f"{count} frames extracted")
            count += 1

        print(f"{count} images are extracted in {self.output_folder_path}.")


FrameExtractor('1.mp4').extract_frames()
