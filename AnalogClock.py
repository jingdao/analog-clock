#!/usr/bin/python
from PyQt4 import QtCore,QtGui
import datetime
import math

class AnalogClock(QtGui.QWidget):
	def __init__(self,parent,width=400):
		QtGui.QWidget.__init__(self,parent)
		self.thickPen=QtGui.QPen(QtGui.QColor(0x000000),3,QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
		self.thinPen=QtGui.QPen(QtGui.QColor(0x000000),1,QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
		self.penHour=QtGui.QPen(QtGui.QColor(0x0000ff),6,QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
		self.penMinute=QtGui.QPen(QtGui.QColor(0x0000ff),3,QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
		self.penSecond=QtGui.QPen(QtGui.QColor(0xff0000),1,QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
		self.clock = QtCore.QTimer()
		self.clock.timeout.connect(self.updateClock)
		self.resize(QtCore.QSize(width,width))

	def resizeEvent(self,e):
		self.clock.stop()
		self.radius=min(e.size().width(),e.size().height())/2
		self.minorTicks=[]
		self.innerTicks=[]
		self.outerTicks=[]
		dt=math.pi*2/60
		t=math.pi/2
		for i in range(0,60):
			dx=math.cos(t)
			dy=math.sin(t)
			self.minorTicks.append((self.radius+self.radius*dx,self.radius-self.radius*dy))
			self.outerTicks.append((self.radius+(self.radius-10)*dx,self.radius-(self.radius-10)*dy))
			self.innerTicks.append((self.radius+self.radius*dx/2,self.radius-self.radius*dy/2))
			t-=dt
		self.getCurrentTime()
		self.clock.start(1000)
		self.update()

	def getCurrentTime(self):
		d=datetime.datetime.now()
		self.hourTicks=(d.hour%12)*5+d.minute/12
		self.minuteTicks=d.minute
		self.secondTicks=d.second

	def updateClock(self):
		self.secondTicks+=1
		if self.secondTicks==60:
			self.secondTicks=0
			self.minuteTicks+=1
			if self.minuteTicks%12==0:
				if self.minuteTicks==60:
					self.minuteTicks=0
				self.hourTicks+=1
				if self.hourTicks==60:
					self.hourTicks=0
		self.update()

	def paintEvent(self,event):
		painter = QtGui.QPainter(self)
		painter.setPen(self.thickPen)
		#painter.drawEllipse(self.rect())
		painter.drawEllipse(0,0,self.radius*2,self.radius*2)
		painter.setPen(self.penHour)
		painter.drawLine(self.radius,self.radius,self.innerTicks[self.hourTicks][0],self.innerTicks[self.hourTicks][1])
		painter.setPen(self.penMinute)
		painter.drawLine(self.radius,self.radius,self.outerTicks[self.minuteTicks][0],self.outerTicks[self.minuteTicks][1])
		painter.setPen(self.penSecond)
		painter.drawLine(self.radius,self.radius,self.outerTicks[self.secondTicks][0],self.outerTicks[self.secondTicks][1])
		for i in range(0,60):
			if i%5==0:
				painter.setPen(self.thickPen)
			else:
				painter.setPen(self.thinPen)
			painter.drawLine(self.outerTicks[i][0],self.outerTicks[i][1],self.minorTicks[i][0],self.minorTicks[i][1])

if __name__=='__main__':
	app=QtGui.QApplication([])
	g = AnalogClock(None)
	g.move(0,0)
	g.resize(200,200)
	g.setWindowTitle('Analog Clock')
	g.show()
	app.exec_()
