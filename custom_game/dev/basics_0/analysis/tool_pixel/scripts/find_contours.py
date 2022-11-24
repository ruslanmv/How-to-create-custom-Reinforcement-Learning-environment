from pathlib import Path
from os.path import abspath
import sys
SRC: Path = Path(__name__).parent.parent.parent.resolve()
sys.path.append(abspath(SRC))

from src.libs import *
from src.configs import IMAGES

BASE_FILENAME: Path = IMAGES / Path("background.png")
SHOW_FIG_FLAG: bool = False
SAVE_FIG_FLAG: bool = True

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

#contours_found=seats_coordinates[0]
#get_coordinates_from_countour(contours_found)
def get_coordinates_from_countour(contours_found):
    for c in contours_found:
            if cv2.contourArea(c) <= 50 :
                continue    
            x,y,w,h = cv2.boundingRect(c)
            #cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255,0), 2)
            center = (x,y)
            #print (center)
            return center


def create_and_save_seats_clean() -> list:
    image = cv2.imread(str(BASE_FILENAME))
    original = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 208, 94], dtype="uint8")
    upper = np.array([179, 255, 232], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)

    # Find contours
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Extract contours depending on OpenCV version
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    count = 0
    seats_coordinates=[]
    # Iterate through contours and filter by the number of vertices 
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
        if len(approx) > 5:
            cv2.drawContours(original, [c], -1, (36, 255, 12), -1)
            #print([c])
            contours_found = [c]
            coordinates=get_coordinates_from_countour(contours_found)
            print(coordinates)
            seats_coordinates.append([coordinates])
            count += 1
    print('Number of Seats : {}'.format(count))
    if SHOW_FIG_FLAG:
        cv2.imshow('mask', mask)
        cv2.imshow('original', original)
    if SAVE_FIG_FLAG:
        cv2.imwrite(str(IMAGES / Path('mask.png')), mask)
        cv2.imwrite(str(IMAGES / Path('original.png')), original)
    # cv2.waitKey()
    seats_clean = [list(i[0]) for i in seats_coordinates if i[0] is not None]
    with open('seats.pkl', 'wb') as f:
        pickle.dump(seats_clean, f)
    return seats_clean


def show_seats_clean(seats_clean) -> None:
    image = mpimg.imread(str(BASE_FILENAME))
    #seats=[[98, 98], [124, 95], [106, 123], [128, 125], [89, 144], [102, 142], [122, 140], [94, 166], [105, 165], [125, 165], [88, 181], [107, 183], [124, 176]]
    seats=seats_clean
    pts = np.array(seats)
    if SHOW_FIG_FLAG:
        plt.imshow(image)
        plt.plot(1024, 768, "og", markersize=10)  # og:shorthand for green circle
        plt.scatter(pts[:, 0], pts[:, 1], marker="x", color="red", s=3)
        plt.show()
    else:
        plt.close()


def main() -> None:
    logger.debug("Create and save seats clean...")
    seats_clean = \
        create_and_save_seats_clean()
    
    logger.debug("Show seats clean...")
    show_seats_clean(
        seats_clean=seats_clean
    )


if __name__ == "__main__":
    main()
