from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
config = config()

config.General.requestName = ''
config.General.workArea = 'output_files'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../dfinder/forest_miniAOD_112X_DATA_wDfinder.py'
config.JobType.inputFiles = ['../dfinder/CentralityTable_HFtowers200_DataPbPb_periHYDJETshape_run3v1302x04_offline_Nominal.db','../dfinder/HeavyIonRPRcd_offline.db']
#config.JobType.maxJobRuntimeMin = 350 
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '' 
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 2 
config.Data.lumiMask = ''
#config.Data.runRange = '193093-193999' # '193093-194075'
config.Data.outLFNDirBase = '/store/user/mstojano/Lc_vn' 
config.Data.publication = False
config.Data.outputDatasetTag = 'Lc_Phys1'

config.Site.storageSite = 'T2_US_Purdue'
#config.Site.ignoreGlobalBlacklist = True
