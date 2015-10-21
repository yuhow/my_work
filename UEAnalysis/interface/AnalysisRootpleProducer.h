#ifndef AnalysisRootpleProducer_H
#define AnalysisRootpleProducer_H

#include <memory>

#include <iostream>
#include <vector>
#include <algorithm>
#include <math.h>

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "JetMETCorrections/Modules/interface/JetCorrectionService.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

// jet ID
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"

#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/ESHandle.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <DataFormats/Common/interface/Handle.h>

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

#include <FWCore/ServiceRegistry/interface/Service.h>
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <TROOT.h>
#include <TTree.h>
#include <TFile.h>
#include <TLorentzVector.h>
#include <TVector.h>
#include <TObjString.h>
#include <TClonesArray.h>
#include <TH2D.h>

#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/JetReco/interface/BasicJet.h"
#include "DataFormats/JetReco/interface/BasicJetCollection.h"
#include "DataFormats/JetReco/interface/TrackJet.h"
#include "DataFormats/JetReco/interface/TrackJetCollection.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
//#include "RecoPixelVertexing/PixelVertexFinding/interface/PVClusterComparer.h"


// track
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/TrackingRecHit/interface/TrackingRecHit.h"

// access trigger results
#include <FWCore/Common/interface/TriggerNames.h>
#include <DataFormats/Common/interface/TriggerResults.h>
#include <DataFormats/HLTReco/interface/TriggerEvent.h> 
#include <DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h>

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include <DataFormats/HLTReco/interface/TriggerEvent.h>
#include <DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h>
#include "CondFormats/DataRecord/interface/L1GtTriggerMenuRcd.h"
#include "CondFormats/L1TObjects/interface/L1GtTriggerMenu.h"
#include "CondFormats/L1TObjects/interface/L1GtTriggerMenuFwd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetupFwd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetup.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMapRecord.h"

//handle recHits and clusters: maybe some package are redundant
#include "DataFormats/TrackingRecHit/interface/TrackingRecHit.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit2D.h"
#include "DataFormats/TrackerRecHit2D/interface/ProjectedSiStripRecHit2D.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripMatchedRecHit2D.h"
#include "DataFormats/SiStripCluster/interface/SiStripCluster.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripMatchedRecHit2DCollection.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit2DCollection.h"
#include "DataFormats/TrackerRecHit2D/interface/SiPixelRecHitCollection.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/SiStripDetId/interface/StripSubdetector.h"
#include "DataFormats/SiPixelDetId/interface/PixelSubdetector.h"
#include "DataFormats/SiPixelDetId/interface/PXBDetId.h"
#include "DataFormats/SiPixelDetId/interface/PXFDetId.h"
#include "DataFormats/SiPixelCluster/interface/SiPixelCluster.h"

//For electron
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "PhysicsTools/SelectorUtils/interface/SimpleCutBasedElectronIDSelectionFunctor.h"

// For Photon
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/EgammaReco/interface/PreshowerCluster.h"
#include "DataFormats/EgammaReco/interface/PreshowerClusterFwd.h"

#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgo.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgoRcd.h"
#include "CondFormats/DataRecord/interface/EcalChannelStatusRcd.h"
#include "CommonTools/Utils/interface/PtComparator.h"
//#include "RecoEgamma/EgammaTools/interface/ConversionLikelihoodCalculator.h"
#include "CommonTools/Statistics/interface/ChiSquaredProbability.h"
#include "DataFormats/HcalDetId/interface/HcalSubdetector.h"

//geometry
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"

#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/EcalAlgo/interface/EcalPreshowerGeometry.h"

//Candidate
#include "DataFormats/Candidate/interface/Candidate.h"

#include <Math/VectorUtil.h>


//PATObject
#include "DataFormats/PatCandidates/interface/PATObject.h"

#include "PhysicsTools/SelectorUtils/interface/strbitset.h"


// pile up summary info.
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"

using namespace edm;
using namespace reco;
using namespace trigger;
using std::vector;

class TTree;
class TFile;
class TObject;



class AnalysisRootpleProducer : public edm::EDAnalyzer
{
  

public:
  
