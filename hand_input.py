import cv2
import numpy as np
import math

def index_loc(img):
    height,width = img.shape
    lowest_row = 1000
    col_save = None
    reached = False
    for row in range(height):
        for col in range(width):
            if np.array_equal(255, img[row][col]) and row < lowest_row:
                lowest_row = row
                col_save = col
                return (lowest_row,col_save) #(y,x)
    return (lowest_row,col_save)
def categorize(img_src, img_copy):
    src = cv2.resize(img_src, (578,578))
    game_img = src.copy()
    copy = cv2.resize(img_copy, (578,578))

    '''
    Citation for Code Below:
    Permission: tutorial
    Source: https://pythonexamples.org/python-opencv-extract-red-channel-of-image/
    '''
    # extract red channel
    red_channel = src[:,:,2]
    # create empty image with same shape as that of src image
    red_img = np.zeros(src.shape)

    #assign the red channel of src to empty image
    red_img[:,:,2] = red_channel
    lower_bound_color = (0,0,0)
    upper_bound_color = (0,0,150)



    '''
    Citation for Code Below:
    Permission: 3-Clause BSD License
    Source:'https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html'
    '''
    mask =  cv2.inRange(red_img, lower_bound_color, upper_bound_color)

    mask = cv2.bitwise_not(mask)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=4)
    '''
    Citation for Code Below:
    Permission: 3-Clause BSD License
    Source: 'https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html'
    '''
    # convert image to grayscale image
    gray_image = copy
    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(gray_image,127,255,0)
    # calculate moments of binary image
    M = cv2.moments(thresh)
    # calculate x,y coordinate of centroid
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    # put text and highlight the center
    cv2.circle(src, (cX, cY), 5, (25, 25, 112), -1)
    cv2.putText(src, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)



    #print("cX: {}, cY: {}".format(cX,cY))
    # display the image
    #cv2.imshow("Two_centroid", src)

    '''
    One: cX: 386, cY: 394
    Two: (368,397)
    Three: cX: 364, cY: 395
    Four: cX: 343, cY: 380
    Splay_Center: cX: 345, cY: 404
    Splay_Lower_Left: cX: 154, cY: 534
    Splay_Lower_Right: cX: 562, cY: 675
    Splay_Upper_Right: cX: 559, cY: 164
    Splay_Upper_Left: cX: 190, cY: 143
    '''
    quadrant = 0
    '''
    1 | 2 | 3
    4 | 5 | 6
    7 | 8 | 9
    '''
    #print("{} {}".format(cX,cY))
    if 500>cX>250 and 500>cY>250:
        quadrant = 5 #center
    elif cX<250 and cY<250:
        quadrant = 1 #upper_left
    elif cX>500 and cY<250:
        quadrant = 3 #upper_right
    elif cX<250 and cY>500:
        quadrant = 7 #lower_left
    elif cX>500 and cY>500:
        quadrant = 9 #lower_right
    elif 500>cX>250 and cY<250: #BAD SECTIONS
        quadrant = 2 #top_center
    elif cX<250 and 500>cY>250:
        quadrant = 4 #center_left
    elif cX>500 and 500>cY>250:
        quadrant = 6 #center_right
    elif 500>cX>250 and cY>500:
        quadrant = 8 #bottom_center
    else:
        quadrant = None

    #Centering rectangle
    cv2.rectangle(copy, (250,250), (500,500), (255,255,255), 2)

    #centroid
    cv2.circle(copy, (cX, cY), 10 , (0,0,255))

    '''
    Citation for Code Below:
    Permission: 3-Clause BSD License
    Source: https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
    '''
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(copy, contours, -1, (255,0,0), 3)

    #https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
    #area = cv.contourArea(cnt)
    '''
    Citation for Code Below:
    Source: https://github.com/rkbvikrant/Hand-Gesture-Recognition-Python-OPENCV/tree/master/Hand%20gesture
    Permission: OpenSource + Blog tutorial
    '''
    blurred = cv2.GaussianBlur(mask, (35,35), 0)
    _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #cv2.imwrite('Lower_Left_Failure.jpg', thresh1)
    max_area = -1
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
    cnt=contours[ci]

    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(copy,(x,y),(x+w,y+h),(0,0,255),0)
    area_contour = cv2.contourArea(cnt)
    hull = cv2.convexHull(cnt)
    area_hull = cv2.contourArea(hull)
    if area_contour != 0:
        area_ratio = (((area_hull-area_contour)/area_contour) *100)

    drawing = np.zeros(copy.shape,np.uint8)
    hand_outline = drawing.copy()
    cv2.drawContours(hand_outline,[cnt],0,(255,255,255),0)
    cv2.drawContours(drawing,[hull],0,(255,255,255),0)
    finger_row,finger_col = index_loc(drawing)
    #cv2.rectangle(drawing,(finger_row-10,finger_col-10),(finger_row+10,finger_col+10), 255,1)
    #frame  = game_img.copy()
    #cv2.imshow("tst", drawing)
    #cv2.waitKey(0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)

    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        #cv2.circle(copy,far,1,[0,0,0],-1)
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(copy,far,1,[255,255,255],-1)
    hand = None
    #counts number of defects to return hand shape
    if count_defects == 0:
        if area_ratio <10:
            hand = "Fist"
        else:
            hand = "One"
    elif count_defects == 1:
        hand = "Two"
    elif count_defects == 2:
        hand = "Three"
    elif count_defects == 3:
        hand = "Four"
    elif count_defects == 4:
        hand = "Five"

    result = "{}".format((hand, quadrant))
    cv2.putText(copy,result, (20,400), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2)
    result = result+".jpg"
    cv2.rectangle(game_img,(finger_col-10,finger_row-10),(finger_col+10,finger_row+10), (255, 255, 255),1)
    frame  = game_img.copy()
    #cv2.imwrite(result, copy) Uncomment this if you wish to have the final labeled image written to the directory
    return (hand, (finger_row, finger_col), frame)
#if __name__ == "__main__":
    #i = "algo/One.jpg"
    #src = cv2.imread(i,cv2.IMREAD_UNCHANGED)
    #copy = cv2.imread(i, cv2.IMREAD_GRAYSCALE)
    #hand,quadrant = categorize(src, copy)
