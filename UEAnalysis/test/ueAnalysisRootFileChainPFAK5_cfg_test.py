import FWCore.ParameterSet.Config as cms

process = cms.Process("MBUEAnalysisRootFile")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisParticles_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisTracks_cfi")
#process.load("QCDAnalysis.UEAnalysis.UEAnalysisJetsSISCone_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisJetsAntiKt_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisJetsPFAntiKt_cfi")
#process.load("PhysicsTools.HepMCCandAlgos.genEventKTValue_cfi")
process.load("QCDAnalysis.UEAnalysis.UEAnalysisRootple_cfi")

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('MC_3XY_V20::All')
#process.GlobalTag.globaltag = cms.string('MC_41_V0::All')
process.GlobalTag.globaltag = cms.string('START41_V0::All')
#process.GlobalTag.globaltag = cms.string('START42_V10::ALL')
process.load("Configuration.StandardSequences.MagneticField_cff")

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
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/step2_RAW2DIGI_L1Reco_RECO_PAT.root')
                            #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_9_1_xxS.root')
			    #fileNames = cms.untracked.vstring('file:/nasdata2/yuhow/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT.root')
fileNames = cms.untracked.vstring(
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_100_1_fd9.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_10_1_10k.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_11_1_83D.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_12_1_wsO.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_13_1_P4k.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_14_1_c1k.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_15_1_qat.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_16_1_4UP.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_17_1_DCy.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_18_1_HEX.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_19_1_1gm.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_1_1_nbA.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_20_1_EWu.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_21_1_jai.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_22_1_drR.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_23_1_YJA.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_24_1_1c0.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_25_1_BI3.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_26_1_Y5X.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_27_1_uFq.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_28_1_wrX.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_29_1_rGa.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_2_1_fiq.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_30_1_JCP.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_31_1_krc.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_32_1_EXE.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_33_1_Y9y.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_34_1_s9k.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_35_1_da9.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_36_1_Uju.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_37_1_cyC.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_38_1_P76.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_39_1_s0U.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_3_1_oEO.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_40_1_ibX.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_41_1_9u0.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_42_1_Wko.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_43_1_31i.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_44_1_ZY7.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_45_1_g84.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_46_1_ZC8.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_47_1_WN5.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_48_1_Zfv.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_49_1_03o.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_4_1_qTW.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_50_1_eQ7.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_51_1_eVo.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_52_1_ASy.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_53_1_DL3.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_54_1_Mgv.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_55_1_eTF.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_56_1_raY.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_57_1_izD.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_58_1_9Bu.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_59_1_xs4.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_5_1_3WP.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_60_1_eHr.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_61_1_O0M.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_62_1_XQf.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_63_1_hjp.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_64_1_uD6.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_65_1_Vui.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_66_1_CDh.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_67_1_BYO.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_68_1_XMp.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_69_1_xKM.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_6_1_ak3.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_70_1_K5n.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_71_1_x8U.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_72_1_xc3.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_73_1_IGZ.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_74_1_vS0.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_75_1_uvN.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_76_1_8q3.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_77_1_XST.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_78_1_Rkk.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_79_1_ZR1.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_7_1_A2c.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_80_1_3QS.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_81_1_hsG.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_82_1_uby.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_83_1_Zd8.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_84_1_pvr.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_85_1_XZK.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_86_1_brH.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_87_1_UVe.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_88_1_TyA.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_89_1_bx4.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_8_1_WZG.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_90_1_7gp.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_91_1_DNU.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_92_1_02M.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_93_1_Hm6.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_94_1_Rrt.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_95_1_SU0.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_96_1_tnv.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_97_1_C7x.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_98_1_CeP.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_99_1_Yc2.root',
'file:/nasdata2/yuhow/photon3jet_MC_2011/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_2/G_Pt50_Tune4C_MPIenriched_7TeV_pythia8_cff_py_RAW2DIGI_L1Reco_RECO_VALIDATION_9_1_dXR.root')

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

process.p1 = cms.Sequence((process.UEAnalysisParticles+process.UEAnalysisTracks
                      *process.UEAnalysisJets
                      *process.UEAnalysisPFJets
                      #+process.genEventKTValue
                      +process.UEAnalysis))
#process.L1T1collpath=cms.Path(process.L1T1coll*process.p1)
process.goodvertex=cms.Path((process.primaryVertexFilter+process.noscraping)*process.p1)

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
process.UEAnalysisRootple500.GenJetCollectionName      = 'ueAntiKt5GenJet500'
process.UEAnalysisRootple500.ChgGenJetCollectionName   = 'ueAntiKt5ChgGenJet500'
process.UEAnalysisRootple500.TracksJetCollectionName   = 'ueAntiKt5TracksJet500'
process.UEAnalysisRootple500.RecoCaloJetCollectionName = 'ak5CaloJets'
process.UEAnalysisRootple500.PFJetCollectionName       = 'ueAntiKt5PFJet500'
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


