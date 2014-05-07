LXXLIBS+=-L/usr/local/lib
LXXLIBS+=-lopencv_core -lopencv_highgui -lopencv_features2d -lopencv_imgproc -lwiringPi
LXXLIBS+=-L/home/pi/Desktop/git/robidouille/raspicam_cv -lraspicamcv
LXXLIBS+=-L/home/pi/Desktop/git/raspberry/userland/build/lib -lmmal_core -lmmal -l mmal_util -lvcos -lbcm_host

vispi: vispi.cpp
	g++ vispi.cpp -o vispi $(LXXLIBS)

vispi.cpp:
	python vispi.py testCases/FactorialModule.vpi > debugOutput
	rm tempMain.cpp

all: vispi.cpp vispi
	

clean:
	rm vispi.cpp
	rm vispi