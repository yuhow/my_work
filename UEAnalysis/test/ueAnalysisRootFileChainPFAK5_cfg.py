import FWCore.ParameterSet.Config as cms

process = cms.Process("MBUEAnalysisRootFile")
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



process.TFileService = cms.Service("TFileService",
    #fileName = cms.string('MBUEAnalysisRootFile.root')
    fileName = cms.string('MBUEAnalysisRootFile.root')
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
			    #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/photon_root/G_Pt_50to80_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO/mycopy_1_1_eN7.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/step2_RAW2DIGI_L1Reco_RECO_VALIDATION_1_1_PwA.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/step2_RAW2DIGI_L1Reco_RECO.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_9_1_xxS.root')
			    #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/photon_root/G_Pt-50to80_TuneZ2_7TeV_pythia6/Summer11-PU_S4_START42_V11-v1/AODSIM/mycopy_1_3_OYA.root')
                            fileNames = cms.untracked.vstring(
                            'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_1.root',
                            #'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_2.root',
                            #'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_3.root',
                            #'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_4.root',
                            #'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_5.root',
                            #'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_6.root',
                            #'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_7.root',
                            #'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_8.root',
                            #'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_9.root',
                            #'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_PU_BS_CMSSW425/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_PU_10.root',
 )
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


##TrackJet
process.ueAntiKt5TracksJet.jetPtMin = cms.double(0.9)
process.ueAntiKt5TracksJet500.jetPtMin = cms.double(0.5)
process.ueAntiKt5TracksJet700.jetPtMin = cms.double(0.7)
process.ueAntiKt5TracksJet1500.jetPtMin = cms.double(1.5)
process.ueAntiKt5TracksJet1100.jetPtMin = cms.double(1.1)


process.ueAntiKt5TracksJet.UseOnlyOnePV = cms.bool(True)
process.ueAntiKt5TracksJet.UseOnlyVertexTracks = cms.bool(False)
process.ueAntiKt5TracksJet.DzTrVtxMax = cms.double(999999.)
process.ueAntiKt5TracksJet.DxyTrVtxMax = cms.double(999999.)
process.ueAntiKt5TracksJet500.UseOnlyOnePV = cms.bool(True)
process.ueAntiKt5TracksJet500.UseOnlyVertexTracks = cms.bool(False)
process.ueAntiKt5TracksJet500.DzTrVtxMax = cms.double(999999.)
process.ueAntiKt5TracksJet500.DxyTrVtxMax = cms.double(999999.)
process.ueAntiKt5TracksJet1500.UseOnlyOnePV = cms.bool(True)
process.ueAntiKt5TracksJet1500.UseOnlyVertexTracks = cms.bool(False)
process.ueAntiKt5TracksJet1500.DzTrVtxMax = cms.double(999999.)
process.ueAntiKt5TracksJet1500.DxyTrVtxMax = cms.double(999999.)
process.ueAntiKt5TracksJet1100.UseOnlyOnePV = cms.bool(True)
process.ueAntiKt5TracksJet1100.UseOnlyVertexTracks = cms.bool(False)
process.ueAntiKt5TracksJet1100.DzTrVtxMax = cms.double(999999.)
process.ueAntiKt5TracksJet1100.DxyTrVtxMax = cms.double(999999.)
process.ueAntiKt5TracksJet700.UseOnlyOnePV = cms.bool(True)
process.ueAntiKt5TracksJet700.UseOnlyVertexTracks = cms.bool(False)
process.ueAntiKt5TracksJet700.DzTrVtxMax = cms.double(999999.)
process.ueAntiKt5TracksJet700.DxyTrVtxMax = cms.double(999999.)

process.L1L2L3CorJetAK5PF = cms.EDProducer("PFJetCorrectionProducer",
   src = cms.InputTag("ak5PFJets"),
   correctors = cms.vstring('ak5PFL1L2L3')     #for MC
)

##PFJet
#process.ueAntiKt5PFJet.jetPtMin = cms.double(0.9)
#process.ueAntiKt5PFJet500.jetPtMin = cms.double(0.5)
#process.ueAntiKt5PFJet700.jetPtMin = cms.double(0.7)
#process.ueAntiKt5PFJet1500.jetPtMin = cms.double(1.5)
#process.ueAntiKt5PFJet1100.jetPtMin = cms.double(1.1)
#
#
#process.ueAntiKt5PFJet.UseOnlyOnePV = cms.bool(True)
#process.ueAntiKt5PFJet.UseOnlyVertexTracks = cms.bool(False)
#process.ueAntiKt5PFJet.DzTrVtxMax = cms.double(999999.)
#process.ueAntiKt5PFJet.DxyTrVtxMax = cms.double(999999.)
#process.ueAntiKt5PFJet500.UseOnlyOnePV = cms.bool(True)
#process.ueAntiKt5PFJet500.UseOnlyVertexTracks = cms.bool(False)
#process.ueAntiKt5PFJet500.DzTrVtxMax = cms.double(999999.)
#process.ueAntiKt5PFJet500.DxyTrVtxMax = cms.double(999999.)
#process.ueAntiKt5PFJet1500.UseOnlyOnePV = cms.bool(True)
#process.ueAntiKt5PFJet1500.UseOnlyVertexTracks = cms.bool(False)
#process.ueAntiKt5PFJet1500.DzTrVtxMax = cms.double(999999.)
#process.ueAntiKt5PFJet1500.DxyTrVtxMax = cms.double(999999.)
#process.ueAntiKt5PFJet1100.UseOnlyOnePV = cms.bool(True)
#process.ueAntiKt5PFJet1100.UseOnlyVertexTracks = cms.bool(False)
#process.ueAntiKt5PFJet1100.DzTrVtxMax = cms.double(999999.)
#process.ueAntiKt5PFJet1100.DxyTrVtxMax = cms.double(999999.)
#process.ueAntiKt5PFJet700.UseOnlyOnePV = cms.bool(True)
#process.ueAntiKt5PFJet700.UseOnlyVertexTracks = cms.bool(False)
#process.ueAntiKt5PFJet700.DzTrVtxMax = cms.double(999999.)
#process.ueAntiKt5PFJet700.DxyTrVtxMax = cms.double(999999.)


process.genParticles.abortOnUnknownPDGCode = cms.untracked.bool(False)

process.goodvertex=cms.Path(process.primaryVertexFilter+process.noscraping)

process.p1 = cms.Sequence((process.UEAnalysisTracks
                      #*process.UEAnalysisJets
                      *process.UEAnalysisPFJets
                      #+process.genEventKTValue
                      +process.UEAnalysis))
#process.L1T1collpath=cms.Path(process.L1T1coll*process.p1)
process.goodvertex=cms.Path((process.primaryVertexFilter+process.noscraping)*process.L1L2L3CorJetAK5PF*process.p1)

process.UEAnalysisRootple.OnlyRECO     = False 
process.UEAnalysisRootple500.OnlyRECO  = False
process.UEAnalysisRootple1500.OnlyRECO = False
process.UEAnalysisRootple700.OnlyRECO  = False
process.UEAnalysisRootple1100.OnlyRECO = False


process.UEAnalysisRootple.GenJetCollectionName      = 'ueAntiKt5GenJet'
process.UEAnalysisRootple.ChgGenJetCollectionName   = 'ueAntiKt5ChgGenJet'
process.UEAnalysisRootple.TracksJetCollectionName   = 'ueAntiKt5TracksJet'
process.UEAnalysisRootple.RecoCaloJetCollectionName = 'ak5CaloJets'
process.UEAnalysisRootple.PFJetCollectionName       = 'ueAntiKt5PFJet'
#process.UEAnalysisRootple500.GenJetCollectionName      = 'ueAntiKt5GenJet500'
#process.UEAnalysisRootple500.ChgGenJetCollectionName   = 'ueAntiKt5ChgGenJet500'
#process.UEAnalysisRootple500.TracksJetCollectionName   = 'ueAntiKt5TracksJet500'
process.UEAnalysisRootple500.RecoCaloJetCollectionName = 'ak5CaloJets'
#process.UEAnalysisRootple500.PFJetCollectionName       = 'ueAntiKt5PFJet500'
process.UEAnalysisRootple500.PFJetCollectionName       = 'L1L2L3CorJetAK5PF'
process.UEAnalysisRootple1500.GenJetCollectionName      = 'ueAntiKt5GenJet1500'
process.UEAnalysisRootple1500.ChgGenJetCollectionName   = 'ueAntiKt5ChgGenJet1500'
process.UEAnalysisRootple1500.TracksJetCollectionName   = 'ueAntiKt5TracksJet1500'
process.UEAnalysisRootple1500.RecoCaloJetCollectionName = 'ak5CaloJets'
process.UEAnalysisRootple1500.PFJetCollectionName       = 'ueAntiKt5PFJet1500'
process.UEAnalysisRootple1100.GenJetCollectionName      = 'ueAntiKt5GenJet1100'
process.UEAnalysisRootple1100.ChgGenJetCollectionName   = 'ueAntiKt5ChgGenJet1100'
process.UEAnalysisRootple1100.TracksJetCollectionName   = 'ueAntiKt5TracksJet1100'
process.UEAnalysisRootple1100.RecoCaloJetCollectionName = 'ak5CaloJets'
process.UEAnalysisRootple1100.PFJetCollectionName       = 'ueAntiKt5PFJet1100'
process.UEAnalysisRootple700.GenJetCollectionName      = 'ueAntiKt5GenJet700'
process.UEAnalysisRootple700.ChgGenJetCollectionName   = 'ueAntiKt5ChgGenJet700'
process.UEAnalysisRootple700.TracksJetCollectionName   = 'ueAntiKt5TracksJet700'
process.UEAnalysisRootple700.RecoCaloJetCollectionName = 'ak5CaloJets'
process.UEAnalysisRootple700.PFJetCollectionName       = 'ueAntiKt5PFJet700'



#/// Pythia: genEventScale = cms.InputTag("genEventScale")
#/// Herwig: genEventScale = cms.InputTag("genEventKTValue")
#process.UEAnalysisRootple.genEventScale     = 'genEventKTValue'
#process.UEAnalysisRootple500.genEventScale  = 'genEventKTValue'
#process.UEAnalysisRootple1500.genEventScale = 'genEventKTValue'


