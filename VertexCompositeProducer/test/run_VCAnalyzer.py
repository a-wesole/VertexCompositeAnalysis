#this is to analyze skimmed EDM
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
process = cms.Process('ANASKIM', eras.Run3_2023) #define the processes to be anaylzer - purpose to analyze outputted edm file and create ttree

# Load standard sequences and services same as org code
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')


# Set the global tag - not sure if needed 
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '132X_dataRun3_Prompt_v7'  # Adjust if necessary




# Add trigger selection
import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltFilter.andOr = cms.bool(True)
process.hltFilter.throw = cms.bool(False)
process.hltFilter.HLTPaths = [
    "HLT_HIMinimumBiasHF1AND_v*", #24
    "HLT_HIMinimumBiasHF1ANDZDC2nOR_v*", #25
    "HLT_HIMinimumBiasHF1ANDZDC1nOR_v*", #26
]


# Add PbPb collision event selection
process.load('VertexCompositeAnalysis.VertexCompositeProducer.collisionEventSelection_cff')
process.load('VertexCompositeAnalysis.VertexCompositeProducer.hfCoincFilter_cff')
process.load('VertexCompositeAnalysis.VertexCompositeProducer.hffilter_cfi')
process.colEvtSel = cms.Sequence()

# Define the event selection sequence 
process.eventFilter_HM = cms.Sequence( 
    process.hltFilter 
)
process.eventFilter_HM_step = cms.Path( process.eventFilter_HM )

# Configure the message logger
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.cerr.threshold = 'INFO' #don't print excessive amount of info 
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True)) #prints a summary of the job at the end

# Define the input source
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('file:output.root')  # Use the EDM output file
    fileNames = cms.untracked.vstring('file:/eos/purdue/store/user/awesolek/D0Test/HIPhysicsRawPrime0/D0Test/250224_202852/0000/out100events_472.root'),  # Use the EDM output file
    #eventsToProcess = cms.untracked.VEventRange('1:1430:199505260')  # Replace with your specific run, lumi, event numbers

)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(50))  # Process all events -- currently 2 for debugging

# TFileService to save the output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string('analyzed_crabTest.root')
)



from VertexCompositeAnalysis.VertexCompositeProducer.PATAlgos_cff import changeToMiniAOD 

# Load and configure the analyzer
#process.load("VertexCompositeAnalysis.VertexCompositeAnalyzer.d0selector_cff")
process.load("VertexCompositeAnalysis.VertexCompositeAnalyzer.d0analyzer_tree_cff") #for d0ana tree
process.load("VertexCompositeAnalysis.VertexCompositeAnalyzer.eventinfotree_cff") #for eventInfo tree 
#process.load("VertexCompositeAnalysis.VertexCompositeProducer.generalD0Candidates_cff")



# Configure the analyzer



process.d0ana = process.d0ana.clone()

process.d0ana.VertexCompositeCollection = cms.untracked.InputTag("d0selectorNewReduced:D0") #get the D0 collection from the d0selectorNew Reduced module 
process.d0ana.DCAValCollection = cms.InputTag("d0selectorNewReduced:DCAValuesNewD0")
process.d0ana.DCAErrCollection = cms.InputTag("d0selectorNewReduced:DCAErrorsNewD0")
#process.d0ana.doGenNtuple = cms.untracked.bool(True) #MConly
#process.d0ana.doGenMatching = cms.untracked.bool(True) #MConly

process.d0ana_seq2 = cms.Sequence( process.d0ana) #no MH filter or selector those are already ran

 #eventinfoana must be in EndPath, and process.eventinfoana.selectEvents must be the name of eventFilter_HM Path
process.eventinfoana.selectEvents = cms.untracked.string('eventFilter_HM_step')
process.eventinfoana.triggerPathNames = cms.untracked.vstring(
    "HLT_HIMinimumBiasHF1AND_v*", #24
    "HLT_HIMinimumBiasHF1ANDZDC2nOR_v", #25
    "HLT_HIMinimumBiasHF1ANDZDC1nOR_v", #26
    )
process.eventinfoana.eventFilterNames = cms.untracked.vstring(
    'Flag_colEvtSel',
    'Flag_hfCoincFilter',
    'Flag_primaryVertexFilter',
    )
process.eventinfoana.triggerFilterNames = cms.untracked.vstring()
process.eventinfoana.stageL1Trigger = cms.uint32(2)
process.pevt = cms.EndPath(process.eventinfoana)





# Define the process path
process.p = cms.Path(process.d0ana_seq2)

# Schedule the process
process.schedule = cms.Schedule(
        process.eventFilter_HM_step,
        process.p,
        process.pevt)

# Add the event selection filters
process.Flag_colEvtSel = cms.Path(process.colEvtSel)
#####Abbyprocess.Flag_colEvtSel = cms.Path(process.eventFilter_HM * process.colEvtSel)
#process.Flag_hfCoincFilter = cms.Path(process.eventFilter_HM * process.hfCoincFilter2Th4)
process.Flag_primaryVertexFilter = cms.Path(process.primaryVertexFilter * process.clusterCompatibilityFilter)
#####Abbyprocess.Flag_primaryVertexFilter = cms.Path(process.eventFilter_HM * process.primaryVertexFilter * process.clusterCompatibilityFilter)
# follow the exactly same config of process.eventinfoana.eventFilterNames
#eventFilterPaths = [ process.Flag_colEvtSel , process.Flag_hfCoincFilter , process.Flag_primaryVertexFilter ]
eventFilterPaths = [ process.Flag_colEvtSel  , process.Flag_primaryVertexFilter ]
for P in eventFilterPaths:
    process.schedule.insert(0, P)

changeToMiniAOD(process)
process.options.numberOfThreads = 1


# Output module, if needed
# process.output = cms.OutputModule("PoolOutputModule",
#     fileName = cms.untracked.string('final_output.root'),
#     outputCommands = cms.untracked.vstring(
#         "drop *",
#         "keep *_*_*_ANALYZER"
#     )
# )
# process.outputPath = cms.EndPath(process.output)

