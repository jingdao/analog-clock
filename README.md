analog-clock
============

Simple analog-style clock in PyQt. Uses QTimer and QPainter functions
to update the clock every second

Usage
-----

command line:
	
	python AnalogClock.py

embed in another PyQt application:

	from AnalogClock import AnalogClock
	g = AnalogClock(parent,size)
	g.show()
