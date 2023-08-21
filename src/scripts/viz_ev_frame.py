"""
visulize event frame (npy file).
"""
import argparse
from pathlib import Path
import numpy as np
from tqdm import tqdm
import cv2 as cv

parser = argparse.ArgumentParser(description="Convert the event file to frame.")
parser.add_argument("--input", type=str, help="the path of npz file or dir.")
parser.add_argument("--output", type=str, help="the dir of out event.")
parser.add_argument("--show", action="store_true", help="show the event frame on screen.")
parser.add_argument("--save", action="store_true", help="write the visualization results to dir.")
args = parser.parse_args()

def render_ev_accumulation(ev_frame) -> np.ndarray:
    img = np.full((*ev_frame.shape, 3), fill_value=255, dtype="uint8")
    img[ev_frame == 0] = [255, 255, 255]
    img[ev_frame < 0] = [255, 0, 0]
    img[ev_frame > 0] = [0, 0, 255]
    return img

if __name__ == "__main__":
    print(args)
    in_path = Path(args.input)
    out_path = Path(args.output)
    out_path.mkdir(parents=True, exist_ok=True)

    if in_path.is_dir():
        ev_list = list(in_path.glob("*.npy"))
    else:
        ev_list = [in_path]
    
    for ev_path in tqdm(ev_list):
        ev_frame = np.load(ev_path)
        img = render_ev_accumulation(ev_frame)
        cv.imwrite(str(out_path / ev_path.stem) + ".png", img)
        
        if args.show:
            cv.imshow("img", img)
            cv.waitKey(0)
            cv.destroyAllWindows()