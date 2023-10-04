"""
convert the event file to frame (npy file).
"""
import argparse
from pathlib import Path
import numpy as np
from tqdm import tqdm
import numba
import cv2 as cv
import pandas as pd


parser = argparse.ArgumentParser(description="Convert the event file to frame.")
parser.add_argument("--input", type=str, help="the path of event files.")
parser.add_argument("--output", type=str, help="the dir of out event.")
parser.add_argument("--rgb", type=str, help="the dir of rgb frames.")
parser.add_argument("--sort_by_num", action="store_true", help="sort by number.")
parser.add_argument("--winsz", type=int, default=5, help="the window size of event frame.")
parser.add_argument("--intrinsic", type=str, help="yaml include intrinsic of davis.")
args = parser.parse_args()

@numba.jit()
def accumulate_events(xs, ys, ps, size, ev_frame = None, resolution_level=1, polarity_offset=0):
    if ev_frame is None:
        ev_frame = np.zeros(size, dtype=np.float32)
    for i in range(len(xs)):
        x, y, p = xs[i], ys[i], ps[i]
        ev_frame[y // resolution_level, x // resolution_level] += (p + polarity_offset)
    return ev_frame

def get_info(event_path, rgb_path, sort_by_num=False):
    df = pd.read_csv(event_path)
    df['t'] = df['ts_s'] + df['ts_n'] * 1e-9
    df['polarity'] = df['polarity'].replace({True: 1, False: -1})
    image_list = list(Path(rgb_path).iterdir())

    if sort_by_num:
        image_list = sorted(image_list, key=lambda x: int(x))
    else:
        image_list = sorted(image_list)
    print(image_list[0], image_list[-1])
    return df, image_list

if __name__ == "__main__":
    import os
    print(args)
    out_path = Path(args.output)
    out_path.mkdir(parents=True, exist_ok=True)
    import yaml

    with open(args.intrinsic, 'r') as f:
        davis_data = yaml.safe_load(f)
    
    size = np.array([davis_data['davis']['H'], davis_data['davis']['W']], dtype=np.int32)
    df, image_list = get_info(args.input, args.rgb, sort_by_num=False)
    dist_coeffs = np.array(davis_data['davis']['distortion'], dtype=np.float32)
    fx, fy, cx, cy = davis_data['davis']['fx'], davis_data['davis']['fy'], davis_data['davis']['cx'], davis_data['davis']['cy']
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float32)
    print(f"=== start convert {args.input}, winsz {args.winsz}, size {size},  image_len {len(image_list)} ===")
    
    for i in tqdm(range(0, len(image_list))):
        if i >= args.winsz:
            start_time = float(os.path.basename(image_list[i-args.winsz]).split(".")[0] + "." + os.path.basename(image_list[i-args.winsz]).split(".")[1])
            end_time = float(os.path.basename(image_list[i]).split(".")[0] + "." + os.path.basename(image_list[i]).split(".")[1])
        else:
            start_time = float(os.path.basename(image_list[0]).split(".")[0] + "." + os.path.basename(image_list[0]).split(".")[1])
            end_time = float(os.path.basename(image_list[i]).split(".")[0] + "." + os.path.basename(image_list[i]).split(".")[1])
        assert start_time <= end_time
        start = df.t.searchsorted(start_time, side='right')
        end = df.t.searchsorted(end_time, side='right')

        df_tmp = df.iloc[start:end]
        ev_frame = np.zeros(size, dtype=np.float32)
        ev_frame = accumulate_events(df_tmp["x"].values, df_tmp["y"].values, df_tmp["polarity"].values, size, ev_frame)
        # undistord
        # img_undistorted = cv.undistort(ev_frame, K, dist_coeffs)

        np.save(out_path / "{:.6f}".format(end_time), ev_frame)
        # np.save(out_path/str('un')/ str(i), img_undistorted)
