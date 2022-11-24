from pathlib import Path
from os.path import abspath
import sys
SRC: Path = Path(__name__).parent.parent.parent.resolve()
sys.path.append(abspath(SRC))

from src.libs import *
from src.configs import IMAGES

BASE_FILENAME: Path = IMAGES / Path("background.png")


def main():
    img = cv2.imread(str(BASE_FILENAME))
    blur_hor = cv2.filter2D(img[:, :, 0], cv2.CV_32F, kernel=np.ones((11,1,1), np.float32)/11.0, borderType=cv2.BORDER_CONSTANT)
    blur_vert = cv2.filter2D(img[:, :, 0], cv2.CV_32F, kernel=np.ones((1,11,1), np.float32)/11.0, borderType=cv2.BORDER_CONSTANT)
    mask = ((img[:,:,0]>blur_hor*1.2) | (img[:,:,0]>blur_vert*1.2)).astype(np.uint8)*255
    plt.imshow(mask)
    plt.show()

    circles = cv2.HoughCircles(mask,
                            cv2.HOUGH_GRADIENT,
                            minDist=8,
                            dp=1,
                            param1=150,
                            param2=12,
                            minRadius=4,
                            maxRadius=10)
    output = img.copy()
    count = 0
    for (x, y, r) in circles[0, :, :]:
        print(x,y,r)      
        cv2.circle(output, (int(x), int(y)), int(r), (0, 255, 0), 1)
        count += 1
    # show the output image
    print('Number of Seats: {}'.format(count))
    cv2.imshow("output", np.hstack([output]))
    # cv2.imwrite('output.jpg',np.hstack([output]),[cv2.IMWRITE_JPEG_QUALITY, 70])
    # cv2.waitKey(0)


if __name__ == "__main__":
    main()
