from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
config = config()

config.General.requestName = 'dataTTree'
config.General.workArea = 'D0_data_TTree'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/home/awesole/VertexCP_clean/CMSSW_13_2_11/src/VertexCompositeAnalysis/VertexCompositeProducer/test/run_VCAnalyzer_DATA.py'
config.JobType.allowUndistributedCMSSW = True
#config.JobType.maxMemoryMB = 4500

config.Data.inputDataset = '/HIPhysicsRawPrime0/awesolek-D0_DATA_Run3_publish-34b1f9f465ba57acd9888389eb7f7106/USER' 
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1 
config.Data.lumiMask = 'mini2.json'
#for part of dataset0
config.Data.outputPrimaryDataset = 'D0_data_TTrees'
config.Data.outLFNDirBase = '/store/user/wxie/D0_data_TTrees' 
config.Data.publication = True
config.Data.outputDatasetTag = 'D0_DATA_Run3_TTree'

config.Site.storageSite = 'T2_US_Purdue'
#config.Site.ignoreGlobalBlacklist = True
