import FWCore.ParameterSet.Config as cms

process = cms.Process("DPSAnalysisRootFile")
process.load('FWCore.MessageService.MessageLogger_cfi')
##-------------------- Communicate with the DB -----------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.GlobalTag.globaltag = cms.string('FT_R_38X_V14A')
#process.GlobalTag.globaltag = cms.string('GR_R_38X_V13::All')
#process.GlobalTag.globaltag = cms.string('GR_R_311_V4::All')
process.GlobalTag.globaltag = cms.string('FT_R_42_V10A::All')
#process.GlobalTag.globaltag = cms.string('GR_R_42_V19::All')

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

#process.load('JetMETCorrections.Configuration.DefaultJEC_cff')

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
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
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/photon_DATA_2010/EG/Run2010A-Dec22ReReco_v1/RECO/2010data_EG_1_2_C3T.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/Photon/Run2010B-Apr21ReReco-v1/AOD/mycopy_4_1_8tL.root')
                            #fileNames = cms.untracked.vstring('rfio:/castor/cern.ch/user/l/lucaroni/PerLucia/step2_RAW2DIGI_L1Reco_RECO_VALIDATION_1_1_PwA.root')
			    fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/photon_root/EG/Run2010A-Dec22ReReco_v1/AOD/mycopy_1_1_An3.root')

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
debugOn = cms.untracked.bool(True),
numtrack = cms.untracked.uint32(10),
thresh = cms.untracked.double(0.25)
)

#HLT
#process.load('HLTrigger/HLTfilters/triggerResultsFilter_cfi')
#import HLTrigger.HLTfilters.hltHighLevel_cfi

#process.HLTrigger =cms.EDFilter("HLTHighLevel",
#     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
#     HLTPaths = cms.vstring('HLT_Photon50_Cleaned_L1R','HLT_Photon50_Cleaned_L1R_v1'),           # provide list of HLT paths (or patterns) you want
#     eventSetupPathsKey = cms.string(''), # not empty => use read paths from AlCaRecoTriggerBitsRcd via this key
#     andOr = cms.bool(True),  # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
#     throw = cms.bool(False)    # throw exception on unknown path names
# )


#from JetMETCorrections.Configuration.JetCorrectionServices_cff import *
#process.load("JetMETCorrections.Configuration.JetCorrectionServices_cff")
#process.load("CondCore.DBCommon.CondDBCommon_cfi")
#from CondCore.DBCommon.CondDBSetup_cfi import *

process.L1L2L3CorJetAK5PF = cms.EDProducer("PFJetCorrectionProducer",
   src = cms.InputTag("ak5PFJets"),
   correctors = cms.vstring('ak5PFL1L2L3Residual')     #for 2010data
)

process.genParticles.abortOnUnknownPDGCode = cms.untracked.bool(False)

process.goodvertex=cms.Path(process.primaryVertexFilter+process.noscraping)

process.p1 = cms.Sequence((process.UEAnalysisTracks
                      #*process.UEAnalysisJetsOnlyReco
                      *process.UEAnalysisPFJets
                      #+process.genEventKTValue
                      +process.DPSAnalysis))
#process.goodvertex=cms.Path(process.HLTrigger*(process.primaryVertexFilter+process.noscraping)*process.L1L2L3CorJetAK5PF*process.p1)
process.goodvertex=cms.Path((process.primaryVertexFilter+process.noscraping)*process.L1L2L3CorJetAK5PF*process.p1)
#process.goodvertex=cms.Path((process.primaryVertexFilter+process.noscraping)*process.L1L2L3CorJetAK5PF*process.DPSAnalysis)

process.DPSAnalysisRootple.OnlyRECO  = True
process.DPSAnalysisRootple.IsMC = False
process.DPSAnalysisRootple.IsDATA = True
process.DPSAnalysisRootple.Have_PILEUP = False

process.DPSAnalysisRootple.PFJetCollectionName       = 'L1L2L3CorJetAK5PF'
