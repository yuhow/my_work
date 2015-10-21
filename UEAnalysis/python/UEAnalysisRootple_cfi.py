import FWCore.ParameterSet.Config as cms

DPSAnalysisRootple = cms.EDAnalyzer("AnalysisRootpleProducer",
                                      PFJetCollectionName       = cms.InputTag("ak5PFJets"),
                                      triggerEvent              = cms.InputTag("hltTriggerSummaryAOD"),
                                      GenPartCollectionName     = cms.InputTag("genParticles"),
                                      OnlyRECO                  = cms.bool(True),
				      IsMC                      = cms.bool(True),
				      Is2010DATA		= cms.bool(True),
                                      Is2011DATA                = cms.bool(True),
				      Have_PILEUP               = cms.bool(True),
                                      GenJetCollectionName      = cms.InputTag("ak5GenJets"),
                                      triggerResults            = cms.InputTag("TriggerResults","","HLT"),
                                      ebReducedRecHitCollection = cms.InputTag("reducedEcalRecHitsEB"),
                                      eeReducedRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
                                      PhotonProducer            = cms.InputTag("photons"),
				      ElectronProducer          = cms.InputTag("gsfElectrons")
)


DPSAnalysis = cms.Sequence(DPSAnalysisRootple)
