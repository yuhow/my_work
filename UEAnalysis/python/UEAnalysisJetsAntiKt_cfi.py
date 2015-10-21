import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.FastjetParameters_cfi import *
from RecoJets.JetProducers.ak5GenJets_cfi import ak5GenJets
from RecoJets.JetProducers.ak5TrackJets_cfi import ak5TrackJets




FastjetWithAreaPU = cms.PSet(
    Active_Area_Repeats = cms.int32(5),
    GhostArea = cms.double(0.01),
    Ghost_EtaMax = cms.double(6.0),
    UE_Subtraction = cms.string('no')
)

#MC jet
ueAntiKt5GenJet = ak5GenJets.clone( 
src = cms.InputTag("goodParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.9)
 )

ueAntiKt5ChgGenJet = ak5GenJets.clone( 
src = cms.InputTag("chargeParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.9)
 )

ueAntiKt5GenJet500 = ak5GenJets.clone( 
src = cms.InputTag("goodParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.5)
 )

ueAntiKt5ChgGenJet500 = ak5GenJets.clone( 
src = cms.InputTag("chargeParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.5)
 )

ueAntiKt5GenJet1500 = ak5GenJets.clone( 
src = cms.InputTag("goodParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(1.5)
 )

ueAntiKt5ChgGenJet1500 = ak5GenJets.clone( 
src = cms.InputTag("chargeParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(1.5)
 )


ueAntiKt5GenJet700 = ak5GenJets.clone( 
src = cms.InputTag("goodParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.7)
 )

ueAntiKt5ChgGenJet700 = ak5GenJets.clone( 
src = cms.InputTag("chargeParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.7)
 )

ueAntiKt5GenJet1100 = ak5GenJets.clone( 
src = cms.InputTag("goodParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(1.1)
 )

ueAntiKt5ChgGenJet1100 = ak5GenJets.clone( 
src = cms.InputTag("chargeParticles"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(1.1)
 )

#RECO jet Tracks

ueAntiKt5TracksJet500 = ak5TrackJets.clone(
    src = cms.InputTag("goodTracks"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.5)
)

ueAntiKt5TracksJet = ak5TrackJets.clone(
src = cms.InputTag("goodTracks"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.9)
)

ueAntiKt5TracksJet1500 = ak5TrackJets.clone(
    src = cms.InputTag("goodTracks"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(1.5)
)

ueAntiKt5TracksJet700 = ak5TrackJets.clone(
    src = cms.InputTag("goodTracks"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(0.7)
)

ueAntiKt5TracksJet1100 = ak5TrackJets.clone(
    src = cms.InputTag("goodTracks"),
jetPtMin       = cms.double(1.0),
inputEtMin     = cms.double(1.1)
)


UEAnalysisJetsOnlyMC = cms.Sequence(ueAntiKt5GenJet*ueAntiKt5ChgGenJet*ueAntiKt5GenJet500*ueAntiKt5ChgGenJet500*ueAntiKt5GenJet1500*ueAntiKt5ChgGenJet1500*ueAntiKt5GenJet700*ueAntiKt5ChgGenJet700*ueAntiKt5GenJet1100*ueAntiKt5ChgGenJet1100)

UEAnalysisJetsOnlyReco = cms.Sequence(ueAntiKt5TracksJet*ueAntiKt5TracksJet500*ueAntiKt5TracksJet700*ueAntiKt5TracksJet1500*ueAntiKt5TracksJet1100)


UEAnalysisJets = cms.Sequence(UEAnalysisJetsOnlyMC*UEAnalysisJetsOnlyReco)

