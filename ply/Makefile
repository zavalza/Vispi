LXXLIBS+=-L/usr/local/lib
LXXLIBS+=-lopencv_core -lopencv_video -lopencv_highgui -lopencv_features2d -lopencv_imgproc -lwiringPi
LXXLIBS+=-L/home/pi/Desktop/git/robidouille/raspicam_cv -lraspicamcv
LXXLIBS+=-L/home/pi/Desktop/git/raspberry/userland/build/lib -lmmal_core -lmmal -l mmal_util -lvcos -lbcm_host

vispi: vispi.cpp
	g++ vispi.cpp -o vispi $(LXXLIBS)

all: vispi.cpp
	

clean:
	rm vispi.cpp
	rm vispi