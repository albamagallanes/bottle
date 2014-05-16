import cv2
import numpy 
import glob
from sets import Set

class TareaFinal:
	def loadImages(self):
		cv2.namedWindow('image')
		for picname in glob.glob('img3/bien/*.jpg'):
			self.img = cv2.imread(picname, cv2.CV_LOAD_IMAGE_GRAYSCALE)
			self.img2 = cv2.imread(picname)
			thresh = 90 #100
			thresh, self.img_binary = cv2.threshold(self.img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
			self.height,self.width = self.img_binary.shape[:2]
			self.getMaxArea()
			print picname
			print self.getBottleType(),"with",self.getLiquidType(),"and",self.qualityOk()
			
			#cv2.imshow('image',self.img_binary)
			#cv2.imshow('image2',self.img2)
			#cv2.waitKey()
			
	
	def getMaxArea(self):
		self.filled = set()
		self.maxArea=0
		totalWhite=0
		totalBlack=0
		for h in xrange (self.height):
			for w in xrange (self.width):
				px = self.img_binary[h,w]
				if (px == 255):
					totalWhite=totalWhite+1
					continue
				totalBlack=totalBlack+1
				if (h,w) not in self.filled:
					self.floodFill(h,w)
					
		#print "WHITE",totalWhite,"BLACK",totalBlack,"MAX",self.maxArea
		
	def floodFill(self,current_h,current_w):
		total = 0
		toFill = set()
		toFill.add((current_h,current_w))
		colors=[0,0,0]
		while len(toFill) > 0:
			(h,w) = toFill.pop()
			if (w<0 or w>self.width-1 or h<0 and h>self.height-1):
				continue
			pixel = self.img_binary[h,w]
			if pixel == 255:
				continue
			(r,g,b) = self.img2[h,w]
			colors[0]+=r
			colors[1]+=g
			colors[2]+=b
			if (h-1,w) not in self.filled:
				toFill.add((h-1,w))
			if (h+1,w) not in self.filled:
				toFill.add((h+1,w))
			if (h,w-1) not in self.filled:
				toFill.add((h,w-1))
			if (h,w+1) not in self.filled:
				toFill.add((h,w+1))
			self.filled.add((h,w))
			total=total+1
		if total > self.maxArea:
			self.maxArea=total
			colors[0]/=total
			colors[1]/=total
			colors[2]/=total
			self.colorAverage=colors
	
	def getBottleType(self):
		sizeThreshold=30000
		if self.maxArea < sizeThreshold: #GlassBottle
			self.bottle=0
			return "Glass Bottle"
		else: 
			self.bottle=1
			return "Plastic Bottle"
		
	def getLiquidType(self):
		colorThreshold=180
		colorResult= self.colorAverage[0]+self.colorAverage[1]+self.colorAverage[2]
		if colorResult < colorThreshold: #DARK ONE
			return "Apple Juice"
		else: #YELLOW ONE
			return "Lemon Juice"
	
	def qualityOk(self): #[glass,plastic]
		bottlesThreshold=[23000,45000]
		if self.maxArea < bottlesThreshold[self.bottle]:
			return "BAD Quality"
		else:
			return "Quality OK!"
		
classifier = TareaFinal()
classifier.loadImages()
cv2.waitKey()