  //
  explicit AnalysisRootpleProducer( const edm::ParameterSet& ) ;
  virtual ~AnalysisRootpleProducer() {} // no need to delete ROOT stuff
  // as it'll be deleted upon closing TFile

  virtual void analyze( const edm::Event& e, const edm::EventSetup &es ) ;
  virtual void beginJob() ;
  virtual void endJob() ;
  
  math::XYZPoint vtx_;
  typedef math::XYZPoint Point;

  //Point vtx_ ;

  void fillEventInfo(int);
  void store();


protected:

  virtual Int_t getNumOfPreshClusters(reco::Photon &photon, const edm::Event&);
  virtual Float_t getESRatio(reco::Photon &photon, const edm::Event&, const edm::EventSetup&);

  virtual Float_t getGenCalIso(edm::Handle<reco::GenParticleCollection> handle,
			        std::vector<GenParticle>::const_iterator thisPho, const Float_t dRMax=0.4, bool removeMu=true, bool removeNu=false);

  virtual Int_t JetVertexAssociation(edm::Handle<reco::VertexCollection> pvtxHandle, std::vector<reco::Vertex> vtxVector, std::vector<reco::PFJet>::const_iterator thisJet);
  
private:

  bool isMC;
  bool is2010DATA;
  bool is2011DATA;  
  bool onlyRECO;
  bool have_PILEUP;


  InputTag genJetCollName; // label of Jet made with MC particles
  InputTag genPartCollName ;  //for photon+jet analysis

  Handle< GenParticleCollection > CandHandleMCGamma  ;
  Handle< GenParticleCollection > CandHandleMCGamma_forMatch  ;
  Handle< GenJetCollection    > GenJetsHandle ;
  Handle< GenJetCollection    > GenJetsHandle_forSmear ;

  InputTag triggerResultsTag;
  InputTag triggerEventTag;

  InputTag electronProducer_;  //For Zee 
  InputTag photonProducer_;  //for photon+jet analysis

  int          pdgId_;            // PDG ID of expected MC particle
  std::vector<int> otherPdgIds_;  // PDG ID of other MC particles to match

  edm::InputTag ebReducedRecHitCollection_;
  edm::InputTag eeReducedRecHitCollection_;

  double   ecalBarrelMaxEta_; // Begining of ECAL Barrel/Endcap gap
  double   ecalEndcapMinEta_; // End of ECAL Barrel/Endcap gap

  InputTag pfJetCollName;    //for PFJet 

  Handle< TriggerResults      		> triggerResults;
  Handle< TriggerEvent     		> triggerEvent;
  Handle< reco::GsfElectronCollection 	> gsf_electrons;
  Handle< PhotonCollection              > photons_preMatch;
  Handle< PhotonCollection    		> photons;
  Handle< PhotonCollection		> photons_match;
  Handle< reco::PFJetCollection    	> NOcutPFJetsHandle;
  Handle< reco::PFJetCollection    	> LOOSEPFJetsHandle;
  Handle< reco::PFJetCollection     	> TIGHTPFJetsHandle;

  TriggerNames triggerNames;

  float piG;

  TTree* AnalysisTree;   //for all events
  int eventNum_RAW;
  int lumiBlock_RAW;
  int runNumber_RAW;
  int hltRunRange_2010data_RAW;
  int hltRunRange_2011data_RAW;
  int bx_RAW;
  double intrisic_weight_RAW;
  float n_interactions_RAW;
  float ave_nvtx_RAW;
  float pile_up_weight_RAW;
  vector<double> b_vtx_x;
  vector<double> b_vtx_y;
  vector<double> b_vtx_z;
  vector<double> b_vtx_d0;
  vector<int> b_vtx_ndof;
  vector<double> b_vtx_ptsum_track;

  double trkPt_squareSum_1stVtx_RAW;
  double trkPt_squareSum_2ndVtx_RAW;
  double trkPt_squareSum_3rdVtx_RAW;
  int n_vertex_RAW;

  int selection_number_RAW;  
 
  int    photon_Tag_RAW;

