import FWCore.ParameterSet.Config as cms

process = cms.Process("DPSAnalysisRootFile")
process.load('FWCore.MessageService.MessageLogger_cfi')
##-------------------- Communicate with the DB -----------------------
process.load('Configuration.StandardSequences.Services_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.GlobalTag.globaltag = cms.string('MC_3XY_V20::All')
#process.GlobalTag.globaltag = cms.string('MC_41_V0::All')
#process.GlobalTag.globaltag = cms.string('MC_42_V13::All')
#process.GlobalTag.globaltag = cms.string('START38_V12::All')
#process.GlobalTag.globaltag = cms.string('START42_V10::All')

process.load("QCDAnalysis.UEAnalysis.UEAnalysisParticles_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisJetsAntiKt_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisRootpleOnlyMC_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.threshold = cms.untracked.string('INFO')

process.TFileService = cms.Service("TFileService",
    #fileName = cms.string('MBUEAnalysisRootFile.root')
    fileName = cms.string('DPSAnalysisRootFile.root')
)

process.MessageLogger = cms.Service("MessageLogger",
    #cerr = cms.untracked.PSet(
    #    default = cms.untracked.PSet(
    #        limit = cms.untracked.int32(10)
    #    )
    #),
    cout = cms.untracked.PSet(
#        threshold = cms.untracked.string('ERROR')
        threshold = cms.untracked.string('DEBUG')
    ),
    destinations = cms.untracked.vstring('cout')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    #skipEvent = cms.untracked.vstring('ProductNotFound')
    #input = cms.untracked.int32(-1)
)
process.source = cms.Source("PoolSource",
   duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/pcntu10_work/G_Pt-170to300_Tune23_7TeV_herwigpp/FE0A4CD4-657F-E011-8B32-002481E0DC82.root')
    fileNames = cms.untracked.vstring(
'file:/wk1/yuhow/pcntu10_work/QCD_Pt-600to800_Tune23_HFshowerLibrary_7TeV_herwigpp/34A0597D-A47B-E211-95AA-002481A60370.root',
'file:/wk1/yuhow/pcntu10_work/QCD_Pt-600to800_Tune23_HFshowerLibrary_7TeV_herwigpp/3EA11A2B-AD7B-E211-8493-1CC1DE1D2028.root',
'file:/wk1/yuhow/pcntu10_work/QCD_Pt-600to800_Tune23_HFshowerLibrary_7TeV_herwigpp/B495E222-AB7B-E211-B85C-0017A4770428.root',
'file:/wk1/yuhow/pcntu10_work/QCD_Pt-600to800_Tune23_HFshowerLibrary_7TeV_herwigpp/B8C31CD0-AA7B-E211-B434-00266CFFBDAC.root',
'file:/wk1/yuhow/pcntu10_work/QCD_Pt-600to800_Tune23_HFshowerLibrary_7TeV_herwigpp/CA34A874-847B-E211-865A-0017A4770408.root',
'file:/wk1/yuhow/pcntu10_work/QCD_Pt-600to800_Tune23_HFshowerLibrary_7TeV_herwigpp/E6A02681-807B-E211-B219-00266CFEFC5C.root'
)

)

process.genParticles.abortOnUnknownPDGCode = cms.untracked.bool(False)

process.p1 = cms.Path((process.DPSAnalysisOnlyMC))

