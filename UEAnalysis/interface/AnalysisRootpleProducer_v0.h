#ifndef AnalysisRootpleProducer_H
#define AnalysisRootpleProducer_H

#include <iostream>

#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/ESHandle.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <DataFormats/Common/interface/Handle.h>

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

#include <FWCore/ServiceRegistry/interface/Service.h>
//#include <PhysicsTools/UtilAlgos/interface/TFileService.h>
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <TROOT.h>
#include <TTree.h>
#include <TFile.h>
#include <TLorentzVector.h>
#include <TVector.h>
#include <TObjString.h>
#include <TClonesArray.h>

#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/JetReco/interface/BasicJet.h"
#include "DataFormats/JetReco/interface/BasicJetCollection.h"
#include "DataFormats/JetReco/interface/TrackJetCollection.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/TrackingRecHit/interface/TrackingRecHit.h"

// access trigger results
#include <FWCore/Framework/interface/TriggerNames.h>
#include <DataFormats/Common/interface/TriggerResults.h>
#include <DataFormats/HLTReco/interface/TriggerEvent.h> 
#include <DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h>

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNames.h"
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

  virtual void analyze( const edm::Event&, const edm::EventSetup& ) ;
  virtual void beginJob() ;
  virtual void endJob() ;
  
  void fillEventInfo(int);
  void store();

private:
  
  bool onlyRECO;

  InputTag mcEvent; // label of MC event
  InputTag genJetCollName; // label of Jet made with MC particles
  InputTag chgJetCollName; // label of Jet made with only charged MC particles
  InputTag chgGenPartCollName; // label of charged MC particles
  InputTag tracksJetCollName;
  InputTag recoCaloJetCollName;
  InputTag tracksCollName;
  InputTag triggerResultsTag;
  InputTag triggerEventTag;
  InputTag genEventScaleTag;

  Handle< double              > genEventScaleHandle;
  Handle< HepMCProduct        > EvtHandle ;
  Handle< vector<GenParticle> > CandHandleMC ;
  Handle< GenJetCollection    > GenJetsHandle ;
  Handle< GenJetCollection    > ChgGenJetsHandle ;
  //  Handle< CandidateCollection > CandHandleRECO ;
  Handle< edm::View<reco::Candidate> > CandHandleRECO ;
  Handle< reco::TrackJetCollection  > TracksJetsHandle ;
  Handle< CaloJetCollection   > RecoCaloJetsHandle ;
  Handle< TriggerResults      > triggerResults;
  Handle< TriggerEvent        > triggerEvent;

  //  Handle<TriggerFilterObjectWithRefs> hltFilter; // not used at the moment: can access objects that fired the trigger
  TriggerNames triggerNames;

  edm::Service<TFileService> fs;

  float piG;

  TTree* AnalysisTree;

  int EventKind;

  TClonesArray* Parton;
  TClonesArray* MonteCarlo;
  TClonesArray* MonteCarlo2;
  TClonesArray* InclusiveJet;
  TClonesArray* ChargedJet;
  TClonesArray* Track;
  TClonesArray* AssVertex;
  TClonesArray* TracksJet;
  TClonesArray* CalorimeterJet;
  TClonesArray* acceptedTriggers;

  double genEventScale;
  //info sull'evento 
  int eventNum;
  int lumiBlock;
  int runNumber;
  int bx;

  //tracks with vertex
struct Vertex
{
  Int_t   npv;
  Double_t pvx[10];
  Double_t pvxErr[10];
  Double_t pvy[10];
  Double_t pvyErr[10];
  Double_t pvz[10];
  Double_t pvzErr[10];
  Double_t pvchi2[10];
  int   pvntk[10];
}vertex_;
 
struct TrackExtraUE
{
 Double_t  pvtkp[5000];
 Double_t pvtkpt[5000];
 Double_t pvtketa[5000];
 Double_t pvtkphi[5000];
 Double_t pvtknhit[5000];
 Double_t pvtkchi2norm[5000];
 Double_t pvtkd0[5000];
 Double_t pvtkd0Err[5000];
 Double_t pvtkdz[5000];
 Double_t pvtkdzErr[5000];
}trackextraue_;
 

struct TrackinJet
{
  Int_t tkn[100];
 Double_t tkp[5000];
 Double_t tkpt[5000];
 Double_t tketa[5000];
 Double_t tkphi[5000];
 Double_t tknhit[5000];
 Double_t tkchi2norm[5000];
 Double_t tkd0[5000];
 Double_t tkd0Err[5000];
 Double_t tkdz[5000];
 Double_t tkdzErr[5000];
}trackinjet_;
 

  vector<int>  pdgidList;

};

#endif
