from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
config = config()

config.General.requestName = 'partial_HIPhysicsRawPrime0_publish'
config.General.workArea = 'D0_DATA_Run3_publish'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../run_VCProducer_Data.py'
config.JobType.allowUndistributedCMSSW = True
#config.JobType.maxMemoryMB = 4500

config.Data.inputDataset = '/HIPhysicsRawPrime0/HIRun2023A-PromptReco-v2/MINIAOD' 
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 2 
config.Data.lumiMask = 'mini2.json'
#for part of dataset0
config.Data.outLFNDirBase = '/store/user/awesolek/D0_DATA_Run3_publish' 
config.Data.publication = True
config.Data.outputDatasetTag = 'D0_DATA_Run3_publish'

config.Site.storageSite = 'T2_US_Purdue'
#config.Site.ignoreGlobalBlacklist = True
