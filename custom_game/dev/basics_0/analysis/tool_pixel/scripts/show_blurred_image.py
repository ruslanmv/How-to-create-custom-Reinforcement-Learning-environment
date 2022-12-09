from pathlib import Path
from os.path import abspath
import sys
SRC: Path = Path(__name__).parent.parent.parent.resolve()
sys.path.append(abspath(SRC))

from src.libs import *
from src.configs import IMAGES

BASE_FILENAME: Path = IMAGES / Path("background.png")
SAVE_FIG_FLAG: bool = True
SHOW_FIG_FLAG: bool = True

import logging
script_name = __name__
def define_script_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger
logger = define_script_logger()


def show_blurred_image():
    img = cv2.imread(str(BASE_FILENAME))
    blur_hor = cv2.filter2D(img[:, :, 0], cv2.CV_32F, kernel=np.ones((11,1,1), np.float32)/11.0, borderType=cv2.BORDER_CONSTANT)
    blur_vert = cv2.filter2D(img[:, :, 0], cv2.CV_32F, kernel=np.ones((1,11,1), np.float32)/11.0, borderType=cv2.BORDER_CONSTANT)
    mask = ((img[:,:,0]>blur_hor*1.2) | (img[:,:,0]>blur_vert*1.2)).astype(np.uint8)*255
    plt.imshow(mask)
    if SAVE_FIG_FLAG:
        img_blurred_path = str(IMAGES / Path("floor_blurred_image.png"))
        plt.savefig(img_blurred_path)
    if SHOW_FIG_FLAG:
        plt.show()
    plt.close()
    return img, mask


def show_image_after_blur_analysi(img, mask) -> None:
    circles = cv2.HoughCircles(mask,
        cv2.HOUGH_GRADIENT,
        minDist=8,
        dp=1,
        param1=150,
        param2=12,
        minRadius=4,
        maxRadius=10
    )
    output = img.copy()
    count = 0
    for (x, y, r) in circles[0, :, :]:
        print(x,y,r)      
        cv2.circle(output, (int(x), int(y)), int(r), (0, 255, 0), 1)
        count += 1
    # show the output image
    print('Number of Seats: {}'.format(count))
    if SHOW_FIG_FLAG:
        cv2.imshow("output", np.hstack([output]))
    if SAVE_FIG_FLAG:
        cv2.imwrite('output.jpg',np.hstack([output]),[cv2.IMWRITE_JPEG_QUALITY, 70])


def main() -> None:

    logger.debug("Show Blurred Image...")
    img, mask = show_blurred_image()

    logger.debug("Show Image after Blur Analysis...")
    show_image_after_blur_analysi(img, mask)
    # cv2.waitKey(0)


if __name__ == "__main__":
    main()
