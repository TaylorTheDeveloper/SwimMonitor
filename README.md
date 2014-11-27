SwimMonitor
===========

Tracking Swimmers in a pool.

Some Sample Video can be found here:
https://drive.google.com/folderview?id=0BwK-dcuoOzfdUlhnZC1rODRzVFk&usp=sharing

How to use:

1. Make sure you have openCV installed. I'm using version 2.4.9.
2. old/colorFilter.cpp
	* Run ./build.sh
	* Then ./colorFilter
	* Currently Loops, so you can adjust settings

3. old/colorFilter.py
	* Run python colorFilter.py

4. filterBlue.py
	* Focus on Filtering Blue hues out of images for swimmer segmentation in python

Currently, both of these programs attempt to do the same thing. The Python version runs much faster than the CPP version, however, it's not as accurate. 
