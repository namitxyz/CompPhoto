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

	return red_hist, grn_hist, blu_hist

def ComputeDifferences(InputImg, Library, Tile, OutputImageFile):

	rows = InputImg.shape[0]
	cols = InputImg.shape[1]

	for i in range(0, rows/Tile):
		for j in range(0, cols/Tile):
			SingleTileImg = InputImg[i * Tile:(i + 1) * Tile, j * Tile:(j + 1) * Tile]
			Red_Tile, Green_Tile, Blue_Tile = FindAverage(SingleTileImg)

			heap = []

			for key in Library.keys():
				Red_lib = Library[key][0]
				Green_lib = Library[key][1]
				Blue_lib = Library[key][2]

				#change the value of method from 0 to 4 to test different comparison functions
				red_diff   = cv2.compareHist(Red_Tile, Red_lib, method = 4)
				green_diff = cv2.compareHist(Green_Tile, Green_lib, method = 4)
				blue_diff  = cv2.compareHist(Blue_Tile, Blue_lib, method = 4)

				MeanSquare = 1*(red_diff + green_diff + blue_diff)
				heapq.heappush(heap, (MeanSquare, key))


			InputImg[i * Tile:(i + 1) * Tile, j * Tile:(j + 1) * Tile] = Library[heap[0][1]][3]


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
		Library[img] = [Red, Green, Blue, Libimage]

	InputImg = InputImg[0:InputImg.shape[0] - InputImg.shape[0]%int(Tile), 0:InputImg.shape[1] - InputImg.shape[1]%int(Tile)]

	ComputeDifferences(InputImg, Library, int(Tile), OutputImageFile)

if __name__ == "__main__":
    main()