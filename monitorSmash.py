# import the opencv library
import cv2
import numpy as np
import sys


def is_similar(image1, image2):
    if image1.shape != image2.shape:
        return False
    res = cv2.absdiff(image1, image2)
    res = res.astype(np.uint8)
    percentage = (np.count_nonzero(res) * 100) / res.size
    #print(str(percentage) + "%")
    return percentage < 5


def init_score_files():
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

    targetImg2 = cv2.imread("images/p1Rank2.png")
    frameSizeX = int(targetImg2.shape[1])
    frameSizeY = int(targetImg2.shape[0])

    # define a video capture object
    vid = cv2.VideoCapture(capture_index)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    print("Play ball!")
    knowsWinner = False
    screenBlanked = False
    winner = -1
    frame1offX = 745
    frame1offY = 50
    frame2offX = 1535

    # Find who took second place
    while not knowsWinner:
        # Capture the video frame
        ret, frame = vid.read()

        frame1 = frame[frame1offY:frame1offY + frameSizeY, frame1offX:frame1offX + frameSizeX]
        frame2 = frame[frame1offY:frame1offY + frameSizeY, frame2offX:frame2offX + frameSizeX]

        if is_similar(frame1, targetImg2):
            knowsWinner = True
            winner = 2
        if is_similar(frame2, targetImg2):
            knowsWinner = True
            winner = 1

    if 0 <= winner <= 8:
        winStr = "P" + str(winner)
        print(winStr + " wins!")
        winnerPath = "sharedInfo/" + winStr + ".txt"
        increment_file(winnerPath)
        increment_file("sharedInfo/gameCount.txt")

        # wait for screen to blank
        while not screenBlanked:
            ret, frame = vid.read()
            if cv2.countNonZero(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)) == 0:
                screenBlanked = True
    else:
        return False

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cam_index = 0
    print(sys.argv)
    if len(sys.argv) >= 2:
        cam_index = sys.argv[2]
    init_score_files()
    while True:
        keep_score_in_smash(cam_index)
