from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
config = config()

config.General.requestName = ''
config.General.workArea = 'D0MC_Run3'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../run_VCProducer.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '' 
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1 
config.Data.lumiMask = ''
config.Data.outLFNDirBase = '/store/user/awesolek/D0MC_Run3' 
config.Data.publication = False
config.Data.outputDatasetTag = 'D0MC_run3'

config.Site.storageSite = 'T2_US_Purdue'
#config.Site.ignoreGlobalBlacklist = True
