from gold.learn.ModelEvaluator import ModelEvaluator
from gold.learn.trainer import MoveTrainer
from gold.learn.Model import ModelBuilder
from gold.learn.Model import Model

temp = ModelBuilder(["working_data/latest/trainfeaturesBtL.csv"],1)
temp.downSample()
temp.buildScaler("working_data/models/trainfeaturesBtLScaler.txt")
temp.scaleData()
#temp.buildFeatureSelector("working_data/models/BtLFeatureSelector.txt",120)
#temp.setFeaturesFromSelector("working_data/models/BtLFeatureSelector.txt")
#temp.selectFeatures()
#temp.buildModelAdaBoost("working_data/models/modelRF100BtL.txt")
temp.buildModelRF("working_data/models/modelRF100BtL.txt",301,20,3,1)
temp.setData(["working_data/latest/devfeaturesBtL.csv"],1)
temp.setScaler("working_data/models/trainfeaturesBtLScaler.txt")
temp.scaleData()
#temp.setFeaturesFromSelector("working_data/models/BtLFeatureSelector.txt")
#temp.selectFeatures()

print temp.evaluateModel("working_data/models/modelRF100BtL.txt")

temp = ModelBuilder(["working_data/latest/trainfeaturesWtK.csv"],1)
temp.downSample()
temp.buildScaler("working_data/models/trainfeaturesWtKScaler.txt")
temp.scaleData()
#temp.buildFeatureSelector("working_data/models/WtKFeatureSelector.txt",120)
#temp.setFeaturesFromSelector("working_data/models/WtKFeatureSelector.txt")
#temp.selectFeatures()
#temp.buildModelAdaBoost("working_data/models/modelRF100WtK.txt")
temp.buildModelRF("working_data/models/modelRF100Wtk.txt",301,20,3,1)
temp.setData(["working_data/latest/devfeaturesWtK.csv"],1)
temp.setScaler("working_data/models/trainfeaturesWtKScaler.txt")
temp.scaleData()
#temp.setFeaturesFromSelector("working_data/models/WtKFeatureSelector.txt")
#temp.selectFeatures()
print temp.evaluateModel("working_data/models/modelRF100WtK.txt")