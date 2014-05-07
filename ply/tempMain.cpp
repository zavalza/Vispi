
	wiringPiSetup(); //allow the use of wiringPi interface library
	pullUpDnControl(6, PUD_DOWN); //Enable PullUp Resistor connected to GND 
pinMode(6, INPUT); 
pullUpDnControl(3, PUD_OFF); //Disable PullUp Resistor
pinMode(3, OUTPUT); 
pullUpDnControl(4, PUD_OFF); //Disable PullUp Resistor
pinMode(4, OUTPUT); 
pullUpDnControl(1, PUD_OFF); //Disable PullUp Resistor
pinMode(1, PWM_OUTPUT); 
personas = oAnMK;
mensajeAlerta = mozWb;
