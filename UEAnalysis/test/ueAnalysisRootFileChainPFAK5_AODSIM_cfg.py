import FWCore.ParameterSet.Config as cms

process = cms.Process("DPSAnalysisRootFile")
process.load('FWCore.MessageService.MessageLogger_cfi')
##-------------------- Communicate with the DB -----------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.GlobalTag.globaltag = cms.string('MC_3XY_V20::All')
#process.GlobalTag.globaltag = cms.string('MC_41_V0::All')
#process.GlobalTag.globaltag = cms.string('MC_42_V13::All')
#process.GlobalTag.globaltag = cms.string('START38_V12::All')
process.GlobalTag.globaltag = cms.string('START42_V10::All')

process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Geometry_cff')
process.load('RecoJets.Configuration.RecoPFJets_cff')
process.load('RecoJets.Configuration.RecoJets_cff')
process.load("JetMETCorrections.Configuration.JetCorrectionServices_cff")

process.load("QCDAnalysis.UEAnalysis.UEAnalysisParticles_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisTracks_cfi")
#process.load("QCDAnalysis.UEAnalysis.UEAnalysisJetsSISCone_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisJetsAntiKt_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisJetsPFAntiKt_cfi")
#process.load("PhysicsTools.HepMCCandAlgos.genEventKTValue_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisRootple_cfi")

# ########### Channel Status and Severity Level !!! #########
process.load("RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.threshold = cms.untracked.string('INFO')

process.TFileService = cms.Service("TFileService",
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
                            #fileNames = cms.untracked.vstring('file:/nasdata/cmsdata/MinBias_START3X_V26A_357ReReco-v3_3EE4E026-7C50-DF11-9F0F-002354EF3BD0.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/photon_root/PhotonJet_Pt15/Summer10-START36_V9_S09-v1/GEN-SIM-RECODEBUG/mycopy_1_1_ED6.root')
			    #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/photon_root/G_Pt-50to80_TuneZ2_7TeV_pythia6/Summer11-PU_S4_START42_V11-v1/AODSIM/mycopy_1_3_OYA.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/step2_RAW2DIGI_L1Reco_RECO_VALIDATION_1_1_PwA.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/step2_RAW2DIGI_L1Reco_RECO.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_9_1_xxS.root')
			    #fileNames = cms.untracked.vstring('file:/data10b/yuhow/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_1_1_gjo.root')
                            fileNames = cms.untracked.vstring('file:/wk1/yuhow/pcntu10_work/CMSSW_4_2_5/src/QCDAnalysis/UEAnalysis/test/G_Pt50To80_Tune4C_7TeV_pythia8_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_198_1_0rP.root')
)

#L1
#process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
#process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')

#process.L1T1coll=process.hltLevel1GTSeed.clone()
#process.L1T1coll.L1TechTriggerSeeding = cms.bool(True)
#process.L1T1coll.L1SeedsLogicalExpression = cms.string('(40 OR 41) AND NOT (36 OR 37 OR 38 OR 39) AND NOT ((42 AND NOT 43) OR (43 AND NOT 42))')

#process.L1T1collpath=cms.Path(process.L1T1coll)

#vertex
#process.primaryVertexFilter = cms.EDFilter("VertexSelector",
#   src = cms.InputTag("offlinePrimaryVertices"),
#   cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2"), # tracksSize() > 3 for the older cut
#   filter = cms.bool(True),   # otherwise it won't filter the events, just produce an empty vertex collection.
#)

process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
vertexCollection = cms.InputTag('offlinePrimaryVertices'),
minimumNDOF      = cms.uint32  (4),
maxAbsZ          = cms.double  (24.0), # this parameter
maxd0            = cms.double  (2.0),
)

process.noscraping = cms.EDFilter("FilterOutScraping",
applyfilter = cms.untracked.bool(True),
debugOn = cms.untracked.bool(False),
numtrack = cms.untracked.uint32(10),
thresh = cms.untracked.double(0.25)
)

#HLT
#process.load('HLTrigger/HLTfilters/triggerResultsFilter_cfi')
#import HLTrigger.HLTfilters.hltHighLevel_cfi

#process.HLTrigger =cms.EDFilter("HLTHighLevel",
#     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
#     HLTPaths = cms.vstring('HLT_Photon50_CaloIdVL_IsoL_v1'),           # provide list of HLT paths (or patterns) you want
#     eventSetupPathsKey = cms.string(''), # not empty => use read paths from AlCaRecoTriggerBitsRcd via this key
#     andOr = cms.bool(True),  # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
#     throw = cms.bool(False)    # throw exception on unknown path names
# )


process.L1L2L3CorJetAK5PF = cms.EDProducer("PFJetCorrectionProducer",
   src = cms.InputTag("ak5PFJets"),
   correctors = cms.vstring('ak5PFL1L2L3')     #for MC
)

process.genParticles.abortOnUnknownPDGCode = cms.untracked.bool(False)

process.goodvertex=cms.Path(process.primaryVertexFilter+process.noscraping)

process.p1 = cms.Sequence((process.UEAnalysisTracks
                      #*process.UEAnalysisJetsOnlyReco
                      *process.UEAnalysisPFJets
                      #+process.genEventKTValue
                      +process.DPSAnalysis))
process.goodvertex=cms.Path((process.primaryVertexFilter+process.noscraping)*process.L1L2L3CorJetAK5PF*process.p1)

process.DPSAnalysisRootple.OnlyRECO     = False 
process.DPSAnalysisRootple.IsMC = True
process.DPSAnalysisRootple.Is2010DATA = False
process.DPSAnalysisRootple.Is2011DATA = False
process.DPSAnalysisRootple.Have_PILEUP = True

process.DPSAnalysisRootple.PFJetCollectionName       = 'L1L2L3CorJetAK5PF'
