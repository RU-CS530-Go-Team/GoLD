import sys
sys.path.append("/Users/zacharydaniels/Documents/GoLD/src/")
from gold.learn.Model import ModelBuilder
from gold.learn.Model import Model

bestMeasure = 0
bestClass1Weight = 1
bestClass0Weight = 1

training = "extraneous/games/terminal/trainfeaturesBtL_T.csv"
test = "extraneous/games/terminal/devfeaturesBtL_T.csv"

temp = ModelBuilder([training],1)
temp.buildScaler("extraneous/games/train/scaler.txt")
temp.scaleData()

temp2 = ModelBuilder([test],1)
temp2.setScaler("extraneous/games/train/scaler.txt")
temp2.scaleData()

for class1Weight in range(1,20):
  for class0Weight in range(1,2):
    print "(" + str(class1Weight) + "," + str(class0Weight) + ")\n"
    temp.buildModelSVM("extraneous/games/train/model.txt",weights={1:class1Weight,0:class0Weight})
    data = temp2.evaluateModel("extraneous/games/train/model.txt")
    if data[2] > bestMeasure:
      bestMeasure = data[2]
      bestClass1Weight = class1Weight
      bestClass0Weight = class0Weight
      print "Measure: " + str(bestMeasure) + ", Class 1 Weight: " + str(bestClass1Weight) + ", Class 0 Weight: " + str(bestClass0Weight) + "\n"

print "[Final] Measure: " + str(bestMeasure) + ", Class 1 Weight: " + str(bestClass1Weight) + ", Class 0 Weight: " + str(bestClass0Weight) + "\n"
