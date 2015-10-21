import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.FastjetParameters_cfi import *
#from RecoJets.JetProducers.GenJetParameters_cfi import *
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

#from CondCore.DBCommon.CondDBSetup_cfi import *
from JetMETCorrections.Configuration.JetCorrectionServices_cff import *
from JetMETCorrections.Configuration.JetCorrectionProducers_cff import *
#from RecoJets.JetProducers.ak5GenJets_cfi import ak5GenJets
from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets



FastjetWithAreaPU = cms.PSet(
    Active_Area_Repeats = cms.int32(5),
    GhostArea = cms.double(0.01),
    Ghost_EtaMax = cms.double(6.0),
    UE_Subtraction = cms.string('no')
)

#ak5GenJets = cms.EDProducer(
#    "FastjetJetProducer",
#    GenJetParameters,
#    AnomalousCellParameters,
#    jetAlgorithm = cms.string("AntiKt"),
#    rParam       = cms.double(0.5)
#    )

#akt5PFJets = cms.EDProducer(
#    "FastjetJetProducer",
#    PFJetParameters,
#    AnomalousCellParameters,
#    jetAlgorithm = cms.string("AntiKt"),
#    rParam       = cms.double(0.5)
#    )


##MC jet
#ueAntiKt5GenJet = ak5GenJets.clone( 
#src = cms.InputTag("goodParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(0.9)
# )

#ueAntiKt5ChgGenJet = ak5GenJets.clone( 
#src = cms.InputTag("chargeParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(0.9)
# )

#ueAntiKt5GenJet500 = ak5GenJets.clone( 
#src = cms.InputTag("goodParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(0.5)
# )

#ueAntiKt5ChgGenJet500 = ak5GenJets.clone( 
#src = cms.InputTag("chargeParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(0.5)
# )

#ueAntiKt5GenJet1500 = ak5GenJets.clone( 
#src = cms.InputTag("goodParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(1.5)
# )

#ueAntiKt5ChgGenJet1500 = ak5GenJets.clone( 
#src = cms.InputTag("chargeParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(1.5)
# )

#ueAntiKt5GenJet700 = ak5GenJets.clone( 
#src = cms.InputTag("goodParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(0.7)
# )

#ueAntiKt5ChgGenJet700 = ak5GenJets.clone( 
#src = cms.InputTag("chargeParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(0.7)
# )

#ueAntiKt5GenJet1100 = ak5GenJets.clone( 
#src = cms.InputTag("goodParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(1.1)
# )

#ueAntiKt5ChgGenJet1100 = ak5GenJets.clone( 
#src = cms.InputTag("chargeParticles"),
#jetPtMin       = cms.double(1.0),
#inputEtMin     = cms.double(1.1)
# )

#ak5PFJetsL2L3 = cms.EDProducer(
#    'PFJetCorrectionProducer',
#    src        = cms.InputTag('ak5PFJets'),
#    correctors = cms.vstring('ak5PFL2L3Residual')
#    )


#RECO jet Tracks

ueAntiKt5PFJet500 = ak5PFJets.clone(
src            = cms.InputTag('particleFlow'),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.5)
)

ueAntiKt5PFJet = ak5PFJets.clone(
src            = cms.InputTag('particleFlow'),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.9)
)

ueAntiKt5PFJet1500 = ak5PFJets.clone(
  src            = cms.InputTag('particleFlow'),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(1.5)
)

ueAntiKt5PFJet700 = ak5PFJets.clone(
 src            = cms.InputTag('particleFlow'),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.7)
)

ueAntiKt5PFJet1100 = ak5PFJets.clone(
 src            = cms.InputTag('particleFlow'),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(1.1)
)

#UEAnalysisPFJetsOnlyMC = cms.Sequence(ueAntiKt5GenJet*ueAntiKt5ChgGenJet*ueAntiKt5GenJet500*ueAntiKt5ChgGenJet500*ueAntiKt5GenJet1500*ueAntiKt5ChgGenJet1500*ueAntiKt5GenJet700*ueAntiKt5ChgGenJet700*ueAntiKt5GenJet1100*ueAntiKt5ChgGenJet1100)
UEAnalysisPFJetsOnlyReco = cms.Sequence(ueAntiKt5PFJet500*ueAntiKt5PFJet*ueAntiKt5PFJet1500*ueAntiKt5PFJet700*ueAntiKt5PFJet1100)

#UEAnalysisPFJets = cms.Sequence(UEAnalysisPFJetsOnlyMC*UEAnalysisPFJetsOnlyReco)
UEAnalysisPFJets = cms.Sequence(UEAnalysisPFJetsOnlyReco)

