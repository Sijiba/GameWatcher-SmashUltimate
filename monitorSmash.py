# import the opencv library
import cv2
import numpy as np
import sys
import time


def init_scoreFiles():
    f = open("sharedInfo/gameCount.txt", "w")
    f.write(str(0))
    f.close()
    f = open("sharedInfo/P1.txt", "w")
    f.write(str(0))
    f.close()
    f = open("sharedInfo/P2.txt", "w")
    f.write(str(0))
    f.close()


def increment_file(path):
    val = 0
    try:
        f = open(path, "r")
        g = int(f.read())
        f.close()
        val = g
    except:
        pass
    val += 1
    f = open(path, "w")
    f.write(str(val))
    f.close()


def keep_score_in_smash(capture_index=0):
    targetImg1 = cv2.imread("images/bottomLeftCorner.png")
    bottomleftSizeX = int(targetImg1.shape[1])
    bottomleftSizeY = int(targetImg1.shape[0])

    targetImg2 = cv2.imread("images/p1Rank2.png")
    frame2sizeX = int(targetImg2.shape[1])
    frame2sizeY = int(targetImg2.shape[0])

    # define a video capture object
    vid = cv2.VideoCapture(capture_index)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    print("Play ball!")
    hasWinner = False
    knowsWinner = False
    winner = -1

    # Scan for end screen to appear
    while not hasWinner:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        frame = frame[frame.shape[0] - bottomleftSizeY:frame.shape[0], 0:bottomleftSizeX]
        if not np.bitwise_xor(frame, targetImg1).any():
            hasWinner = True
            winner = 2
        else:
            time.sleep(0.1)

    print("Game over!")
    increment_file("sharedInfo/gameCount.txt")

    frame1offX = 745
    frame1offY = 50
    frame2offX = 1535

    # Find who took second place
    while not knowsWinner:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        frame1 = frame[frame1offY:frame1offY + frame2sizeY, frame1offX:frame1offX + frame2sizeX]
        frame2 = frame[frame1offY:frame1offY + frame2sizeY, frame2offX:frame2offX + frame2sizeX]
        if not np.bitwise_xor(frame1, targetImg2).any():
            knowsWinner = True
            winner = 2
        if not np.bitwise_xor(frame2, targetImg2).any():
            knowsWinner = True
            winner = 1

    winStr = "P" + str(winner)
    print(winStr)
    winnerPath = "sharedInfo/" + winStr + ".txt"
    increment_file(winnerPath)

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cam_index = 2
    print(sys.argv)
    if len(sys.argv) >= 2:
        cam_index = sys.argv[2]
    init_scoreFiles()
    while True:
        keep_score_in_smash(cam_index)
