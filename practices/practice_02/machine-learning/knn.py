import math
from operator import itemgetter

labelTestFile = open("label-test.txt")
CSV_testFile = open("test.csv")
CSV_treiningFile = open("treining.csv")

flowerTreining = CSV_treiningFile.readlines()[1:]
flowerTest = CSV_testFile.readlines()[1:]
labelTest = labelTestFile.readlines()

labelTestFile.close()
CSV_testFile.close()
CSV_treiningFile.close()

for i in range(len(flowerTreining)):
	flowerTreining[i] = flowerTreining[i].split(",")
	for j in range(len(flowerTreining[i])):		
		flowerTreining[i][j] = float(flowerTreining[i][j].replace("\n", ""))

for i in range(len(flowerTest)):
	flowerTest[i] = flowerTest[i].split(",")
	for j in range(len(flowerTest[i])):				
		flowerTest[i][j] = float(flowerTest[i][j].replace("\n",""))

def distance(p, q): return math.sqrt((float(p[0]) - float(q[0]))**2 + (float(p[1]) - float(q[1]))**2 + float((p[2] - q[2]))**2 + float((p[3] - q[3])**2))

def near(k, flower, flowers):
	nearbyFlowers = []
	for i in range(len(flowers)):
		nearbyFlowers.append([distance(flower, flowers[i]), i, int(flowers[i][4])])
	nearbyFlowers.sort()
	return nearbyFlowers[1:k+1]

def classify(nearbyFlowers):
	dic = {}
	for i in nearbyFlowers:
		if(not(dic.has_key(i[2]))):
			dic[i[2]] = 0
		dic[i[2]] =  dic[i[2]] + 1
	return sorted(dic.items(), key=itemgetter(1), reverse=True)[0][0]
	
def knn(k, flower):
	nearbyFlowers = near(k, flower, flowerTreining)
	return classify(nearbyFlowers)

def getBest_K():	
	flowers = flowerTest
	bestK = 1
	maxRightResults = 0
	for k in range(1, len(flowers)+1):
		rightResults = 0
		for i in range(len(flowers)):			
			if knn(k, flowers[i]) == int(labelTest[i].replace("\n","")):
				rightResults += 1
		if(maxRightResults < rightResults):
			maxRightResults = rightResults
			bestK = k
	return bestK, maxRightResults

# main
#print getBest_K()

def main():
	k = 4

	resultFile = open("result.txt", 'w')	
	for i in range(len(flowerTest)):		
		resultFile.write(str(knn(k, flowerTest[i])) + ("" if i == len(flowerTest)-1 else "\n"))
	resultFile.close()

	resultFile = open("result.txt")
	labelResult = resultFile.readlines()
	resultFile.close()
		
	rightResults = 0

	for i in range(len(labelTest)):
		if (labelTest[i] == labelResult[i]):
			rightResults += 1

	print "Artificial Intelligence - KNN implementation - Joao Helis Bernardo"
	print "\nK =",k
	print str(float(rightResults)/len(labelResult)*100)+"% correct."	
	print rightResults, "of", len(labelResult), "right results.\n"

main()