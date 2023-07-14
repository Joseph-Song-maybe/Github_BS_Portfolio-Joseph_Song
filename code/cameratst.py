import cv2

vid = cv2.VideoCapture(0)

while(True):
    ret, frame = vid.read()
    height = frame.shape[0]
    width = frame.shape[1]
    
    if ret:
        # cv2.imshow('frame', frame)
        
        # frame_r: resized tensor H/4,W/4,3
        frame_r = cv2.resize(frame, (width//4,height//4))
        # I guess that camera (VideoCapture.read) captures in RGB, but cv2.imshow uses BGR to display.
        # I decided to flip the channel order [0,1,2] (from camera) to [2,1,0] (to display via cv2.imshow) 
        cv2.imshow('frame', frame_r[:,:,[2,1,0]])
        #cv2.imshow('frame', frame_r)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
        
vid.release()
cv2.destroyAllWindows()
