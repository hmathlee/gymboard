import cv2
import os
import argparse
from pathlib import Path
from tqdm import tqdm


def split_video(video_fp: str, frame_dir: str, sample_rate: int = 1):
    """
    Splits video into frames; saves (fps_factor * 100)% of them.
    :param video_fp: Path to video.
    :param frame_dir: Frame save directory.
    :param sample_rate: Every (sample_rate)^th frame is written.
    :return: None.
    """

    video_capture = cv2.VideoCapture(str(video_fp))
    if not video_capture.isOpened():
        print("Error: Could not open video:", video_fp)
        exit()

    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    for frame_ct in range(0, total_frames, sample_rate):
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_ct)
        ret, frame = video_capture.read()
        video_fname = os.path.basename(video_fp)
        frame_fname = os.path.splitext(video_fname)[0] + f"_frame_{frame_ct}.jpg"
        cv2.imwrite(os.path.join(frame_dir, frame_fname), frame)

    video_capture.release()


def split_dir_videos(video_dir: Path, sample_rate: int = 1):
    video_dir = Path(video_dir)
    frame_dir = video_dir.parent / (str(video_dir) + "_frames")
    if not os.path.exists(frame_dir):
        os.mkdir(frame_dir)

    for label in video_dir.glob("*"):
        print(f"Splitting videos for label: {label.name}")

        label_frame_dir = os.path.join(frame_dir, label.name)
        if not os.path.exists(label_frame_dir):
            os.mkdir(label_frame_dir)

        for vid in tqdm(label.glob("*")):
            split_video(vid, label_frame_dir, sample_rate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video_dir", help="Video directory.")
    parser.add_argument("-s", "--sample_rate", type=int, help="""Sample rate. The script will wait until this number of 
    frames have passed before writing the next one.""")
    args = vars(parser.parse_args())

    split_dir_videos(args["video_dir"], args["sample_rate"])
