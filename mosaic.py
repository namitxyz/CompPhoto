import os
import cv2
import numpy as np
import sys
import scipy as sp
import glob
import heapq

def FindAverage(image):

	red_hist = cv2.calcHist([image],[2], None, [256],[0,256])
	grn_hist = cv2.calcHist([image],[1], None, [256],[0,256])
	blu_hist = cv2.calcHist([image],[0], None, [256],[0,256])

	sum = 0
	for i in range(0,len(red_hist)):
		sum = sum + (int(red_hist[i])*i)
	Red = sum / (image.shape[0]*image.shape[1])

	sum = 0
	for i in range(0,len(grn_hist)):
		sum = sum + (int(grn_hist[i])*i)
	Green = sum / (image.shape[0]*image.shape[1])

	sum = 0
	for i in range(0,len(blu_hist)):
		sum = sum + (int(blu_hist[i])*i)
	Blue = sum / (image.shape[0]*image.shape[1])

	return Red, Green, Blue

def ComputeDifferences(InputImg, Library, Tile, OutputImageFile):

	rows = InputImg.shape[0]
	cols = InputImg.shape[1]

	for i in range(0, rows/Tile):
		for j in range(0, cols/Tile):
			SingleTileImg = InputImg[i * Tile:(i + 1) * Tile, j * Tile:(j + 1) * Tile]
			Red_Tile, Green_Tile, Blue_Tile = FindAverage(SingleTileImg)

			heap = []

			for key in Library.keys():
				Red_lib = key[1]
				Green_lib = key[2]
				Blue_lib = key[3]

				MeanSquare = pow((Red_lib - Red_Tile), 2) + pow((Green_lib - Green_Tile), 2) + pow((Blue_lib - Blue_Tile), 2)
				heapq.heappush(heap, (MeanSquare, key))

			InputImg[i * Tile:(i + 1) * Tile, j * Tile:(j + 1) * Tile] = Library[heap[0][1]]


	cv2.imwrite(OutputImageFile, InputImg)


def main():
	if len(sys.argv) !=5:
		print "Invalid Arguments. Usage: python mosaic.py <InputImage.jpg> <TilePixels> <OutputImage.jpg> <Path_To_Image_Library>"
		return
	
	InputImg = cv2.imread(sys.argv[1])
	Tile = sys.argv[2]
	OutputImageFile = sys.argv[3]
	LibraryPath = sys.argv[4]

	Library = {}

	images = glob.glob(LibraryPath + "/" + "*.jpg")

	for img in images:
		Libimage = cv2.imread(img)
		Libimage = cv2.resize(Libimage, (int(Tile),int(Tile)), interpolation=cv2.INTER_AREA)
		Red, Green, Blue = FindAverage(Libimage)
		Library[img, Red, Green, Blue] = Libimage

	InputImg = InputImg[0:InputImg.shape[0] - InputImg.shape[0]%int(Tile), 0:InputImg.shape[1] - InputImg.shape[1]%int(Tile)]

	ComputeDifferences(InputImg, Library, int(Tile), OutputImageFile)

if __name__ == "__main__":
    main()