import FWCore.ParameterSet.Config as cms 
from Configuration.StandardSequences.Eras import eras
process = cms.Process('MYTEST', eras.Run3_2023)

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')

# Limit the output messages
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Define the input source
infile = 'root://xrootd-cms.infn.it//store/mc/HINPbPbSpring23MiniAOD/promptD0ToKPi_PT-1_TuneCP5_5p36TeV_pythia8-evtgen/MINIAODSIM/132X_mcRun3_2023_realistic_HI_v9-v2/2560000/04335bea-a283-40ea-a050-d71e1b7fac6b.root' #mc file 

process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(infile),
)



process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10)) #CHANGE

# Set the global tag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string('132X_mcRun3_2023_realistic_HI_v9')

# =============== Import Sequences =====================
#Trigger Selection
### Comment out for the timing being assuming running on secondary dataset with trigger bit selected already
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

from VertexCompositeAnalysis.VertexCompositeProducer.PATAlgos_cff import changeToMiniAOD

# Define the analysis steps

########## D0 candidate rereco ###############################################################
process.load("VertexCompositeAnalysis.VertexCompositeProducer.generalD0Candidates_cff")
process.generalD0CandidatesNew = process.generalD0Candidates.clone()
process.generalD0CandidatesNew.trkPtSumCut = cms.double(2.0)
process.generalD0CandidatesNew.trkEtaDiffCut = cms.double(1.0)
process.generalD0CandidatesNew.tkNhitsCut = cms.int32(0)
process.generalD0CandidatesNew.tkPtErrCut = cms.double(0.1)
process.generalD0CandidatesNew.tkPtCut = cms.double(1.0)
process.generalD0CandidatesNew.alphaCut = cms.double(0.30)
process.generalD0CandidatesNew.alpha2DCut = cms.double(0.30)
process.generalD0CandidatesNew.dPtCut = cms.double(1.0)
process.generalD0CandidatesNew.VtxChiProbCut = cms.double(0.010)
process.generalD0CandidatesNew.mPiKCutMin = cms.double(1.74)
process.generalD0CandidatesNew.mPiKCutMax = cms.double(2.00)

process.d0rereco_step = cms.Path( process.generalD0CandidatesNew) #creates a new path 'd0rereco_step' will execute the generalD0candidates

# produce D0 trees
process.load("VertexCompositeAnalysis.VertexCompositeAnalyzer.d0selector_cff") #load the configuration file for d0slector 
process.load("VertexCompositeAnalysis.VertexCompositeAnalyzer.eventinfotree_cff")


# set up selectors
process.d0selector = process.d0selectorBDTPreCut.clone() #clones the BDT module
process.d0selector.useAnyMVA = cms.bool(False) #multivariable analysis
process.d0selector.multMin = cms.untracked.double(0) #multiplicity min
process.d0selector.multMax = cms.untracked.double(100000) #multiplicity max

process.d0selectorNewReduced = process.d0selector.clone() #clone of d0seector can be edited wihhout affecting og 
process.d0selectorNewReduced.DCAValCollection = cms.InputTag("generalD0CandidatesNew:DCAValuesD0") #need further investigating 
process.d0selectorNewReduced.DCAErrCollection = cms.InputTag("generalD0CandidatesNew:DCAErrorsD0") #need further investigating 
process.d0selectorNewReduced.cand3DDecayLengthSigMin = cms.untracked.double(0.) #precuts
process.d0selectorNewReduced.cand3DPointingAngleMax = cms.untracked.double(1.0) #precuts 

process.d0selectorWSNewReduced = process.d0selectorWS.clone() #for wrong sign 
process.d0selectorWSNewReduced.DCAValCollection = cms.InputTag("generalD0CandidatesNewWrongSign:DCAValuesD0")
process.d0selectorWSNewReduced.DCAErrCollection = cms.InputTag("generalD0CandidatesNewWrongSign:DCAErrorsD0")


process.d0ana_seq2 = cms.Sequence(process.eventFilter_HM * process.d0selectorNewReduced ) #sequence that first applies HM filter then d0 selector



process.p = cms.Path(process.d0ana_seq2) #path p that executes d0anasseq2

# Add the Conversion tree

# Define the process schedule
process.schedule = cms.Schedule( #scehule  sequence of paths that will be executed in particular oder 
    process.eventFilter_HM_step, #HighM
    process.d0rereco_step, #reco D0 mesons
    process.p, #execute d0ana_seq2
)

# Add the event selection filters
process.Flag_colEvtSel = cms.Path(process.colEvtSel) #collision event selection
process.Flag_primaryVertexFilter = cms.Path(process.primaryVertexFilter * process.clusterCompatibilityFilter) #more filters 
eventFilterPaths = [ process.Flag_colEvtSel  , process.Flag_primaryVertexFilter ] #two paths of event filters
for P in eventFilterPaths: #each path in event filters paths lits
    process.schedule.insert(0, P) #inserts each path at the beginning of the process.schedule, 0 means they will be executed first 

changeToMiniAOD(process) #use miniAOD format
process.options.numberOfThreads = 1 #single-threaded mode

process.output = cms.OutputModule("PoolOutputModule", #for writing output to a output file
    fileName = cms.untracked.string('output_withMC.root'), #name of file, untracked = not tracked in the job's history 
    outputCommands = cms.untracked.vstring( #which data to include and exclude 
        #"drop *", #no data is kept unless explicitly specified
        "keep *", #all data is kept 
        #"keep *_*_*_ANASKIM"
        #"keep *_*_*_MYTEST" #keep only the data processed within MYTEST *_*_*_ means keep all products from any module, instance and any label 
        )
)


process.outputPath = cms.EndPath(process.output)
process.schedule.append(process.outputPath)


process.options.numberOfThreads = 1
