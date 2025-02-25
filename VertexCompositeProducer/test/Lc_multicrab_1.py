from CRABClient.UserUtilities import config #, getUsernameFromSiteDB
config = config()

config.General.requestName = ''
config.General.workArea = 'output_files'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
#config.JobType.psetName = '../dfinder/forest_miniAOD_112X_DATA_wDfinder.py'
config.JobType.psetName = '/home/awesole/VertexCP_clean/CMSSW_13_2_11/src/VertexCompositeAnalysis/VertexCompositeProducer/test/run_VCProducer.py'
#config.JobType.inputFiles = ['../dfinder/CentralityTable_HFtowers200_DataPbPb_periHYDJETshape_run3v1302x04_offline_Nominal.db','../dfinder/HeavyIonRPRcd_offline.db'] extra files if needed
#config.JobType.maxJobRuntimeMin = 350 
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/HIPhysicsRawPrime0/HIRun2023A-PromptReco-v2/MINIAOD' #add as many as necesary from https://cmsweb.cern.ch/das/
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 1 #as low as possible probably not more than 3 
config.Data.lumiMask = '' #only golden sections
#config.Data.runRange = '193093-193999' # '193093-194075'
config.Data.outLFNDirBase = '/store/user/awesole/D0_output' 
config.Data.publication = False
config.Data.outputDatasetTag = 'Lc_Phys1'

config.Site.storageSite = 'T2_US_Purdue'
#config.Site.ignoreGlobalBlacklist = True