  vector<double> b_photonEt;
  vector<double> b_photonEta;
  vector<double> b_photonPhi;
  vector<double> b_photonEnergy;
  vector<double> b_photonScEta;
  vector<double> b_photonScPhi;
  vector<double> b_photonSigmaIetaIeta;
  vector<double> b_photonSigmaIphiIphi;
  vector<double> b_photonSigmaIetaIphi;
  vector<double> b_photonHadronicOverEm;
  vector<double> b_photonTrackIso;
  vector<double> b_photonEcalIso;
  vector<double> b_photonHcalIso;
  vector<int> b_photonHasPixelSeed;
  vector<double> b_photonSeedTime;
  
  vector<double> b_loosejetPt;
  vector<double> b_loosejetJecUnc;
  vector<double> b_loosejetEta;
  vector<double> b_loosejetPhi;
  vector<double> b_loosejetEnergy;
  vector<double> b_loosejet_association;

  vector<double> b_tightjetPt;
  vector<double> b_tightjetJecUnc;
  vector<double> b_tightjetEta;
  vector<double> b_tightjetPhi;
  vector<double> b_tightjetEnergy;
  vector<double> b_tightjet_association;

  TTree* DPS_AnalysisTree;   //for photon+3jet events

  // GEN Level //
  //info of event
  double gen_intrisic_weight;
  int    gen_n_jet_pt20;
  int    gen_n_jet_pt75;
  int    gen_is_DPS_event;
  //photon info
  double genIsoDR04;
  int  	 genMomId;
  double gen_pT_leadingPhoton;
  double gen_eta_leadingPhoton;
  double gen_phi_leadingPhoton;
  int gen_match_leadingPhoton;
  //jet info
  double gen_pT_leading1stJet;
  double gen_eta_leading1stJet;
  double gen_phi_leading1stJet;
  double gen_pT_leading2ndJet;
  double gen_eta_leading2ndJet;
  double gen_phi_leading2ndJet;
  double gen_pT_leading3rdJet;
  double gen_eta_leading3rdJet;
  double gen_phi_leading3rdJet;
  //pT ratio
  //DPS info
  double gen_DPS_S_CDFpT;
  double gen_DPS_dS_CDFpT;
  double gen_DPS_pT_GJ1;
  double gen_DPS_pT_J2J3;
  double gen_DPS_imbal_GJ1;
  double gen_DPS_imbal_J2J3;
  double gen_DPS_imbal_overall;
  double gen_DPS_dPhi_GJ1;
  double gen_DPS_dPhi_GJ2;
  double gen_DPS_dPhi_GJ3;
  double gen_DPS_dPhi_J1J2;
  double gen_DPS_dPhi_J1J3;
  double gen_DPS_dPhi_J2J3;
  double gen_DPS_MaxEta_jet;
  double gen_DPS_MinPt_jet;
  double gen_Et_ratio_J1G;
  double gen_Et_ratio_J3J2;
  //momentum fraction x (Bjorken-x dependence)
  double gen_DPS_x1_GJ;
  double gen_DPS_x1_JJ;
  double gen_DPS_x2_GJ;
  double gen_DPS_x2_JJ;

