import math
from operator import itemgetter

def csv(fileName):
	csvFile = open(fileName)
	contentLines = csvFile.readlines()
	csvFile.close()	
	for i in range(len(contentLines)):
		contentLines[i] = contentLines[i].split(",")
		j = len(contentLines[i]) - 1
		contentLines[i][j] = contentLines[i][j].replace("\n", "")			
	return contentLines

def txt(fileName):
	txtFile = open(fileName)
	contentLines = txtFile.readlines();
	txtFile.close()
	return contentLines

def distance(p, q): return math.sqrt((float(p[0]) - float(q[0]))**2 + (float(p[1]) - float(q[1]))**2 + (float(p[2]) - float(q[2]))**2 + (float(p[3]) - float(q[3]))**2)

def near(k, flower, flowers):
	nearbyFlowers = []
	for i in range(len(flowers)):		
		nearbyFlowers.append([distance(flower, flowers[i]), i, int(flowers[i][4])])
	nearbyFlowers.sort()
	return nearbyFlowers[:k]

def classify(nearbyFlowers):
	dic = {}
	for i in nearbyFlowers:
		if(not(dic.has_key(i[2]))):
			dic[i[2]] = 0
		dic[i[2]] =  dic[i[2]] + 1
	return sorted(dic.items(), key=itemgetter(1), reverse=True)[0][0]
	
def knn(k, flower, flowerTreining):
	nearbyFlowers = near(k, flower, flowerTreining)
	return classify(nearbyFlowers)

def best_K(flowerTest, labelTest, flowerTreining):	
	flowers = flowerTest
	bestK = 1
	maxRightResults = 0
	for k in range(1, len(flowers)+1):
		rightResults = 0
		for i in range(len(flowers)):			
			if knn(k, flowers[i], flowerTreining) == int(labelTest[i]):
				rightResults += 1
		if(maxRightResults < rightResults):
			maxRightResults = rightResults
			bestK = k
	return bestK, maxRightResults, len(flowers)

# main

def main():
	flowerTreining = csv("treining.csv")[1:]
	flowerTest = csv("test.csv")[1:]
	labelTest = txt("label-test.txt")		

	k = 1 # print best_K(flowerTest, labelTest, flowerTreining)[0]

	resultFile = open("result.txt", 'w')	
	for i in range(len(flowerTest)):		
		resultFile.write(str(knn(k, flowerTest[i], flowerTreining)) + ("" if i == len(flowerTest)-1 else "\n"))
	resultFile.close()
	
	labelResult = txt("result.txt")
		
	rightResults = 0

	for i in range(len(labelTest)):
		if (labelTest[i] == labelResult[i]):
			rightResults += 1

	print "Artificial Intelligence - KNN implementation - Joao Helis Bernardo"
	print "\nK =",k
	print str(float(rightResults)/len(labelResult)*100)+"% correct."	
	print rightResults, "of", len(labelResult), "right results.\n"

main()