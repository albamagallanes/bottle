import cv2
import numpy 
import glob
from sets import Set

class TareaFinal:
	def loadImages(self):
		cv2.namedWindow('image')
		for picname in glob.glob('img/botella*.jpg'):
		#for picname in glob.glob('img/botella1.jpg'):
		#for picname in glob.glob('img/dona.png'):
			self.img = cv2.imread(picname, cv2.CV_LOAD_IMAGE_GRAYSCALE)
			self.img2 = cv2.imread(picname)
			#self.gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			thresh = 110 #100
			self.img_binary = cv2.threshold(self.img, thresh, 255, cv2.THRESH_BINARY)[1]
			self.width, self.height = self.img_binary.shape[:2]
			#cv2.imwrite('binary_image.png', img_binary)
			self.getMaxArea()
			#self.getBottleType()
			
			#if self.maxArea>= 4000:
			#	print "Botella OK!"
			#else:
			#	print "Botella le falta liquido"
			
			cv2.imshow('image',self.img_binary)
			cv2.imshow('image2',self.img2)
			cv2.waitKey()
	
	def getMaxArea(self):
		self.filled = set()
		self.maxArea=0
		totalWhite=0
		totalBlack=0
		for x in xrange (self.width):
			for y in xrange (self.height):
				px = self.img_binary[x,y]
				if (px == 255):
					totalWhite=totalWhite+1
					continue
				totalBlack=totalBlack+1
				if (x,y) not in self.filled:
					self.floodFill(x,y)
					
		print "WHITE",totalWhite,"BLACK",totalBlack,"MAX",self.maxArea
		
	def floodFill(self,current_x,current_y):
		total = 0
		toFill = set()
		toFill.add((current_x,current_y))
		while len(toFill) > 0:
			(x,y) = toFill.pop()
			if (x<0 or x>self.width-1 or y<0 and y>self.height-1):
				continue
			pixel = self.img_binary[x,y]
			if pixel == 255:
				continue
			if (x-1,y) not in self.filled:
				toFill.add((x-1,y))
			if (x+1,y) not in self.filled:
				toFill.add((x+1,y))
			if (x,y-1) not in self.filled:
				toFill.add((x,y-1))
			if (x,y+1) not in self.filled:
				toFill.add((x,y+1))
			self.filled.add((x,y))
			total=total+1
			#toFill.discard((x,y))
		if total > self.maxArea:
			self.maxArea=total
	
	def getBottleType(self):
		print "MAX ",self.maxArea
		
	
mona = TareaFinal()
mona.loadImages()
cv2.waitKey()