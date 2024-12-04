import math
import os

import cv2
import moviepy.editor as mp
import numpy as np
from PIL import Image

zoom_in_factor = 0.06
zoom_max_ratio = 0.3  # Maximum zoom-in at the start
zoom_out_factor = 0.04  # Zoom-out speed
duration = 6  # Duration of the video
fps = 40  # Frames per second


def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t))),
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([x, y, new_size[0] - x, new_size[1] - y]).resize(
            base_size, Image.LANCZOS
        )

        result = np.array(img)
        img.close()

        return result

    return clip.fl(effect)


def zoom_out_effect(clip, zoom_max_ratio=0.2, zoom_out_factor=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        # Reverse the zoom effect by starting zoomed in and zooming out
        scale_factor = zoom_max_ratio - (zoom_out_factor * t)
        scale_factor = max(scale_factor, 0)  # Ensure scale factor doesn't go negative

        new_size = [
            math.ceil(base_size[0] * (1 + scale_factor)),
            math.ceil(base_size[1] * (1 + scale_factor)),
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] - (new_size[0] % 2)
        new_size[1] = new_size[1] - (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([x, y, new_size[0] - x, new_size[1] - y])

        # Resize back to base size
        img = img.resize(base_size, Image.LANCZOS)

        result = np.array(img)
        img.close()

        return result

    return clip.fl(effect)


def create_video_from_images(images_folder, output_video, fps=10, duration=6):
    images = sorted(os.listdir(images_folder))

    # create path to the input images
    img_path = os.path.join(images_folder, images[0])

    # load image
    frame = cv2.imread(img_path)
    # extract dimensions of the image
    height, width, channels = frame.shape

    video_writer = cv2.VideoWriter(
        output_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    # total number of frames for the video
    frames_per_image = fps * duration

    for image in images:
        img_path = os.path.join(images_folder, image)
        frame = cv2.imread(img_path)

        for _ in range(frames_per_image):
            video_writer.write(frame)

    video_writer.release()
    print(f"Video {output_video} created successfully")


if __name__ == "main":
    create_video_from_images("/images", "out.mp4")

    slides = (
        mp.ImageClip(image_path).set_fps(fps).set_duration(duration).resize(image_size)
    )

    # add zoom-in effect to input image
    video = zoom_in_effect(slides, zoom_in_factor)

    # save video
    video.write_videofile("zoomin.mp4")

    slides2 = (
        mp.ImageClip(image_path).set_fps(fps).set_duration(duration).resize(image_size)
    )

    video2 = zoom_out_effect(slides2, zoom_max_ratio, zoom_out_factor)

    video2.write_videofile("zoomout.mp4")
