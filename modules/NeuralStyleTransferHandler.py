import functools
import os
import logging

import tensorflow as tf
import tensorflow_hub as hub

log = logging.getLogger(__name__)


class NeuralStyleTransferHandler:
    def __init__(self, extracted_frames_path:str, input_video_filename:str) -> None:
        os.environ['CUDA_VISIBLE_DEVICES']='-1'    # disable gpu

        log.debug('TF Version: ', tf.__version__)
        log.debug('TF-Hub version: ', hub.__version__)
        log.debug('Eager mode enabled: ', tf.executing_eagerly())
        log.debug('GPU available: ', tf.config.list_physical_devices('GPU'))

        # Load TF-Hub module

        # TODO: check if downloaded and set up on first startup, load from local afterwards
        #hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
        hub_handle = 'models/arbv1'
        self.hub_module = hub.load(hub_handle)

        self.extracted_frames_path = extracted_frames_path
        self.input_video_filename = input_video_filename

        parent_dir = 'output/stylized/'

        self.stylized_frames_path = os.path.join(parent_dir, input_video_filename)

        if not os.path.exists(self.stylized_frames_path):
            try:
                os.makedirs(self.stylized_frames_path)
                log.debug(f'Output path for extracted frames: {self.stylized_frames_path}')
            except Exception as e:
                log.error(f'Output path for extracted frames FAILED: {e}')

        log.debug('FrameExtractor initialized')


    def crop_center(self, image):
        '''Returns a cropped square image.'''
        shape = image.shape
        new_shape = min(shape[1], shape[2])
        offset_y = max(shape[1] - shape[2], 0) // 2
        offset_x = max(shape[2] - shape[1], 0) // 2
        image = tf.image.crop_to_bounding_box(
            image, offset_y, offset_x, new_shape, new_shape)
        return image


    def img_scaler(self, image, max_dim = 256):

        # Casts a tensor to a new type.
        original_shape = tf.cast(tf.shape(image)[:-1], tf.float32)

        # Creates a scale constant for the image
        scale_ratio = max_dim / max(original_shape)

        # Casts a tensor to a new type.
        new_shape = tf.cast(original_shape * scale_ratio * 1, tf.int32)

        # Resizes the image based on the scaling constant generated above
        return tf.image.resize(image, new_shape)


    @functools.lru_cache(maxsize=None)
    def load_image(self, image_url, image_size=(256, 256), preserve_aspect_ratio=True):
        '''Loads and preprocesses images.'''
        # Cache image file locally.
        #image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
        image_path = image_url
        # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
        img = tf.io.decode_image(
            tf.io.read_file(image_path),
            channels=3, dtype=tf.float32)
        

        #img = crop_center(img)
        img = self.img_scaler(img)

        #img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
        return img[tf.newaxis, ...]





    def stylize_batch(self, mode:str,  place_in_folder: int):

        if mode == "stylize_by_all_filters":
            foldername = self.extracted_frames_path
            files_in_folder = len([file for file in os.listdir(f'{foldername}/')])
            stylized_folder = f'output/stylized/{self.input_video_filename}_all_filter'
        else: 
            foldername = self.extracted_frames_path
            files_in_folder = len([file for file in os.listdir(f'{foldername}/')])
            stylized_folder = f'output/stylized/{self.input_video_filename}'

        if not os.path.exists(stylized_folder):
            os.mkdir(stylized_folder)

        #  for i in range(0,60):
        for i in range(files_in_folder):

            if mode == 'stylize_by_all_filters':

                content_image_url: str = f'{self.extracted_frames_path}/frame{place_in_folder}.png'
                style_image_url: str = f'filter/{i}.jpg'  
            
            elif mode=='stylize_by_filter':
                content_image_url: str = f'{self.extracted_frames_path}/frame{i}.png'
                style_image_url: str = f'filter/{place_in_folder}.jpg' 
            
            output_image_size: int = 512


            # The content image size can be arbitrary.
            content_img_size = (output_image_size, output_image_size)
            # The style prediction model was trained with image size 256 and it's the 
            # recommended image size for the style image (though, other sizes work as 
            # well but will lead to different results).
            style_img_size = (256, 256)  # Recommended to keep it at 256.

            content_image = self.load_image(content_image_url, content_img_size)
            style_image = self.load_image(style_image_url, style_img_size)
            print(style_image.shape)
            style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')


            outputs = self.hub_module(tf.constant(content_image), tf.constant(style_image))

            stylized_image = outputs[0]
            squeezed_image = tf.squeeze(stylized_image)
            
            tf.keras.preprocessing.image.save_img(f'{self.stylized_frames_path}/frame{i}.png', squeezed_image)

# stylize_batch("stylize_by_all_filters", 22)
#stylize_batch("stylize_by_filter", 34)


# Built upon: https://www.tensorflow.org/hub/tutorials/tf2_arbitrary_image_stylization
