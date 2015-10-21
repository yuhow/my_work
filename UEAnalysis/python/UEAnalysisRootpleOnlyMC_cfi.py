import FWCore.ParameterSet.Config as cms

DPSAnalysisRootpleOnlyMC = cms.EDAnalyzer("AnalysisRootpleProducerOnlyMC",
                                      GenPartCollectionName     = cms.InputTag("genParticles"),
                                      GenJetCollectionName      = cms.InputTag("ak5GenJets"),
 
)

DPSAnalysisOnlyMC = cms.Sequence(DPSAnalysisRootpleOnlyMC)