  // RECO Level //
  //info of event 
  int eventNum;
  int lumiBlock;
  int runNumber;
  int hltRunRange_2010data;
  int bx;
  double intrisic_weight; 
  float n_interactions;
  float ave_nvtx;
  float pile_up_weight;
  double trkPt_squareSum_1stVtx;
  double trkPt_squareSum_2ndVtx;
  double trkPt_squareSum_3rdVtx;
  int n_vertex;
  int n_jet_pt20;
  int n_jet_pt75;
  int is_DPS_event;
  //Z mass
  double Z_ee_mass;
  //photon info
  int    photon_Tag;
  double pT_leadingPhoton;
  double eta_leadingPhoton;
  double phi_leadingPhoton;
  int match_leadingPhoton;
  double leadingPhoton_scEta;
  double leadingPhoton_scPhi;
  double leadingPhoton_SigmaIetaIeta;
  double leadingPhoton_SigmaIphiIphi;
  double leadingPhoton_SigmaIetaIphi;
  double leadingPhoton_HadronicOverEm;
  double leadingPhoton_TrackIso;
  double leadingPhoton_EcalIso;
  double leadingPhoton_HcalIso;
  int    leadingPhoton_HasPixelSeed;
  float  leadingPhoton_SeedTime;
  //jet info
  double pT_leading1stJet;
  double eta_leading1stJet;
  double phi_leading1stJet;
  double jecUnc_leading1stJet;
  double pT_leading2ndJet;
  double eta_leading2ndJet;
  double phi_leading2ndJet;
  double jecUnc_leading2ndJet;
  double pT_leading3rdJet;
  double eta_leading3rdJet;
  double phi_leading3rdJet;
  double jecUnc_leading3rdJet;
  double chf_leading1stjet;
  double nhf_leading1stjet;
  double cef_leading1stjet;
  double nef_leading1stjet;
  double nch_leading1stjet;
  double nconstituents_leading1stjet;
  double chf_leading2ndjet;
  double nhf_leading2ndjet;
  double cef_leading2ndjet;
  double nef_leading2ndjet;
  double nch_leading2ndjet;
  double nconstituents_leading2ndjet;
  double chf_leading3rdjet;
  double nhf_leading3rdjet;
  double cef_leading3rdjet;
  double nef_leading3rdjet;
  double nch_leading3rdjet;
  double nconstituents_leading3rdjet;
  //pT ratio
  //DPS info, RECO LEVEL
  double DPS_S_CDFpT;    
  double DPS_dS_CDFpT;
  double DPS_pT_GJ1;
  double DPS_pT_J2J3;
  double DPS_imbal_GJ1;
  double DPS_imbal_J2J3;
  double DPS_imbal_overall;
  double DPS_dPhi_GJ1;
  double DPS_dPhi_GJ2;
  double DPS_dPhi_GJ3;
  double DPS_dPhi_J1J2;
  double DPS_dPhi_J1J3;
  double DPS_dPhi_J2J3;
  double DPS_MaxEta_jet;
  double DPS_MinPt_jet;
  double Et_ratio_J1G;
  double Et_ratio_J3J2;

  //DPS info, GEN LEVEL (counterpart)
  double DPS_S_CDFpT_genMatch;
  double DPS_dS_CDFpT_genMatch;
  double DPS_pT_GJ1_genMatch;
  double DPS_pT_J2J3_genMatch;
  double DPS_dPhi_GJ1_genMatch;
  double DPS_dPhi_GJ2_genMatch;
  double DPS_dPhi_GJ3_genMatch;
  double DPS_dPhi_J1J2_genMatch;
  double DPS_dPhi_J1J3_genMatch;
  double DPS_dPhi_J2J3_genMatch;
  double DPS_MaxEta_jet_genMatch;
  double DPS_MinPt_jet_genMatch;
  double Et_ratio_J1G_genMatch;
  double Et_ratio_J3J2_genMatch;

  //DPS info, GEN LEVEL
  double DPS_S_CDFpT_gen;
  double DPS_dS_CDFpT_gen;
  double DPS_imbal_GJ1_gen;
  double DPS_imbal_J2J3_gen;
  double DPS_imbal_overall_gen;
  double DPS_pT_GJ1_gen;
  double DPS_pT_J2J3_gen;
  double DPS_dPhi_GJ1_gen;
  double DPS_dPhi_GJ2_gen;
  double DPS_dPhi_GJ3_gen;
  double DPS_dPhi_J1J2_gen;
  double DPS_dPhi_J1J3_gen;
  double DPS_dPhi_J2J3_gen;
  double DPS_MaxEta_jet_gen;
  double DPS_MinPt_jet_gen;
  double Et_ratio_J1G_gen;
  double Et_ratio_J3J2_gen;

  //momentum fraction x (Bjorken-x dependence)
  double DPS_x1_GJ;
  double DPS_x1_JJ;
  double DPS_x2_GJ;
  double DPS_x2_JJ;


  vector<int>  pdgidList;

};

#endif
