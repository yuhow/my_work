import FWCore.ParameterSet.Config as cms

process = cms.Process("EcalSelectiveReadoutValid")

# initialize  MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

# initialize magnetic field
process.load("Configuration.StandardSequences.MagneticField_cff")

# geometry (Only Ecal)
process.load("Geometry.EcalCommonData.EcalOnly_cfi")
process.load("Geometry.CaloEventSetup.CaloGeometry_cff")
process.load("Geometry.CaloEventSetup.EcalTrigTowerConstituents_cfi")
process.load("Geometry.EcalMapping.EcalMapping_cfi")
process.load("Geometry.EcalMapping.EcalMappingRecord_cfi")

# DQM services
process.load("DQMServices.Core.DQM_cfg")

process.load("CalibCalorimetry.Configuration.Ecal_FakeConditions_cff")

# ECAL digitization sequence
process.load("SimCalorimetry.Configuration.ecalDigiSequence_cff")

# Defines Ecal seletive readout validation module, ecalSelectiveReadoutValidation:
process.load("Validation.EcalDigis.ecalSelectiveReadoutValidation_cfi")
process.ecalSelectiveReadoutValidation.outputFile = 'srvalid_hists.root'

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('/store/relval/CMSSW_3_2_2/RelValQCD_Pt_80_120/GEN-SIM-DIGI-RAW-HLTDEBUG/STARTUP31X_V2-v1/0001/A03E16E9-3C78-DE11-B612-0018F3D09620.root')
    fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_2.root',
                                      'file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_1.root')
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_3.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_4.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_5.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_6.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_7.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_8.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_9.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_10.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_11.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_12.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_13.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_14.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_15.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_16.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_17.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_18.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_19.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_20.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_21.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_22.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_23.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_24.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_25.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_26.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_27.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_28.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_29.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_30.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_31.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_32.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_33.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_34.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_35.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_36.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_37.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_38.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_39.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_40.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_41.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_42.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_43.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_44.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_45.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_46.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_47.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_48.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_49.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_50.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_51.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_52.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_53.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_54.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_55.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_56.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_57.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_58.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_59.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_60.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_61.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_62.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_63.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_64.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_65.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_66.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_67.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_68.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_69.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_70.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_71.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_72.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_73.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_74.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_75.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_76.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_77.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_78.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_79.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_80.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_81.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_82.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_83.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_84.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_85.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_86.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_87.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_88.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_89.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_90.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_91.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_92.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_93.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_94.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_95.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_96.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_97.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_98.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_99.root'),
#   fileNames = cms.untracked.vstring('file:/wk1/yuhow/HGCal_task/output_QCD_Pt_30_50/QCD_Pt_30_50_14TeV_pythia8_cff_py_GEN_SIM_100.root')
)

process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck")

process.tpparams12 = cms.ESSource("EmptyESSource",
    recordName = cms.string('EcalTPGPhysicsConstRcd'),
    iovIsRunNotTime = cms.bool(True),
    firstValid = cms.vuint32(1)
)

process.p1 = cms.Path(process.ecalSelectiveReadoutValidation)
process.DQM.collectorHost = ''
