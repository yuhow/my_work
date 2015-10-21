// Authors: F. Ambroglini, L. Fano', F. Bechtel, Y.H. Chang
#include <QCDAnalysis/UEAnalysis/interface/AnalysisRootpleProducer.h>
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h" 

//using namespace pat;
using namespace edm;
using namespace std;
using namespace reco;
using namespace ROOT::Math::VectorUtil;


class VertexPtSumSort{
public:
  bool operator() (const reco::Vertex &v1, const reco::Vertex &v2) const {
    double sum_v1=0;
    double sum_v2=0;
    for (reco::Vertex::trackRef_iterator i=v1.tracks_begin(); i!=v1.tracks_end(); ++i) {
      double pt = (*i)->pt();
      if (pt > 0.5) { // Don't count tracks below 2.5 GeV
        //if (pt > 10.0) pt = 10.0;
        sum_v1 += pt*pt;
      }
    }
    for (reco::Vertex::trackRef_iterator i=v2.tracks_begin(); i!=v2.tracks_end(); ++i) {
      double pt = (*i)->pt();
      if (pt > 0.5) { // Don't count tracks below 2.5 GeV
        //if (pt > 10.0) pt = 10.0;
        sum_v2 += pt*pt;
      }
    }
    return sum_v1 > sum_v2;
  }
};

class GreaterPt{
public:
  bool operator()( const math::XYZTLorentzVector& a, const math::XYZTLorentzVector& b) {
    return a.pt() > b.pt();
  }
};

class GenJetSort{
public:
  bool operator()(const GenJet& a, const GenJet& b) {
    return a.pt() > b.pt();
  }
};

class GenPhotonSort{
public:
  bool operator()(const Candidate& a, const Candidate& b) {
    return a.pt() > b.pt();
  }
};

class PhotonSort{
public:
  bool operator()(const Photon& a, const Photon& b) {
    return a.pt() > b.pt();
  }
};

class BasicJetSort{
public:
  bool operator()(const reco::TrackJet& a, const reco::TrackJet& b) {
    return a.pt() > b.pt();
  }
};

class PFJetSort{
public:
  bool operator()(const reco::PFJet& a, const reco::PFJet& b) {
    return a.pt() > b.pt();
  }
};

class CaloJetSort{
public:
  bool operator()(const CaloJet& a, const CaloJet& b) {
    return a.pt() > b.pt();
  }
};

class QFcompareSort{
public:
  bool operator()(std::pair<int,double> o1, std::pair<int,double> o2) {
    return o1.second > o2.second;
  }
};


Int_t AnalysisRootpleProducer::getNumOfPreshClusters(reco::Photon &photon, const edm::Event& e) {

// ES clusters in X plane
  edm::Handle<reco::PreshowerClusterCollection> esClustersX;
  e.getByLabel(InputTag("multi5x5SuperClustersWithPreshower:preshowerXClusters"), esClustersX);
  const reco::PreshowerClusterCollection *ESclustersX = esClustersX.product();

// ES clusters in Y plane
  edm::Handle<reco::PreshowerClusterCollection> esClustersY;
  e.getByLabel(InputTag("multi5x5SuperClustersWithPreshower:preshowerYClusters"),esClustersY);
  const reco::PreshowerClusterCollection *ESclustersY = esClustersY.product();


  Int_t numOfPreshClusters(-1);
  
// Is the photon in region of Preshower?
  if (fabs(photon.eta())>1.62) {
    numOfPreshClusters=0;

  // Loop over all ECAL Basic clusters in the supercluster
    for (reco::CaloCluster_iterator ecalBasicCluster = photon.superCluster()->clustersBegin();
	 ecalBasicCluster!=photon.superCluster()->clustersEnd(); ecalBasicCluster++) {
      const reco::CaloClusterPtr ecalBasicClusterPtr = *(ecalBasicCluster);

      for (reco::PreshowerClusterCollection::const_iterator iESClus = ESclustersX->begin(); iESClus != ESclustersX->end(); ++iESClus) {
	const reco::CaloClusterPtr preshBasicCluster = iESClus->basicCluster();
//	const reco::PreshowerCluster *esCluster = &*iESClus;
	if (preshBasicCluster == ecalBasicClusterPtr) {
	  numOfPreshClusters++;
//	  cout << esCluster->energy() <<"\t" << esCluster->x() << "\t" << esCluster->y() << endl;
	}
      }  

      for (reco::PreshowerClusterCollection::const_iterator iESClus = ESclustersY->begin(); iESClus != ESclustersY->end(); ++iESClus) {
	const reco::CaloClusterPtr preshBasicCluster = iESClus->basicCluster();
//	const reco::PreshowerCluster *esCluster = &*iESClus;
	if (preshBasicCluster == ecalBasicClusterPtr) {
	  numOfPreshClusters++;
//	  cout << esCluster->energy() <<"\t" << esCluster->x() << "\t" << esCluster->y() << endl;
	}
      }
    } 
  } 

  return numOfPreshClusters;
  
}

Float_t AnalysisRootpleProducer::getESRatio(reco::Photon &photon, const edm::Event& e, const edm::EventSetup& iSetup){

  //get Geometry
  ESHandle<CaloGeometry> caloGeometry;
  iSetup.get<CaloGeometryRecord>().get(caloGeometry);
  const CaloSubdetectorGeometry *geometry = caloGeometry->getSubdetectorGeometry(DetId::Ecal, EcalPreshower);
  const CaloSubdetectorGeometry *& geometry_p = geometry;

  // Get ES rechits
  Float_t esratio=1.;
  edm::Handle<EcalRecHitCollection> PreshowerRecHits;
  e.getByLabel(InputTag("ecalPreshowerRecHit","EcalRecHitsES"), PreshowerRecHits);
  if( PreshowerRecHits.isValid() ) EcalRecHitCollection preshowerHits(*PreshowerRecHits);
  else return esratio;

   if (fabs(photon.eta())>1.62) {

    const reco::CaloClusterPtr seed = photon.superCluster()->seed();    
    reco::CaloCluster cluster = (*seed);
    const GlobalPoint phopoint(cluster.x(), cluster.y(), cluster.z());
  
    DetId photmp1 = (dynamic_cast<const EcalPreshowerGeometry*>(geometry_p))->getClosestCellInPlane(phopoint, 1);
    DetId photmp2 = (dynamic_cast<const EcalPreshowerGeometry*>(geometry_p))->getClosestCellInPlane(phopoint, 2);
    ESDetId esfid = (photmp1 == DetId(0)) ? ESDetId(0) : ESDetId(photmp1);
    ESDetId esrid = (photmp2 == DetId(0)) ? ESDetId(0) : ESDetId(photmp2);

    int gs_esfid = -99;
    int gs_esrid = -99;
    gs_esfid = esfid.six()*32+esfid.strip();
    gs_esrid = esrid.siy()*32+esrid.strip();

    float esfe3 = 0.; 
    float esfe21 = 0.; 
    float esre3 = 0.; 
    float esre21 = 0.;

    const ESRecHitCollection *ESRH = PreshowerRecHits.product();
    EcalRecHitCollection::const_iterator esrh_it;
    for ( esrh_it = ESRH->begin(); esrh_it != ESRH->end(); esrh_it++) {
      ESDetId esdetid = ESDetId(esrh_it->id());
      if ( esdetid.plane()==1 ) {
	if ( esdetid.zside() == esfid.zside() &&
	     esdetid.siy() == esfid.siy() ) {
	  int gs_esid = esdetid.six()*32+esdetid.strip();
	  int ss = gs_esid-gs_esfid;
	  if ( TMath::Abs(ss)<=10) {
	    esfe21 += esrh_it->energy();
	  } 
	  if ( TMath::Abs(ss)<=1) {
	    esfe3 += esrh_it->energy();
	  } 
	}
      }
      if (esdetid.plane()==2 ){
	if ( esdetid.zside() == esrid.zside() &&
	     esdetid.six() == esrid.six() ) {
	  int gs_esid = esdetid.siy()*32+esdetid.strip();
	  int ss = gs_esid-gs_esrid;
	  if ( TMath::Abs(ss)<=10) {
	    esre21 += esrh_it->energy();
	  } 
	  if ( TMath::Abs(ss)<=1) {
	    esre3 += esrh_it->energy();
	  } 
	}
      }
    }
  
    if( (esfe21+esre21) == 0.) {
      esratio = 1.;
    }else{
      esratio = (esfe3+esre3) / (esfe21+esre21);
    }
    
  }
  return esratio;
  
}

// get amount of generator isolation
// default cut value of etMin is 0.0
// return number of particles and sumEt surrounding candidate

Float_t AnalysisRootpleProducer::getGenCalIso(edm::Handle<reco::GenParticleCollection> handle,
					   std::vector<GenParticle>::const_iterator thisPho,const Float_t dRMax,
					   bool removeMu, bool removeNu)
{
  const Float_t etMin = 0.0;
  Float_t genCalIsoSum = 0.0;
  if(onlyRECO)return genCalIsoSum;
  if(!handle.isValid())return genCalIsoSum;

  for (reco::GenParticleCollection::const_iterator it_gen = 
	 handle->begin(); it_gen!=handle->end(); it_gen++){

    if(it_gen->px() == thisPho->px() && it_gen->py() == thisPho->py() && it_gen->pz() == thisPho->pz() && it_gen->energy() == thisPho->energy() && it_gen->pdgId() == thisPho->pdgId())continue;      // can't be the original photon
    if(it_gen->status()!=1 )continue;    // need to be a stable particle
    //if(it_gen->pdgId() ==22)continue;
    if (thisPho->collisionId() != it_gen->collisionId())  // has to come from the same collision
       continue; 
   
    Int_t pdgCode = abs(it_gen->pdgId());
    /// if(pdgCode>11 && pdgCode < 20)continue;     // we should not count neutrinos, muons
    if( removeMu && pdgCode == 13 ) continue;
    if( removeNu && ( pdgCode == 12 || pdgCode == 14 || pdgCode == 16 ) ) continue;

    Float_t et = it_gen->et();
    if(et < etMin) continue; // pass a minimum et threshold, default 0

    Float_t dR = reco::deltaR(thisPho->momentum(), 
			      it_gen->momentum());
    if(dR > dRMax) continue; // within deltaR cone
    genCalIsoSum += et;
    
  }// end of loop over gen particles

  return genCalIsoSum;
}

Int_t AnalysisRootpleProducer::JetVertexAssociation(edm::Handle<reco::VertexCollection> pvtxHandle, std::vector<reco::Vertex> vtxVector, std::vector<reco::PFJet>::const_iterator thisJet)
{
  Int_t ass_vertex = 99999.;

  std::vector<reco::PFCandidatePtr> pfcands =thisJet->getPFConstituents();
  double cand=0;
  double  candtot=0;
  double PtSumAssCand[200];
  for(int i=0;i<200;i++)
    PtSumAssCand[i]=0;
  int indvertex=0;
  typedef std::pair<int,double> vPtAss;
  std::vector<vPtAss> vertPtTrAssVector;
  double PtSumCand = 0;

  for(std::vector<reco::PFCandidatePtr>::const_iterator pfcand =pfcands.begin(); pfcand !=pfcands.end(); ++pfcand) {
    reco::TrackBaseRef trackBaseRef((*pfcand)->trackRef());
    candtot++;

    if(pfcand->isAvailable() && !trackBaseRef.isNull()){

      cand++;
      PtSumCand = PtSumCand + ((*pfcand)->pt()*(*pfcand)->pt());
      indvertex = 0;

      std::vector<reco::Vertex> vertexVector_ass;
      for (reco::VertexCollection::const_iterator itv_ass=pvtxHandle->begin(); itv_ass!=pvtxHandle->end(); ++itv_ass){
        vertexVector_ass.push_back(*itv_ass);
      }

      std::stable_sort(vertexVector_ass.begin(), vertexVector_ass.end(), VertexPtSumSort());

      if(vertexVector_ass.size()>0){
            for(reco::VertexCollection::const_iterator it_vtx_ass = vtxVector.begin(), it_vtx_ass_ed = vtxVector.end(); it_vtx_ass != it_vtx_ass_ed; ++it_vtx_ass) {
                reco::Vertex pv_ass;
                pv_ass = (*it_vtx_ass);
                for(reco::Vertex::trackRef_iterator pvt_ass = pv_ass.tracks_begin(); pvt_ass!= pv_ass.tracks_end(); pvt_ass++){
                  const reco::Track & track_ass = *pvt_ass->get();
                  if((float)(*pfcand)->pt()==(float)track_ass.pt()&&(float)(*pfcand)->eta()==(float)track_ass.eta()&&(float)(*pfcand)->phi()==(float)track_ass.phi()){
                    PtSumAssCand[indvertex] = PtSumAssCand[indvertex] + ((track_ass.pt())*(track_ass.pt()));;
                  }
                }
                indvertex++;
            }
      }
    }// end if available

  }

  std::pair<int,double> QualityFactor;
  std::vector<std::pair<int,double> > QFvector;

  for (int i=0; i!=indvertex; i++){

      QualityFactor.first = i;
      QualityFactor.second = PtSumAssCand[i]/PtSumCand;
      QFvector.push_back(QualityFactor);
  }

  std::sort(QFvector.begin(), QFvector.end(), QFcompareSort());
  std::pair<int,double> QFvector0;

  if (QFvector.size()>0){
    QFvector0 = QFvector[0];
    ass_vertex = QFvector0.first;
  }

  return ass_vertex;
} 

//void AnalysisRootpleProducer::store(){
//  AnalysisTree->Fill();
//}

void AnalysisRootpleProducer::fillEventInfo(int e){
}

AnalysisRootpleProducer::AnalysisRootpleProducer( const ParameterSet& pset )
{

  // flag to determinate this is a MC run or DATA run
  isMC     = pset.getParameter<bool>("IsMC");
  is2010DATA   = pset.getParameter<bool>("Is2010DATA");
  is2011DATA   = pset.getParameter<bool>("Is2011DATA");

  // flag to ignore gen-level analysis
  onlyRECO = pset.getParameter<bool>("OnlyRECO");

  // flag to determinate if the MC has pile-up effects or not
  have_PILEUP = pset.getParameter<bool>("Have_PILEUP");

  // Gen-Level
  genJetCollName      = pset.getParameter<InputTag>( "GenJetCollectionName"      );
  genPartCollName     = pset.getParameter<InputTag>( "GenPartCollectionName"     );

  // particle, track and jet collections
  pfJetCollName       = pset.getParameter<InputTag>( "PFJetCollectionName"       );

  // photon analysis
  photonProducer_              = pset.getParameter<InputTag>("PhotonProducer"); 

  pdgId_                       = pset.getUntrackedParameter<int>("pdgId", 22);
  otherPdgIds_                 = pset.getUntrackedParameter<vector<int> >("OtherPdgIds", vector<int>(1,11) );

  ebReducedRecHitCollection_   = pset.getParameter<edm::InputTag>("ebReducedRecHitCollection");
  eeReducedRecHitCollection_   = pset.getParameter<edm::InputTag>("eeReducedRecHitCollection");
  ecalBarrelMaxEta_            = pset.getUntrackedParameter<double>("EcalBarrelMaxEta",1.45);
  ecalEndcapMinEta_            = pset.getUntrackedParameter<double>("EcalEndcapMinEta",1.55);

  // trigger results
  triggerResultsTag = pset.getParameter<InputTag>("triggerResults");
  triggerEventTag   = pset.getParameter<InputTag>("triggerEvent"  );

  piG = acos(-1.);
  pdgidList.reserve(200);
}

void AnalysisRootpleProducer::beginJob()
{

  edm::Service<TFileService> fs;

  // use TFileService for output to root file

  AnalysisTree = fs->make<TTree>("AnalysisTree","Analysis Tree");   //for all event

  //event info
  AnalysisTree->Branch("eventNum_RAW",&eventNum_RAW,"eventNum_RAW/I");
  AnalysisTree->Branch("lumiBlock_RAW",&lumiBlock_RAW,"lumiBlock_RAW/I");
  AnalysisTree->Branch("runNumber_RAW",&runNumber_RAW,"runNumber_RAW/I");
  AnalysisTree->Branch("hltRunRange_2010data_RAW",&hltRunRange_2010data_RAW,"hltRunRange_2010data_RAW/I");
  AnalysisTree->Branch("bx_RAW",&bx_RAW,"bx_RAW/I");
  AnalysisTree->Branch("intrisic_weight_RAW",&intrisic_weight_RAW,"intrisic_weight_RAW/D");
  AnalysisTree->Branch("n_interactions_RAW",&n_interactions_RAW,"n_interactions_RAW/F");
  AnalysisTree->Branch("ave_nvtx_RAW",&ave_nvtx_RAW,"ave_nvtx_RAW/F");
  AnalysisTree->Branch("pile_up_weight_RAW",&pile_up_weight_RAW,"pile_up_weight_RAW/F");
  AnalysisTree->Branch("Vtx_X","vector<double>",&b_vtx_x);
  AnalysisTree->Branch("Vtx_Y","vector<double>",&b_vtx_y);
  AnalysisTree->Branch("Vtx_Z","vector<double>",&b_vtx_z);
  AnalysisTree->Branch("Vtx_d0","vector<double>",&b_vtx_d0);
  AnalysisTree->Branch("Vtx_Ndof","vector<int>",&b_vtx_ndof);
  AnalysisTree->Branch("Vtx_Ptsum_Track","vector<double>",&b_vtx_ptsum_track);

  AnalysisTree->Branch("trkPt_squareSum_1stVtx_RAW",&trkPt_squareSum_1stVtx_RAW,"trkPt_squareSum_1stVtx_RAW/D");
  AnalysisTree->Branch("trkPt_squareSum_2ndVtx_RAW",&trkPt_squareSum_2ndVtx_RAW,"trkPt_squareSum_2ndVtx_RAW/D");
  AnalysisTree->Branch("trkPt_squareSum_3rdVtx_RAW",&trkPt_squareSum_3rdVtx_RAW,"trkPt_squareSum_3rdVtx_RAW/D");
  AnalysisTree->Branch("n_vertex_RAW",&n_vertex_RAW,"n_vertex_RAW/I");

  AnalysisTree->Branch("selection_number_RAW",&selection_number_RAW,"selection_number_RAW/I");

  AnalysisTree->Branch("PhotonEt","vector<double>",&b_photonEt);
  AnalysisTree->Branch("PhotonEta","vector<double>",&b_photonEta);
  AnalysisTree->Branch("PhotonPhi","vector<double>",&b_photonPhi);
  AnalysisTree->Branch("PhotonEnergy","vector<double>",&b_photonEnergy);
  AnalysisTree->Branch("PhotonScEta","vector<double>",&b_photonScEta);
  AnalysisTree->Branch("PhotonScPhi","vector<double>",&b_photonScPhi);
  AnalysisTree->Branch("PhotonSigmaIetaIeta","vector<double>",&b_photonSigmaIetaIeta);
  AnalysisTree->Branch("PhotonSigmaIphiIphi","vector<double>",&b_photonSigmaIphiIphi);
  AnalysisTree->Branch("PhotonSigmaIetaIphi","vector<double>",&b_photonSigmaIetaIphi);
  AnalysisTree->Branch("PhotonHadronicOverEm","vector<double>",&b_photonHadronicOverEm);
  AnalysisTree->Branch("PhotonTrackIso","vector<double>",&b_photonTrackIso);
  AnalysisTree->Branch("PhotonEcalIso","vector<double>",&b_photonEcalIso);
  AnalysisTree->Branch("PhotonHcalIso","vector<double>",&b_photonHcalIso);
  AnalysisTree->Branch("PhotonHasPixelSeed","vector<int>",&b_photonHasPixelSeed);
  AnalysisTree->Branch("PhotonSeedTime","vector<double>",&b_photonSeedTime);

  AnalysisTree->Branch("LooseJetPt","vector<double>",&b_loosejetPt);
  AnalysisTree->Branch("LooseJetJecUnc","vector<double>",&b_loosejetJecUnc);
  AnalysisTree->Branch("LooseJetEta","vector<double>",&b_loosejetEta);
  AnalysisTree->Branch("LooseJetPhi","vector<double>",&b_loosejetPhi);
  AnalysisTree->Branch("LooseJetEnergy","vector<double>",&b_loosejetEnergy);
  AnalysisTree->Branch("LooseJetAssociation","vector<double>",&b_loosejet_association);

  AnalysisTree->Branch("TightJetPt","vector<double>",&b_tightjetPt);
  AnalysisTree->Branch("TightJetJecUnc","vector<double>",&b_tightjetJecUnc);
  AnalysisTree->Branch("TightJetEta","vector<double>",&b_tightjetEta);
  AnalysisTree->Branch("TightJetPhi","vector<double>",&b_tightjetPhi);
  AnalysisTree->Branch("TightJetEnergy","vector<double>",&b_tightjetEnergy);
  AnalysisTree->Branch("TightJetAssociation","vector<double>",&b_tightjet_association);

  DPS_AnalysisTree = fs->make<TTree>("DPS_AnalysisTree","DPS Analysis Tree");   //for photon+3jets event

  // GEN Level  //
  //event info
  DPS_AnalysisTree->Branch("gen_intrisic_weight",&gen_intrisic_weight,"gen_intrisic_weight/D");
  DPS_AnalysisTree->Branch("gen_n_jet_pt20",&gen_n_jet_pt20,"gen_n_jet_pt20/I");
  DPS_AnalysisTree->Branch("gen_n_jet_pt75",&gen_n_jet_pt75,"gen_n_jet_pt75/I");
  DPS_AnalysisTree->Branch("gen_is_DPS_event",&gen_is_DPS_event,"gen_is_DPS_event/I");

  //photon
  DPS_AnalysisTree->Branch("genIsoDR04",&genIsoDR04,"genIsoDR04/D");
  DPS_AnalysisTree->Branch("genMomId",&genMomId,"genMomId/I");
  DPS_AnalysisTree->Branch("gen_pT_leadingPhoton",&gen_pT_leadingPhoton,"gen_pT_leadingPhoton/D");
  DPS_AnalysisTree->Branch("gen_eta_leadingPhoton",&gen_eta_leadingPhoton,"gen_eta_leadingPhoton/D");
  DPS_AnalysisTree->Branch("gen_phi_leadingPhoton",&gen_phi_leadingPhoton,"gen_phi_leadingPhoton/D");

  //jet
  DPS_AnalysisTree->Branch("gen_pT_leading1stJet",&gen_pT_leading1stJet,"gen_pT_leading1stJet/D");
  DPS_AnalysisTree->Branch("gen_eta_leading1stJet",&gen_eta_leading1stJet,"gen_eta_leading1stJet/D");
  DPS_AnalysisTree->Branch("gen_phi_leading1stJet",&gen_phi_leading1stJet,"gen_phi_leading1stJet/D");
  DPS_AnalysisTree->Branch("gen_pT_leading2ndJet",&gen_pT_leading2ndJet,"gen_pT_leading2ndJet/D");
  DPS_AnalysisTree->Branch("gen_eta_leading2ndJet",&gen_eta_leading2ndJet,"gen_eta_leading2ndJet/D");
  DPS_AnalysisTree->Branch("gen_phi_leading2ndJet",&gen_phi_leading2ndJet,"gen_phi_leading2ndJet/D");
  DPS_AnalysisTree->Branch("gen_pT_leading3rdJet",&gen_pT_leading3rdJet,"gen_pT_leading3rdJet/D");
  DPS_AnalysisTree->Branch("gen_eta_leading3rdJet",&gen_eta_leading3rdJet,"gen_eta_leading3rdJet/D");
  DPS_AnalysisTree->Branch("gen_phi_leading3rdJet",&gen_phi_leading3rdJet,"gen_phi_leading3rdJet/D");

  //DPS analysis
  DPS_AnalysisTree->Branch("gen_DPS_S_CDFpT",&gen_DPS_S_CDFpT,"gen_DPS_S_CDFpT/D");
  DPS_AnalysisTree->Branch("gen_DPS_dS_CDFpT",&gen_DPS_dS_CDFpT,"gen_DPS_dS_CDFpT/D");
  DPS_AnalysisTree->Branch("gen_DPS_pT_GJ1",&gen_DPS_pT_GJ1,"gen_DPS_pT_GJ1/D");
  DPS_AnalysisTree->Branch("gen_DPS_pT_J2J3",&gen_DPS_pT_J2J3,"gen_DPS_pT_J2J3/D");
  DPS_AnalysisTree->Branch("gen_DPS_imbal_GJ1",&gen_DPS_imbal_GJ1,"gen_DPS_imbal_GJ1/D");
  DPS_AnalysisTree->Branch("gen_DPS_imbal_J2J3",&gen_DPS_imbal_J2J3,"gen_DPS_imbal_J2J3/D");
  DPS_AnalysisTree->Branch("gen_DPS_imbal_overall",&gen_DPS_imbal_overall,"gen_DPS_imbal_overall/D");
  DPS_AnalysisTree->Branch("gen_DPS_dPhi_GJ1",&gen_DPS_dPhi_GJ1,"gen_DPS_dPhi_GJ1/D");
  DPS_AnalysisTree->Branch("gen_DPS_dPhi_GJ2",&gen_DPS_dPhi_GJ2,"gen_DPS_dPhi_GJ2/D");
  DPS_AnalysisTree->Branch("gen_DPS_dPhi_GJ3",&gen_DPS_dPhi_GJ3,"gen_DPS_dPhi_GJ3/D");
  DPS_AnalysisTree->Branch("gen_DPS_dPhi_J1J2",&gen_DPS_dPhi_J1J2,"gen_DPS_dPhi_J1J2/D");
  DPS_AnalysisTree->Branch("gen_DPS_dPhi_J1J3",&gen_DPS_dPhi_J1J3,"gen_DPS_dPhi_J1J3/D");
  DPS_AnalysisTree->Branch("gen_DPS_dPhi_J2J3",&gen_DPS_dPhi_J2J3,"gen_DPS_dPhi_J2J3/D");
  DPS_AnalysisTree->Branch("gen_DPS_MaxEta_jet",&gen_DPS_MaxEta_jet,"gen_DPS_MaxEta_jet/D");
  DPS_AnalysisTree->Branch("gen_DPS_MinPt_jet",&gen_DPS_MinPt_jet,"gen_DPS_MinPt_jet/D");
  DPS_AnalysisTree->Branch("gen_Et_ratio_J1G",&gen_Et_ratio_J1G,"gen_Et_ratio_J1G/D");
  DPS_AnalysisTree->Branch("gen_Et_ratio_J3J2",&gen_Et_ratio_J3J2,"gen_Et_ratio_J3J2/D");

  //Bjorken-x dependence
  DPS_AnalysisTree->Branch("gen_DPS_x1_GJ",&gen_DPS_x1_GJ,"gen_DPS_x1_GJ/D");
  DPS_AnalysisTree->Branch("gen_DPS_x1_JJ",&gen_DPS_x1_JJ,"gen_DPS_x1_JJ/D");
  DPS_AnalysisTree->Branch("gen_DPS_x2_GJ",&gen_DPS_x2_GJ,"gen_DPS_x2_GJ/D");
  DPS_AnalysisTree->Branch("gen_DPS_x2_JJ",&gen_DPS_x2_JJ,"gen_DPS_x2_JJ/D");

  // RECO Level //
  //event info
  DPS_AnalysisTree->Branch("eventNum",&eventNum,"eventNum/I");
  DPS_AnalysisTree->Branch("lumiBlock",&lumiBlock,"lumiBlock/I");
  DPS_AnalysisTree->Branch("runNumber",&runNumber,"runNumber/I"); 
  DPS_AnalysisTree->Branch("hltRunRange_2010data",&hltRunRange_2010data,"hltRunRange_2010data/I");
  DPS_AnalysisTree->Branch("bx",&bx,"bx/I");
  DPS_AnalysisTree->Branch("intrisic_weight",&intrisic_weight,"intrisic_weight/D");
  DPS_AnalysisTree->Branch("n_interactions",&n_interactions,"n_interactions/F");
  DPS_AnalysisTree->Branch("ave_nvtx",&ave_nvtx,"ave_nvtx/F");
  DPS_AnalysisTree->Branch("pile_up_weight",&pile_up_weight,"pile_up_weight/F"); 
  DPS_AnalysisTree->Branch("trkPt_squareSum_1stVtx",&trkPt_squareSum_1stVtx,"trkPt_squareSum_1stVtx/D");
  DPS_AnalysisTree->Branch("trkPt_squareSum_2ndVtx",&trkPt_squareSum_2ndVtx,"trkPt_squareSum_2ndVtx/D");
  DPS_AnalysisTree->Branch("trkPt_squareSum_3rdVtx",&trkPt_squareSum_3rdVtx,"trkPt_squareSum_3rdVtx/D");
  DPS_AnalysisTree->Branch("n_vertex",&n_vertex,"n_vertex/I");
  DPS_AnalysisTree->Branch("n_jet_pt20",&n_jet_pt20,"n_jet_pt20/I");
  DPS_AnalysisTree->Branch("n_jet_pt75",&n_jet_pt75,"n_jet_pt75/I");
  DPS_AnalysisTree->Branch("is_DPS_event",&is_DPS_event,"is_DPS_event/I");

  //photon
  DPS_AnalysisTree->Branch("pT_leadingPhoton",&pT_leadingPhoton,"pT_leadingPhoton/D");
  DPS_AnalysisTree->Branch("eta_leadingPhoton",&eta_leadingPhoton,"eta_leadingPhoton/D");
  DPS_AnalysisTree->Branch("phi_leadingPhoton",&phi_leadingPhoton,"phi_leadingPhoton/D");
  DPS_AnalysisTree->Branch("leadingPhoton_scEta",&leadingPhoton_scEta,"leadingPhoton_scEta/D");
  DPS_AnalysisTree->Branch("leadingPhoton_scPhi",&leadingPhoton_scPhi,"leadingPhoton_scPhi/D");
  DPS_AnalysisTree->Branch("leadingPhoton_SigmaIetaIeta",&leadingPhoton_SigmaIetaIeta,"leadingPhoton_SigmaIetaIeta/D");
  DPS_AnalysisTree->Branch("leadingPhoton_SigmaIphiIphi",&leadingPhoton_SigmaIphiIphi,"leadingPhoton_SigmaIphiIphi/D");
  DPS_AnalysisTree->Branch("leadingPhoton_SigmaIetaIphi",&leadingPhoton_SigmaIetaIphi,"leadingPhoton_SigmaIetaIphi/D");
  DPS_AnalysisTree->Branch("leadingPhoton_HadronicOverEm",&leadingPhoton_HadronicOverEm,"leadingPhoton_HadronicOverEm/D");
  DPS_AnalysisTree->Branch("leadingPhoton_TrackIso",&leadingPhoton_TrackIso,"leadingPhoton_TrackIso/D");
  DPS_AnalysisTree->Branch("leadingPhoton_EcalIso",&leadingPhoton_EcalIso,"leadingPhoton_EcalIso/D");
  DPS_AnalysisTree->Branch("leadingPhoton_HcalIso",&leadingPhoton_HcalIso,"leadingPhoton_HcalIso/D");
  DPS_AnalysisTree->Branch("leadingPhoton_HasPixelSeed",&leadingPhoton_HasPixelSeed,"leadingPhoton_HasPixelSeed/I");
  DPS_AnalysisTree->Branch("leadingPhoton_SeedTime",&leadingPhoton_SeedTime,"leadingPhoton_SeedTime/F");

  //jet
  DPS_AnalysisTree->Branch("pT_leading1stJet",&pT_leading1stJet,"pT_leading1stJet/D");
  DPS_AnalysisTree->Branch("eta_leading1stJet",&eta_leading1stJet,"eta_leading1stJet/D");
  DPS_AnalysisTree->Branch("phi_leading1stJet",&phi_leading1stJet,"phi_leading1stJet/D");
  DPS_AnalysisTree->Branch("jecUnc_leading1stJet",&jecUnc_leading1stJet,"jecUnc_leading1stJet/D");
  DPS_AnalysisTree->Branch("pT_leading2ndJet",&pT_leading2ndJet,"pT_leading2ndJet/D");
  DPS_AnalysisTree->Branch("eta_leading2ndJet",&eta_leading2ndJet,"eta_leading2ndJet/D");
  DPS_AnalysisTree->Branch("phi_leading2ndJet",&phi_leading2ndJet,"phi_leading2ndJet/D");
  DPS_AnalysisTree->Branch("jecUnc_leading2ndJet",&jecUnc_leading2ndJet,"jecUnc_leading2ndJet/D");
  DPS_AnalysisTree->Branch("pT_leading3rdJet",&pT_leading3rdJet,"pT_leading3rdJet/D");
  DPS_AnalysisTree->Branch("eta_leading3rdJet",&eta_leading3rdJet,"eta_leading3rdJet/D");
  DPS_AnalysisTree->Branch("phi_leading3rdJet",&phi_leading3rdJet,"phi_leading3rdJet/D");
  DPS_AnalysisTree->Branch("jecUnc_leading3rdJet",&jecUnc_leading3rdJet,"jecUnc_leading3rdJet/D");
  DPS_AnalysisTree->Branch("chf_leading1stjet"          ,&chf_leading1stjet          ,"chf_leading1stjet/D"          ); 
  DPS_AnalysisTree->Branch("nhf_leading1stjet"          ,&nhf_leading1stjet          ,"nhf_leading1stjet/D"          );
  DPS_AnalysisTree->Branch("cef_leading1stjet"          ,&cef_leading1stjet          ,"cef_leading1stjet/D"          );
  DPS_AnalysisTree->Branch("nef_leading1stjet"          ,&nef_leading1stjet          ,"nef_leading1stjet/D"          );
  DPS_AnalysisTree->Branch("nch_leading1stjet"          ,&nch_leading1stjet          ,"nch_leading1stjet/D"          );
  DPS_AnalysisTree->Branch("nconstituents_leading1stjet",&nconstituents_leading1stjet,"nconstituents_leading1stjet/D");
  DPS_AnalysisTree->Branch("chf_leading2ndjet"          ,&chf_leading2ndjet          ,"chf_leading2ndjet/D"          );
  DPS_AnalysisTree->Branch("nhf_leading2ndjet"          ,&nhf_leading2ndjet          ,"nhf_leading2ndjet/D"          );
  DPS_AnalysisTree->Branch("cef_leading2ndjet"          ,&cef_leading2ndjet          ,"cef_leading2ndjet/D"          );
  DPS_AnalysisTree->Branch("nef_leading2ndjet"          ,&nef_leading2ndjet          ,"nef_leading2ndjet/D"          );
  DPS_AnalysisTree->Branch("nch_leading2ndjet"          ,&nch_leading2ndjet          ,"nch_leading2ndjet/D"          );
  DPS_AnalysisTree->Branch("nconstituents_leading2ndjet",&nconstituents_leading2ndjet,"nconstituents_leading2ndjet/D");
  DPS_AnalysisTree->Branch("chf_leading3rdjet"          ,&chf_leading3rdjet          ,"chf_leading3rdjet/D"          );
  DPS_AnalysisTree->Branch("nhf_leading3rdjet"          ,&nhf_leading3rdjet          ,"nhf_leading3rdjet/D"          );
  DPS_AnalysisTree->Branch("cef_leading3rdjet"          ,&cef_leading3rdjet          ,"cef_leading3rdjet/D"          );
  DPS_AnalysisTree->Branch("nef_leading3rdjet"          ,&nef_leading3rdjet          ,"nef_leading3rdjet/D"          );
  DPS_AnalysisTree->Branch("nch_leading3rdjet"          ,&nch_leading3rdjet          ,"nch_leading3rdjet/D"          );
  DPS_AnalysisTree->Branch("nconstituents_leading3rdjet",&nconstituents_leading3rdjet,"nconstituents_leading3rdjet/D");

  //DPS analysis
  DPS_AnalysisTree->Branch("DPS_S_CDFpT",&DPS_S_CDFpT,"DPS_S_CDFpT/D");
  DPS_AnalysisTree->Branch("DPS_dS_CDFpT",&DPS_dS_CDFpT,"DPS_dS_CDFpT/D");
  DPS_AnalysisTree->Branch("DPS_pT_GJ1",&DPS_pT_GJ1,"DPS_pT_GJ1/D");
  DPS_AnalysisTree->Branch("DPS_pT_J2J3",&DPS_pT_J2J3,"DPS_pT_J2J3/D");
  DPS_AnalysisTree->Branch("DPS_imbal_GJ1",&DPS_imbal_GJ1,"DPS_imbal_GJ1/D");
  DPS_AnalysisTree->Branch("DPS_imbal_J2J3",&DPS_imbal_J2J3,"DPS_imbal_J2J3/D");
  DPS_AnalysisTree->Branch("DPS_imbal_overall",&DPS_imbal_overall,"DPS_imbal_overall/D");
  DPS_AnalysisTree->Branch("DPS_dPhi_GJ1",&DPS_dPhi_GJ1,"DPS_dPhi_GJ1/D");
  DPS_AnalysisTree->Branch("DPS_dPhi_GJ2",&DPS_dPhi_GJ2,"DPS_dPhi_GJ2/D");
  DPS_AnalysisTree->Branch("DPS_dPhi_GJ3",&DPS_dPhi_GJ3,"DPS_dPhi_GJ3/D");
  DPS_AnalysisTree->Branch("DPS_dPhi_J1J2",&DPS_dPhi_J1J2,"DPS_dPhi_J1J2/D");
  DPS_AnalysisTree->Branch("DPS_dPhi_J1J3",&DPS_dPhi_J1J3,"DPS_dPhi_J1J3/D");
  DPS_AnalysisTree->Branch("DPS_dPhi_J2J3",&DPS_dPhi_J2J3,"DPS_dPhi_J2J3/D");
  DPS_AnalysisTree->Branch("DPS_MaxEta_jet",&DPS_MaxEta_jet,"DPS_MaxEta_jet/D");
  DPS_AnalysisTree->Branch("DPS_MinPt_jet",&DPS_MinPt_jet,"DPS_MinPt_jet/D");
  DPS_AnalysisTree->Branch("Et_ratio_J1G",&Et_ratio_J1G,"Et_ratio_J1G/D");
  DPS_AnalysisTree->Branch("Et_ratio_J3J2",&Et_ratio_J3J2,"Et_ratio_J3J2/D");

  //Bjorken-x dependence
  DPS_AnalysisTree->Branch("DPS_x1_GJ",&DPS_x1_GJ,"DPS_x1_GJ/D");
  DPS_AnalysisTree->Branch("DPS_x1_JJ",&DPS_x1_JJ,"DPS_x1_JJ/D");
  DPS_AnalysisTree->Branch("DPS_x2_GJ",&DPS_x2_GJ,"DPS_x2_GJ/D");
  DPS_AnalysisTree->Branch("DPS_x2_JJ",&DPS_x2_JJ,"DPS_x2_JJ/D");

}

  
void AnalysisRootpleProducer::analyze( const Event& e, const edm::EventSetup& iSetup )
{

  // branch variables initialization
  // raw analysis tree
  eventNum_RAW = -1;
  lumiBlock_RAW = -1;
  runNumber_RAW = -1;
  hltRunRange_2010data_RAW = 0;
  bx_RAW = -1;
  intrisic_weight_RAW = -1;
  n_interactions_RAW = -1;
  ave_nvtx_RAW = -1;
  pile_up_weight_RAW = -1;

  b_vtx_x.clear();
  b_vtx_y.clear();
  b_vtx_z.clear();
  b_vtx_d0.clear();
  b_vtx_ndof.clear();
  b_vtx_ptsum_track.clear();

  trkPt_squareSum_1stVtx_RAW = -1;
  trkPt_squareSum_2ndVtx_RAW = -1;
  trkPt_squareSum_3rdVtx_RAW = -1;
  n_vertex_RAW = -1;
  selection_number_RAW = 0;

  b_photonEt.clear();
  b_photonEta.clear();
  b_photonPhi.clear();
  b_photonEnergy.clear();
  b_photonScEta.clear();
  b_photonScPhi.clear();
  b_photonSigmaIetaIeta.clear();
  b_photonSigmaIphiIphi.clear();
  b_photonSigmaIetaIphi.clear();
  b_photonHadronicOverEm.clear();
  b_photonTrackIso.clear();
  b_photonEcalIso.clear();
  b_photonHcalIso.clear();
  b_photonHasPixelSeed.clear();
  b_photonSeedTime.clear();

  b_loosejetPt.clear();
  b_loosejetJecUnc.clear();
  b_loosejetEta.clear();
  b_loosejetPhi.clear();
  b_loosejetEnergy.clear();
  b_loosejet_association.clear();

  b_tightjetPt.clear();
  b_tightjetJecUnc.clear();
  b_tightjetEta.clear();
  b_tightjetPhi.clear();
  b_tightjetEnergy.clear();
  b_tightjet_association.clear();

  // DPS analysis tree, GEN
  //info of event
  gen_intrisic_weight = -1;
  gen_n_jet_pt20 = -1;
  gen_n_jet_pt75 = -1;
  gen_is_DPS_event = -1;
  //photon info
  genIsoDR04 = -999;
  genMomId = 0;
  gen_pT_leadingPhoton = -999;
  gen_eta_leadingPhoton = -999;
  gen_phi_leadingPhoton = -999;
  //jet info
  gen_pT_leading1stJet = -999;
  gen_eta_leading1stJet = -999;
  gen_phi_leading1stJet = -999;
  gen_pT_leading2ndJet = -999;
  gen_eta_leading2ndJet = -999;
  gen_phi_leading2ndJet = -999;
  gen_pT_leading3rdJet = -999;
  gen_eta_leading3rdJet = -999;
  gen_phi_leading3rdJet = -999;
  //pT ratio
  //DPS info
  gen_DPS_S_CDFpT = -999;
  gen_DPS_dS_CDFpT = -999;
  gen_DPS_pT_GJ1 = -999;
  gen_DPS_pT_J2J3 = -999;
  gen_DPS_imbal_GJ1 = -999;
  gen_DPS_imbal_J2J3 = -999;
  gen_DPS_imbal_overall = -999;
  gen_DPS_dPhi_GJ1 = -999;
  gen_DPS_dPhi_GJ2 = -999;
  gen_DPS_dPhi_GJ3 = -999;
  gen_DPS_dPhi_J1J2 = -999;
  gen_DPS_dPhi_J1J3 = -999;
  gen_DPS_dPhi_J2J3 = -999;
  gen_DPS_MaxEta_jet = -999;
  gen_DPS_MinPt_jet = -999;
  gen_Et_ratio_J1G = -999;
  gen_Et_ratio_J3J2 = -999;
  //momentum fraction x (Bjorken-x dependence)
  gen_DPS_x1_GJ = -999;
  gen_DPS_x1_JJ = -999;
  gen_DPS_x2_GJ = -999;
  gen_DPS_x2_JJ = -999;

  // DPS analysis tree, RECO
  eventNum = -1;
  lumiBlock = -1;
  runNumber = -1;
  hltRunRange_2010data = 0;
  bx = -1;
  intrisic_weight = -1.;
  n_interactions = -1.;
  ave_nvtx = -1.;
  pile_up_weight = -1.;
  trkPt_squareSum_1stVtx = -1;
  trkPt_squareSum_2ndVtx = -1;
  trkPt_squareSum_3rdVtx = -1;
  n_vertex = -1;
  n_jet_pt20 = -1;
  n_jet_pt75 = -1;
  is_DPS_event = -1;
  //photon info
  pT_leadingPhoton = -999.;
  eta_leadingPhoton = -999.;
  phi_leadingPhoton = -999.;
  leadingPhoton_scEta = -999.;
  leadingPhoton_scPhi = -999.;
  leadingPhoton_SigmaIetaIeta = -999.;
  leadingPhoton_SigmaIphiIphi = -999.;
  leadingPhoton_SigmaIetaIphi = -999.;
  leadingPhoton_HadronicOverEm = -999.;
  leadingPhoton_TrackIso = -999.;
  leadingPhoton_EcalIso = -999.;
  leadingPhoton_HcalIso = -999.;
  leadingPhoton_HasPixelSeed = -1;
  leadingPhoton_SeedTime = -999.;
  //jet info
  pT_leading1stJet = -999.;
  eta_leading1stJet = -999.;
  phi_leading1stJet = -999.;
  jecUnc_leading1stJet = -999.;
  pT_leading2ndJet = -999.;
  eta_leading2ndJet = -999.;
  phi_leading2ndJet = -999.;
  jecUnc_leading2ndJet = -999.;
  pT_leading3rdJet = -999.;
  eta_leading3rdJet = -999.;
  phi_leading3rdJet = -999.;
  jecUnc_leading3rdJet = -999.;
  //pT ratio
  //DPS info
  DPS_S_CDFpT = -999.;
  DPS_dS_CDFpT = -999.;
  DPS_imbal_GJ1 = -999.;
  DPS_imbal_J2J3 = -999.;
  DPS_imbal_overall = -999.;
  DPS_pT_GJ1 = -999.;
  DPS_pT_J2J3 = -999.;
  DPS_dPhi_GJ1 = -999.;
  DPS_dPhi_GJ2 = -999.;
  DPS_dPhi_GJ3 = -999.;
  DPS_dPhi_J1J2 = -999.;
  DPS_dPhi_J1J3 = -999.;
  DPS_dPhi_J2J3 = -999.;
  DPS_MaxEta_jet = -999.;
  DPS_MinPt_jet = -999.;
  Et_ratio_J1G = -999.;
  Et_ratio_J3J2 = -999.;
  //momentum fraction x (Bjorken-x dependence)
  DPS_x1_GJ = -999.;
  DPS_x1_JJ = -999.;
  DPS_x2_GJ = -999.;
  DPS_x2_JJ = -999.;

  // basic event infomation
  eventNum_RAW   = e.id().event() ;
  runNumber_RAW  = e.id().run() ;
  lumiBlock_RAW  = e.luminosityBlock() ;
  bx_RAW = e.bunchCrossing();

  eventNum   = e.id().event() ;
  runNumber  = e.id().run() ;
  lumiBlock  = e.luminosityBlock() ;
  bx = e.bunchCrossing();

  // intrinsic event weight
  double Event_weight;
  edm::Handle<GenEventInfoProduct> hEventInfo;
  e.getByLabel("generator", hEventInfo);
  if (hEventInfo.isValid()) {
    Event_weight = hEventInfo->weight();
  }
  else
    Event_weight = 1.;

  intrisic_weight_RAW = Event_weight;
  //Event_weight = 1.;

  // pile up info.

  //float sum_nvtx = 0; //!!
  //Tnvtx = -1.0;;  //for S6

  if(!onlyRECO){
    Handle<std::vector< PileupSummaryInfo > >  PupInfo;
    e.getByLabel(edm::InputTag("addPileupInfo"), PupInfo);

    std::vector<PileupSummaryInfo>::const_iterator PVI;

    for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {

       //std::cout << " Pileup Information: bunchXing, nvtx: " << PVI->getBunchCrossing() << " " << PVI->getPU_NumInteractions() << std::endl;
       int BX_ = PVI->getBunchCrossing();

       if(BX_ == 0) { //in time
         n_interactions = PVI->getPU_NumInteractions();  //S3 & S4 for in-time weighting only
	 n_interactions_RAW = PVI->getPU_NumInteractions();
	 //Tnvtx = PVI->getTrueNumInteractions(); //S6
         continue;
        }

       ////for PU S4 condition, distribution obtained by averaging the number of interactions!!
       //n_interactions = PVI->getPU_NumInteractions();
       //sum_nvtx += float(n_interactions);

    }
    ave_nvtx = n_interactions; //for S3 & S4 for in-time weighting only
    //cout<<ave_nvtx<<endl;
    ave_nvtx_RAW = n_interactions_RAW;
    //ave_nvtx= sum_nvtx/3.; //for S4 avg.
    //ave_nvtx= Tnvtx; //for S6 Fall11
  }

  float pu_reweight ( 1. );

//  2010 Pileup Scenarios if one assumes a fixed efficiency of primary vertex reconstruction for minbias events of about 70%
//  Float_t pileup_2010_data[55] =  {0.145168, 0.251419, 0.251596, 0.17943, 0.10, 0.05, 0.02, 0.01, 0.005, 0.002,
//                                      0.001,        0,        0,       0,    0,    0,    0,    0,     0,     0,
//                                          0,        0,        0,       0,    0,    0,    0,    0,     0,     0,
//                                          0,        0,        0,       0,    0,    0,    0,    0,     0,     0,
//                                          0,        0,        0,       0,    0,    0,    0,    0,     0,     0,
//                                          0,        0,        0,       0,    0                                 };

//  DATA v0 (directly use the vtx distribution)
//  Float_t pileup_2010_data[55] =  {0.445765   , 0.325963  , 0.150328  , 0.0544768, 0.0170244, 0.0047958, 0.00125272, 0.000305422, 6.85045e-05, 1.64857e-05,
//                                   3.49605e-06,6.93182e-07,3.01384e-08,         0,         0,         0,          0,           0,           0,           0,
//                                             0,          0,          0,         0,         0,         0,          0,           0,           0,           0,
//                                             0,          0,          0,         0,         0,         0,          0,           0,           0,           0,
//                                             0,          0,          0,         0,         0,         0,          0,           0,           0,           0,
//                                             0,          0,          0,         0,         0                                                               };

////  DATA v1 (iteration by assuming N_vtx ~ N_interaction +1)  (pt55)
//Double_t pileup_2010_data[55] =  {0.3107949642,0.3158648963,0.1988510444,0.1022362782,0.0451684254,0.0164989962,0.0067749179,0.0029168596,0.0006234523,0.0001563622,
//                                  0.0000398837,0.0000724060,0.0000015135,           0,           0,           0,           0,           0,           0,           0,
//                                             0,           0,           0,           0,           0,           0,           0,           0,           0,           0,
//                                             0,           0,           0,           0,           0,           0,           0,           0,           0,           0,
//                                             0,           0,           0,           0,           0,           0,           0,           0,           0,           0,
//                                             0,           0,           0,           0,           0                                                                  };


//  DATA v2 (iteration by assuming N_vtx ~ N_interaction +1)  (pt75)
Double_t pileup_2010_data[55] =  {0.1585671246,0.2866536524,0.1974529591,0.1736262510,0.1377345936,0.0107313691,0.0219496568,0.0109572709,0.0003254841,0.0012740217,
                                  0.0006768534,0.0000507634,           0,           0,           0,           0,           0,           0,           0,           0,
                                             0,           0,           0,           0,           0,           0,           0,           0,           0,           0,
                                             0,           0,           0,           0,           0,           0,           0,           0,           0,           0,
                                             0,           0,           0,           0,           0,           0,           0,           0,           0,           0,
                                             0,           0,           0,           0,           0                                                                  };


  // Flat10+Tail distribution taken directly from MixingModule input:  (Can be used for Spring11 and Summer11 if you don't worry about small shifts in the mean) SHOULD be used
Double_t probdistFlat10[55] = {0.06640010,0.07909570,0.06750980,0.07174610,0.06976400,0.09529710,0.10112800,0.07829490,0.06375080,0.06273190,0.05763280,
                               0.05216420,0.04186060,0.02868950,0.02471460,0.01743060,0.01117600,0.00658406,0.00215448,0.00121692,0.00065769,         0,
                                        0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,
                                        0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,
                                        0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,
                                                                                                                                                         };


  // MC pile-up scenery S3 & S4 (in-time weighting)
//Double_t  pileup_summer11_MC_S3_S4[55] = {0.11722200,0.06520360,0.07022980,0.07056640,0.06953540,0.06858600,0.06732180,0.06400950,0.06317520,0.05849620,0.05317400,
//                                          0.04672380,0.04031370,0.03456010,0.02802780,0.02220120,0.01696230,0.01306680,0.00972250,0.00680845,0.00479307,0.00331416,
//	                                  0.00217729,0.00147490,0.00087449,0.00056782,0.00032534,0.00024342,0.00013166,0.00007984,0.00003845,0.00003179,0.00001475,
//	                                  0.00000970,0.00001081,0.00000208,0.00000126,0.00000007,         0,         0,         0,         0,         0,         0,
//	                                           0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,
//	                                                                                                                                                            };


  // MC pile-up scenery S4, distribution obtained by averaging the number of interactions
//  Float_t pileup_summer11_MC_S4_avg[55] = {0.104109   ,0.0703573,0.0698445,0.0698254,0.0697054,0.0697907 ,0.0696751,0.0694486 ,0.0680332 ,0.0651044 ,0.0598036 ,0.0527395  ,
//                                           0.0439513  ,0.0352202,0.0266714,0.019411 ,0.0133974,0.00898536,0.0057516,0.00351493,0.00212087,0.00122891,0.00070592,0.000384744,
//                                           0.000219377,         0,       0,        0,        0,         0,        0,         0,         0,         0,         0,          0,
//       				                     0,         0,       0,        0,        0,         0,        0,         0,         0,         0,         0,          0,
//                                                     0,         0,       0,        0,        0,         0,        0,                                                        };                      


  int n_pu = ave_nvtx;
  if (have_PILEUP) {
    if (n_pu<22) pu_reweight = pileup_2010_data[n_pu]/probdistFlat10[n_pu];               // flat10+tail
    //if (n_pu<44) pu_reweight = pileup_2010_data[n_pu]/pileup_summer11_MC_S3_S4[n_pu];     //the maximum number of interaction for S3 & S4 have is 35 
    //if (n_pu<55) pu_reweight = pileup_2010_data[n_pu]/pileup_summer11_MC_S4_avg[n_pu];
    else pu_reweight = 0.;
  }

  pile_up_weight = pu_reweight;
  pile_up_weight_RAW = pu_reweight;
  //pu_reweight = 1.;   //to get no pile-up reweight distribution

  // access trigger bits by TriggerResults

  bool hltAccept(false);

  int hltRunRange_2011data = 0;

  edm::Handle<edm::TriggerResults> hltresults;
  try{e.getByLabel(edm::InputTag("TriggerResults::HLT"), hltresults);}
  //try{iEvent.getManyByType(hltresults);}
  catch(...){std::cout<<"The HLT Trigger branch was not correctly taken"<<std::endl;}

  if (e.getByLabel(edm::InputTag("TriggerResults::HLT"), hltresults) )
   {
     edm::TriggerNames const& triggerNames = e.triggerNames(*hltresults);
     int n_TriggerResults( hltresults.product()->size() );
     //     cout<< n_TriggerResults<<"dimensione"<<endl;
     for (int itrig = 0; itrig != n_TriggerResults; ++itrig){
       std::string trigName = triggerNames.triggerName(itrig);
       bool accept = hltresults->accept((const unsigned int )itrig);
       //             cout << "HLT " << itrig << "  " << trigName << "accettato"<<accept <<endl;
       if (accept){
         //cout<<trigName.c_str()<<endl;
	 if (isMC){
	    //if (trigName == "HLT_Photon50_CaloIdVL_IsoL_v1") hltAccept = true;
	    hltAccept = true;
	  }
         if (is2010DATA){
             if ( runNumber >= 138564 && runNumber <= 143962 && trigName == "HLT_Photon20_Cleaned_L1R" )  // Range I
               {
		hltAccept = true;
		hltRunRange_2010data_RAW = 1;
		hltRunRange_2010data = 1;
               }
             if ( runNumber >= 144010 && runNumber <= 147116 && trigName == "HLT_Photon30_Cleaned_L1R")  // Range II
               {
		hltAccept = true;
		hltRunRange_2010data_RAW = 2;
                hltRunRange_2010data = 2;
               }
             if ( runNumber >= 147196 && runNumber <= 148058 && trigName == "HLT_Photon50_Cleaned_L1R_v1")  // Range III
               {
		hltAccept = true;
		hltRunRange_2010data_RAW = 3;
                hltRunRange_2010data = 3;
               }
             if ( runNumber >= 148822 && runNumber <= 149294 && trigName == "HLT_Photon70_Cleaned_L1R_v1")  // Range IV
               {
		hltAccept = true;
		hltRunRange_2010data_RAW = 4;
                hltRunRange_2010data = 4;
               }
          }
//         if (is2010DATA){
//             if ( runNumber >= 138564 && runNumber <= 141881 )  // Range I
//               {
//                if (trigName == "HLT_Photon20_Cleaned_L1R") hltAccept = true;
//               }
//             if ( runNumber >= 141956 && runNumber <= 144114 )  // Range II
//               {
//                if (trigName == "HLT_Photon50_Cleaned_L1R") hltAccept = true;
//               }
//             if ( runNumber >= 146428 && runNumber <= 147116 )  // Range III
//               {
//                if (trigName == "HLT_Photon50_NoHE_Cleaned_L1R") hltAccept = true;
//               }
//             if ( runNumber >= 147196 && runNumber <= 148058 )  // Range IV
//               {
//                if (trigName == "HLT_Photon50_Cleaned_L1R_v1") hltAccept = true;
//               }
//             if ( runNumber >= 148822 && runNumber <= 149294 )  // Range V
//               {
//                if (trigName == "HLT_Photon50_Cleaned_L1R_v1") hltAccept = true;
//               }
//          }
         if (is2011DATA){
             if ( runNumber >= 160431 && runNumber <= 173692 && trigName == "HLT_Photon30_CaloIdVL_v1-7" )
               {
                hltAccept = true;
                hltRunRange_2011data = 1;
               }
             if ( runNumber >= 160431 && runNumber <= 165087 && trigName == "HLT_Photon30_CaloIdVL_v1-3" )
               {
                hltAccept = true;
                hltRunRange_2011data = 2;
               }
             if ( runNumber >= 165088 && runNumber <= 173692 && trigName == "HLT_Photon50_CaloIdVL_v1-4" )
               {
                hltAccept = true;
                hltRunRange_2011data = 2;
               }
             if ( runNumber >= 160431 && runNumber <= 173692 && trigName == "HLT_Photon75_CaloIdVL_v1-7" )
               {
                hltAccept = true;
                hltRunRange_2011data = 3;
               }
             if ( runNumber >= 160431 && runNumber <= 165087 && trigName == "HLT_Photon75_CaloIdVL_v1-3" )
               {
                hltAccept = true;
                hltRunRange_2011data = 4;
               }
             if ( runNumber >= 165088 && runNumber <= 173692 && trigName == "HLT_Photon90_CaloIdVL_v1-4" )
               {
                hltAccept = true;
                hltRunRange_2011data = 4;
               }
             if ( runNumber >= 160431 && runNumber <= 165087 && trigName == "HLT_Photon75_CaloIdVL_v1-3" )
               {
                hltAccept = true;
                hltRunRange_2011data = 5;
               }
             if ( runNumber >= 165088 && runNumber <= 166967 && trigName == "HLT_Photon125_v1-2" )
               {
                hltAccept = true;
                hltRunRange_2011data = 5;
               }
             if ( runNumber >= 167039 && runNumber <= 173692 && trigName == "HLT_Photon135_v1-2" )
               {
                hltAccept = true;
                hltRunRange_2011data = 5;
               }
          }

       }
       //else {HLT[itrig] = "NULL";}
     }
   }


  //Primary Vertex
  //primary vertex extraction --------------------------------------------------------------------------

  vtx_ = Point(0.,0.,0.);
 
  edm::Handle<reco::VertexCollection> primaryVertexHandle;
  e.getByLabel("offlinePrimaryVertices",primaryVertexHandle);

  std::vector<reco::Vertex> vertexVector;
  vertexVector.clear();
  for (reco::VertexCollection::const_iterator itv=primaryVertexHandle->begin(); itv!=primaryVertexHandle->end(); ++itv){
    vertexVector.push_back(*itv);
  }

  std::stable_sort(vertexVector.begin(), vertexVector.end(), VertexPtSumSort());

  if(vertexVector.size()>0){

    int ipv=0;
    for(reco::VertexCollection::const_iterator it = vertexVector.begin(), ed = vertexVector.end();
        it != ed; ++it) {

       reco::Vertex pv;
       pv = (*it);

       double vtx_rho = sqrt(pv.x()*pv.x()+pv.y()*pv.y());

       if ( !(pv.isFake()) && pv.ndof()>4 && TMath::Abs(pv.z())<24 && vtx_rho < 2 )
        {
          if (ipv==0) {
            vtx_ = Point(pv.x(),pv.y(),pv.z());
          }
          ipv++;
          break;
        }
    }
  }

  // reco level: photon & jets objects calling

  std::vector<reco::Photon> PhotonContainer;
  //std::vector<reco::PFJet> NOcutPFJetContainer;
  std::vector<reco::PFJet> LOOSEPFJetContainer;
  std::vector<reco::PFJet> TIGHTPFJetContainer;

  PhotonContainer.clear();
  //NOcutPFJetContainer.clear();
  LOOSEPFJetContainer.clear();
  TIGHTPFJetContainer.clear();

// //particle flow jet without any jet ID selection
// if ( e.getByLabel( pfJetCollName, NOcutPFJetsHandle ) )
//     {
//       for(reco::PFJetCollection::const_iterator itbegin(NOcutPFJetsHandle->begin()), itEnd(NOcutPFJetsHandle->end()), itjet = itbegin;
//           itjet!=itEnd;++itjet)
//         {
//           NOcutPFJetContainer.push_back(*itjet);
//         } 
//       std::stable_sort(NOcutPFJetContainer.begin(),NOcutPFJetContainer.end(),PFJetSort());
//     }
//
  //particle flow jet with "loose" jet ID selection
  if ( e.getByLabel( pfJetCollName, LOOSEPFJetsHandle ) )
      {
        if(LOOSEPFJetsHandle->size())
          {
            // jet ID selection
            PFJetIDSelectionFunctor jetIDFunctor( PFJetIDSelectionFunctor::FIRSTDATA, PFJetIDSelectionFunctor::LOOSE ); // this line can be done once, in a constructor or such
            pat::strbitset ret = jetIDFunctor.getBitTemplate(); // Only needed if you plan to use the detailed return values (see Selector docs)
  
            //unsigned int idx;
 
            for(reco::PFJetCollection::const_iterator itbegin(LOOSEPFJetsHandle->begin()), itEnd(LOOSEPFJetsHandle->end()), itjet = itbegin;
                itjet!=itEnd;++itjet)
              {
 
                //idx = itjet - itbegin;
                //edm::RefToBase<reco::PFJet> jetRef = itjet->refAt(idx);
                //reco::JetID const & jetId = (*hJetIDMap)[ jetRef ];
 
        	//if(!itjet->isPFJet()) continue;
 
        	ret.set(false);
        	bool passed = jetIDFunctor( *itjet, ret );
 
                if(passed){
        	    LOOSEPFJetContainer.push_back(*itjet);
                }
              } 
            std::stable_sort(LOOSEPFJetContainer.begin(),LOOSEPFJetContainer.end(),PFJetSort());
          }
      }

  //particle flow jet with "tight" jet ID selection
  if ( e.getByLabel( pfJetCollName, TIGHTPFJetsHandle ) )
      {
        if(TIGHTPFJetsHandle->size())
          {
            // jet ID selection
            PFJetIDSelectionFunctor jetIDFunctor( PFJetIDSelectionFunctor::FIRSTDATA, PFJetIDSelectionFunctor::TIGHT ); // this line can be done once, in a constructor or such
            pat::strbitset ret = jetIDFunctor.getBitTemplate(); // Only needed if you plan to use the detailed return values (see Selector docs)
  
            //unsigned int idx;

            for(reco::PFJetCollection::const_iterator itbegin(TIGHTPFJetsHandle->begin()), itEnd(TIGHTPFJetsHandle->end()), itjet = itbegin;
                itjet!=itEnd;++itjet)
              {

                //idx = itjet - itbegin;
                //edm::RefToBase<reco::PFJet> jetRef = itjet->refAt(idx);
                //reco::JetID const & jetId = (*hJetIDMap)[ jetRef ];

		ret.set(false);
		bool passed = jetIDFunctor( *itjet, ret );

                if(passed){
		    TIGHTPFJetContainer.push_back(*itjet);
                }
              } 
            std::stable_sort(TIGHTPFJetContainer.begin(),TIGHTPFJetContainer.end(),PFJetSort());
          }
      }


  //RECO-photon
  if (e.getByLabel(photonProducer_, photons))
   {
     if (photons->size()){
          Photon photon;
	  for ( reco::PhotonCollection::const_iterator it(photons->begin()), itEnd(photons->end());
			  it!=itEnd; ++it)
	  {
            photon = (*it);
            photon.setVertex(vtx_);
	    PhotonContainer.push_back(photon);
	  }
	  std::stable_sort(PhotonContainer.begin(),PhotonContainer.end(),PhotonSort());
     }
   }

  
  //
  // dS and dPhi for Reco-level
  //

  // 2nd_pv selection
  bool Cut1_2nd_primary_vtx = true;
  bool Cut2_2nd_primary_vtx = false;

  int number_vertex = 0;
  vector<double> pv_ptsum_track;
  pv_ptsum_track.clear();

  if ( vertexVector.size() > 0 )  
  for(reco::VertexCollection::const_iterator it_vtx = vertexVector.begin(), itend_vtx = vertexVector.end(); it_vtx != itend_vtx; ++it_vtx)
    {
      reco::Vertex pvtx;
      pvtx = (*it_vtx);

      b_vtx_x.push_back(pvtx.x());
      b_vtx_y.push_back(pvtx.y());
      b_vtx_z.push_back(pvtx.z());

      double d0_ = sqrt(pvtx.x()*pvtx.x()+pvtx.y()*pvtx.y());
      b_vtx_d0.push_back(d0_);

      double dz_ = pvtx.z();
      b_vtx_z.push_back(dz_);

      int ndof_  = pvtx.ndof();
      b_vtx_ndof.push_back(ndof_);

      //cout<<"ndof ="<<ndof_<<endl;
      //cout<<"d0 ="<< d0_ <<endl;
      //cout<<"dz " << dz_ <<endl;
  
      double pvtx_ptsum = 0; 

      if ( d0_ < 2 && dz_ < 24 && ndof_ > 4  )
       {
         for(reco::Vertex::trackRef_iterator pvt = pvtx.tracks_begin(); pvt!= pvtx.tracks_end(); pvt++){
           const reco::Track & track = *pvt->get();
	   pvtx_ptsum += track.pt()*track.pt();
	 } 

	 b_vtx_ptsum_track.push_back(pvtx_ptsum);
         pv_ptsum_track.push_back(pvtx_ptsum);
         number_vertex++;
       }
    }

  n_vertex_RAW = number_vertex;

  // 2nd Vtx info.
  if ( number_vertex == 0 ) {
    trkPt_squareSum_1stVtx_RAW = -1;
    trkPt_squareSum_2ndVtx_RAW = -1;
    trkPt_squareSum_3rdVtx_RAW = -1;
    trkPt_squareSum_1stVtx = -1;
    trkPt_squareSum_2ndVtx = -1;
    trkPt_squareSum_3rdVtx = -1;
  }

  if (Cut1_2nd_primary_vtx){
     if ( number_vertex > 1 ) {
       trkPt_squareSum_1stVtx_RAW =  pv_ptsum_track[0];
       trkPt_squareSum_2ndVtx_RAW =  pv_ptsum_track[1];
       trkPt_squareSum_2ndVtx_RAW =  0;
       trkPt_squareSum_1stVtx =  pv_ptsum_track[0];
       trkPt_squareSum_2ndVtx =  pv_ptsum_track[1];
       trkPt_squareSum_3rdVtx =  0;
     }
     else if ( number_vertex > 2 ) {
       trkPt_squareSum_1stVtx_RAW =  pv_ptsum_track[0];
       trkPt_squareSum_2ndVtx_RAW =  pv_ptsum_track[1];
       trkPt_squareSum_3rdVtx_RAW =  pv_ptsum_track[2];
       trkPt_squareSum_1stVtx =  pv_ptsum_track[0];
       trkPt_squareSum_2ndVtx =  pv_ptsum_track[1];
       trkPt_squareSum_3rdVtx =  pv_ptsum_track[2];
     }
     else if ( number_vertex == 1 ) {
       trkPt_squareSum_1stVtx_RAW =  pv_ptsum_track[0];
       trkPt_squareSum_2ndVtx_RAW = 0;
       trkPt_squareSum_3rdVtx_RAW = 0;
       trkPt_squareSum_1stVtx =  pv_ptsum_track[0];
       trkPt_squareSum_2ndVtx = 0;
       trkPt_squareSum_3rdVtx = 0;
     }
  }

  // 2nd Vtx selection for histograms
  if ( number_vertex == 0 ) Cut1_2nd_primary_vtx = false;

  if (Cut1_2nd_primary_vtx){
     if ( number_vertex > 1 && pv_ptsum_track[1] < 10. ) Cut2_2nd_primary_vtx = true;
     else if ( number_vertex == 1 ) Cut2_2nd_primary_vtx = true;
  }

  if (Cut1_2nd_primary_vtx){
    selection_number_RAW = 1;
  }


  // All event analysis
  bool find_Photon = false;
  int passed_photon = 0;

  std::vector<reco::Photon>::const_iterator it_photon_RAW(PhotonContainer.begin()), itEnd_photon_RAW(PhotonContainer.end());

  edm::Handle<EcalRecHitCollection> EBReducedRecHits;
  e.getByLabel(ebReducedRecHitCollection_, EBReducedRecHits);
  edm::Handle<EcalRecHitCollection> EEReducedRecHits;
  e.getByLabel(eeReducedRecHitCollection_, EEReducedRecHits);
  // get the channel status from the DB
  edm::ESHandle<EcalChannelStatus> chStatus;
  iSetup.get<EcalChannelStatusRcd>().get(chStatus);

  EcalClusterLazyTools lazyTool(e, iSetup, ebReducedRecHitCollection_, eeReducedRecHitCollection_ );

  for( int i_Photon(0); it_photon_RAW != itEnd_photon_RAW; ++it_photon_RAW, ++i_Photon ){
  
        const reco::CaloClusterPtr  seed = (*it_photon_RAW).superCluster()->seed();

        DetId id = lazyTool.getMaximum(*seed).first;
        const EcalRecHitCollection & rechits = ( it_photon_RAW->isEB() ? *EBReducedRecHits : *EEReducedRecHits);
        EcalRecHitCollection::const_iterator it_EcalRecHit = rechits.find( id );

        float time  = -999., outOfTimeChi2 = -999., chi2 = -999.;
        int   flags=-1;
        float seedAppEt=-999.;

        if( it_EcalRecHit != rechits.end() ) {
              time = it_EcalRecHit->time();
              outOfTimeChi2 = it_EcalRecHit->outOfTimeChi2();
              chi2     = it_EcalRecHit->chi2();
              flags    = it_EcalRecHit->recoFlag();
              seedAppEt = (id.subdetId() == EcalBarrel)?
                it_EcalRecHit->energy()/ cosh( EBDetId::approxEta( id ) ):0;
        }


        vector<float> viCov;
        viCov = lazyTool.localCovariances(*seed);
  
        double pT_photon ( it_photon_RAW->pt()  );
        if (is2010DATA) pT_photon = pT_photon*(1-0.0043); //photon energy scale for 2010 data

        double eta_photon( it_photon_RAW->eta() );

        double et_photon ( it_photon_RAW->et()  );
        if (is2010DATA) et_photon = et_photon*(1-0.0043); //photon energy scale for 2010 data

        double energy_photon ( it_photon_RAW->energy()  );
        if (is2010DATA) energy_photon = energy_photon*(1-0.0043); //photon energy scale for 2010 data
  
        double scEta( it_photon_RAW->superCluster()->eta() );
        double scPhi( it_photon_RAW->superCluster()->phi() );
  
        double sigmaIetaIeta ( it_photon_RAW->sigmaIetaIeta()           );
        double sigmaIphiIphi ( sqrt(viCov[2])         		 );
        double sigmaIetaIphi ( sqrt(viCov[1])                       );
        double hadronicOverEm( it_photon_RAW->hadronicOverEm()          );
        double trackIso      ( it_photon_RAW->trkSumPtHollowConeDR04()  );
        double ecalIso       ( it_photon_RAW->ecalRecHitSumEtConeDR04() );
        double hcalIso       ( it_photon_RAW->hcalTowerSumEtConeDR04()  );
        int    hasPixelSeed  ( it_photon_RAW->hasPixelSeed()            );
  
        if( TMath::Abs(scEta) > 5.0 ) continue;
        if( pT_photon < 10. ) continue;

	find_Photon = true;
   	passed_photon++;
        b_photonEt.push_back(et_photon);
        b_photonEta.push_back(eta_photon);
        b_photonPhi.push_back(it_photon_RAW->phi());
	b_photonEnergy.push_back(energy_photon);
        b_photonScEta.push_back(scEta);
        b_photonScPhi.push_back(scPhi);
        b_photonSigmaIetaIeta.push_back(sigmaIetaIeta);
        b_photonSigmaIphiIphi.push_back(sigmaIphiIphi);
        b_photonSigmaIetaIphi.push_back(sigmaIetaIphi);
        b_photonHadronicOverEm.push_back(hadronicOverEm);
        b_photonTrackIso.push_back(trackIso);
        b_photonEcalIso.push_back(ecalIso);
        b_photonHcalIso.push_back(hcalIso);
        b_photonHasPixelSeed.push_back(hasPixelSeed);
        b_photonSeedTime.push_back(time);

  }

  cout<<passed_photon<<endl;



  // DPS event tag, 1->YES, 0->NO
  is_DPS_event = 0;

  double S_CDFpt_reco = 99999.;
  double dS_reco = 99999.;

  bool find_dS_reco = false;

  bool find_leadingPhoton = false;
  bool find_1st_jet = false;
  bool find_2nd_jet = false;
  bool find_3rd_jet = false;

  int cut_hlt (0);
  int cut_2nd_pvtx (0);
  int cut_photon_pTeta (0);
  int cut_photonID (0);

  TLorentzVector leadingPhoton;

  TLorentzVector S_CDFpt_leadingPhoton;

  std::vector<reco::Photon>::const_iterator it_photon(PhotonContainer.begin()), itEnd_photon(PhotonContainer.end());

//  edm::Handle<EcalRecHitCollection> EBReducedRecHits;
//  e.getByLabel(ebReducedRecHitCollection_, EBReducedRecHits);
//  edm::Handle<EcalRecHitCollection> EEReducedRecHits;
//  e.getByLabel(eeReducedRecHitCollection_, EEReducedRecHits);
//  // get the channel status from the DB
//  edm::ESHandle<EcalChannelStatus> chStatus;
//  iSetup.get<EcalChannelStatusRcd>().get(chStatus);

//  EcalClusterLazyTools lazyTool(e, iSetup, ebReducedRecHitCollection_, eeReducedRecHitCollection_ );

  //hltAccept = true;   //for trigger efficiency study

  if(Cut1_2nd_primary_vtx)
  if(hltAccept){
     cut_hlt++;
     //if(Cut2_2nd_primary_vtx){
       //cut_2nd_pvtx++;
       for( int i_Photon(0); it_photon != itEnd_photon; ++it_photon, ++i_Photon ){
     
	     const reco::CaloClusterPtr  seed = (*it_photon).superCluster()->seed();

             DetId id = lazyTool.getMaximum(*seed).first;
             const EcalRecHitCollection & rechits = ( it_photon->isEB() ? *EBReducedRecHits : *EEReducedRecHits);
             EcalRecHitCollection::const_iterator it_EcalRecHit = rechits.find( id );

             float time  = -999., outOfTimeChi2 = -999., chi2 = -999.;
             int   flags=-1;
             float seedAppEt=-999.;

             if( it_EcalRecHit != rechits.end() ) {
                   time = it_EcalRecHit->time();
                   outOfTimeChi2 = it_EcalRecHit->outOfTimeChi2();
                   chi2     = it_EcalRecHit->chi2();
                   flags    = it_EcalRecHit->recoFlag();
                   seedAppEt = (id.subdetId() == EcalBarrel)?
                     it_EcalRecHit->energy()/ cosh( EBDetId::approxEta( id ) ):0;
             }


             vector<float> viCov;
             viCov = lazyTool.localCovariances(*seed);
     
             double pT_photon ( it_photon->pt()  );
	     if (is2010DATA) pT_photon = pT_photon*(1-0.0043); //photon energy scale for 2010 data

             double eta_photon( it_photon->eta() );

 	     double et_photon ( it_photon->et()  );
	     if (is2010DATA) et_photon = et_photon*(1-0.0043); //photon energy scale for 2010 data
     
             double scEta( it_photon->superCluster()->eta() );
             double scPhi( it_photon->superCluster()->phi() );
     
             double sigmaIetaIeta ( it_photon->sigmaIetaIeta()           );
             double sigmaIphiIphi ( sqrt(viCov[2])         		 );
             double sigmaIetaIphi ( sqrt(viCov[1])                       );
             double hadronicOverEm( it_photon->hadronicOverEm()          );
             double trackIso      ( it_photon->trkSumPtHollowConeDR04()  );
             double ecalIso       ( it_photon->ecalRecHitSumEtConeDR04() );
             double hcalIso       ( it_photon->hcalTowerSumEtConeDR04()  );
             int    hasPixelSeed  ( it_photon->hasPixelSeed()            );
     
             if( TMath::Abs(scEta) > 5.0 ) continue;
             if( pT_photon < 30. ) continue;
             cut_photon_pTeta++;     

             leadingPhoton.SetPxPyPzE(it_photon->px(),it_photon->py(),it_photon->pz(),it_photon->energy());

	     if (!onlyRECO){
  
               e.getByLabel( genPartCollName   , CandHandleMCGamma_forMatch );     //photon-> for gen-Iso calculation          
               std::vector<GenParticle> GenGamma_forMatch;           
               GenGamma_forMatch.clear();
           
               //Gen-Photon
               if (CandHandleMCGamma_forMatch->size()){
                for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma_forMatch->begin()), it_gen_End(CandHandleMCGamma_forMatch->end());
                it_gen != it_gen_End;it_gen++)
                  {
                    const reco::Candidate &p = (*it_gen);
                    if (p.numberOfMothers() < 1) continue;
                    if (p.status() != 1) continue;
                    if (abs(p.pdgId()) != 22) continue;        //for Dijet events
                    GenGamma_forMatch.push_back(*it_gen);
                  }
           
                std::stable_sort(GenGamma_forMatch.begin(),GenGamma_forMatch.end(),GenPhotonSort());
               }
             }

             if(is2011DATA){
              if(hltRunRange_2011data==1&&(pT_photon<40||pT_photon>60)){
               cut_photon_pTeta = 0;
               continue;
              }
              if(hltRunRange_2011data==2&&(pT_photon<60||pT_photon>85)){
               cut_photon_pTeta = 0;
               continue;
              }
              if(hltRunRange_2011data==3&&(pT_photon<85||pT_photon>100)){
               cut_photon_pTeta = 0;
               continue;
              }
              if(hltRunRange_2011data==4&&(pT_photon<100||pT_photon>145)){
               cut_photon_pTeta = 0;
               continue;
              }
              if(hltRunRange_2011data==5&&(pT_photon<145||pT_photon>300)){
               cut_photon_pTeta = 0;
               continue;
              }
             }

             // photon ID selection
             if ( trackIso >= 2.0+0.001*et_photon ) continue;    // 2.0+0.001*et_photon for loose; 0.9 for tight
             //if ( trackIso < 2.0+0.001*et_photon || trackIso > 5.0+0.001*et_photon ) continue;    // for data side-band
             if ( ecalIso  >= 4.2+0.003*et_photon ) continue;    // 4.2+0.003*et_photon for loose; 2.4 for tight
             if ( hcalIso  >= 2.2+0.001*et_photon ) continue;    // 2.2+0.001*et_photon for loose; 1.0 for tight
             
	     if ( hadronicOverEm >= 0.05 ) continue;   // 0.05 for loose; 0.03 for tight
             if ( (TMath::Abs(scEta) < 1.4442) && (sigmaIetaIeta >= 0.01) ) continue; // 0.011 for loose; 0.01 for tight
             if ( (TMath::Abs(scEta) < 2.5 && TMath::Abs(scEta) > 1.566 ) && (sigmaIetaIeta >= 0.03) ) continue; // 0.03 for loose; 0.028 for tight
     
             if ( hasPixelSeed != 0 ) continue; 

	     if ( sigmaIphiIphi <= 0.009 ) continue;    //spike-removal cuts
	     if ( TMath::Abs(time) > 1.5 ) continue;    //spike-removal cuts
               
             cut_photonID++;

	     leadingPhoton.SetPxPyPzE(it_photon->px(),it_photon->py(),it_photon->pz(),it_photon->energy());
             if (is2010DATA) leadingPhoton.SetPxPyPzE(it_photon->px()*(1-0.0043),it_photon->py()*(1-0.0043),it_photon->pz()*(1-0.0043),it_photon->energy()*(1-0.0043));

             find_leadingPhoton = true;
             leadingPhoton_scEta = scEta;
             leadingPhoton_scPhi = scPhi;
	     leadingPhoton_SigmaIetaIeta = sigmaIetaIeta;
             leadingPhoton_SigmaIphiIphi = sigmaIphiIphi;
             leadingPhoton_SigmaIetaIphi = sigmaIetaIphi;
             leadingPhoton_HadronicOverEm = hadronicOverEm;
             leadingPhoton_TrackIso = trackIso;
             leadingPhoton_EcalIso = ecalIso;
             leadingPhoton_HcalIso = hcalIso;
             leadingPhoton_HasPixelSeed = hasPixelSeed;
             leadingPhoton_SeedTime = time;

             break;	 
       }
     //}
  }

  if(cut_hlt){
    selection_number_RAW = 2;
  }
  if(cut_photon_pTeta){
    selection_number_RAW = 3;
  }
  if(cut_photonID){
    selection_number_RAW = 4;
  }


  TLorentzVector leading_1stjet;
  TLorentzVector leading_2ndjet;
  TLorentzVector leading_3rdjet;

  double jecUnc_jet( 0 );
  double jecUnc_1stjet ( 0 );
  double jecUnc_2ndjet ( 0 );
  double jecUnc_3rdjet ( 0 );

  TLorentzVector S_CDFpt_leading_1stjet;
  TLorentzVector S_CDFpt_leading_2ndjet;
  TLorentzVector S_CDFpt_leading_3rdjet;

  double S_CDFpt_jecUnc_1stjet ( 0 );
  double S_CDFpt_jecUnc_2ndjet ( 0 );
  double S_CDFpt_jecUnc_3rdjet ( 0 );


  int orderOf1stLeadingJet ( 0 );
  int orderOf2ndLeadingJet ( 0 );
  int orderOf3rdLeadingJet ( 0 );

  double sumOfsquare_pt_GJ1 ( 0 );
  double sumOfsquare_pt_J2J3( 0 );
  double sumOfsquare_pt_GJ2 ( 0 );
  double sumOfsquare_pt_J1J3( 0 );
  double sumOfsquare_pt_GJ3 ( 0 );
  double sumOfsquare_pt_J1J2( 0 );
  double err_pt_GJ1 ( 0 );
  double err_pt_J2J3 ( 0 );
  double err_pt_GJ2 ( 0 );
  double err_pt_J1J3 ( 0 );
  double err_pt_GJ3 ( 0 );
  double err_pt_J1J2 ( 0 );

  int cut_jetcleaning_1stjet (0);
  int cut_1stjetvertex (0);
  int cut_1stjet_pTeta (0);
  int cut_jetcleaning_2ndjet (0);
  int cut_2ndjetvertex (0);
  int cut_2ndjet_pTeta (0);
  int cut_jetcleaning_3rdjet (0);
  int cut_3rdjetvertex (0);
  int cut_3rdjet_pTeta (0);

  int i_PFJet (0);
  int j_PFJet (0);
  int k_PFJet (0);

  double dphi_1 (0);
  double deta_1 (0);
  double dR_1 (0);
  double dphi_2 (0);
  double deta_2 (0);
  double dR_2 (0);
  double dphi_3 (0);
  double deta_3 (0);
  double dR_3 (0);

  double chf_1stjet = 0;
  double nhf_1stjet = 0;
  double cef_1stjet = 0;
  double nef_1stjet = 0;
  double nch_1stjet = 0;
  double nconstituents_1stjet = 0;
  double chf_2ndjet = 0;
  double nhf_2ndjet = 0;
  double cef_2ndjet = 0;
  double nef_2ndjet = 0;
  double nch_2ndjet = 0;
  double nconstituents_2ndjet = 0;
  double chf_3rdjet = 0;
  double nhf_3rdjet = 0;
  double cef_3rdjet = 0;
  double nef_3rdjet = 0;
  double nch_3rdjet = 0;
  double nconstituents_3rdjet = 0;


// //uncertainty of the jet energy correction
 edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
 iSetup.get<JetCorrectionsRecord>().get("AK5PF",JetCorParColl);
 JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
 JetCorrectionUncertainty *jecUnc = new JetCorrectionUncertainty(JetCorPar);

  //three kinds of pfjets can be used for jet selection

  //std::vector<reco::PFJet>::const_iterator it_jet1(NOcutPFJetContainer.begin()), itEnd_jet1(NOcutPFJetContainer.end());
  //std::vector<reco::PFJet>::const_iterator it_jet2(NOcutPFJetContainer.begin()), itEnd_jet2(NOcutPFJetContainer.end());
  //std::vector<reco::PFJet>::const_iterator it_jet3(NOcutPFJetContainer.begin()), itEnd_jet3(NOcutPFJetContainer.end());

  std::vector<reco::PFJet>::const_iterator it_jets(LOOSEPFJetContainer.begin()), itEnd_jets(LOOSEPFJetContainer.end());
  std::vector<reco::PFJet>::const_iterator it_jet1(LOOSEPFJetContainer.begin()), itEnd_jet1(LOOSEPFJetContainer.end());
  std::vector<reco::PFJet>::const_iterator it_jet2(LOOSEPFJetContainer.begin()), itEnd_jet2(LOOSEPFJetContainer.end());
  std::vector<reco::PFJet>::const_iterator it_jet3(LOOSEPFJetContainer.begin()), itEnd_jet3(LOOSEPFJetContainer.end());

  //std::vector<reco::PFJet>::const_iterator it_jets(TIGHTPFJetContainer.begin()), itEnd_jets(TIGHTPFJetContainer.end());
  //std::vector<reco::PFJet>::const_iterator it_jet1(TIGHTPFJetContainer.begin()), itEnd_jet1(TIGHTPFJetContainer.end());
  //std::vector<reco::PFJet>::const_iterator it_jet2(TIGHTPFJetContainer.begin()), itEnd_jet2(TIGHTPFJetContainer.end());
  //std::vector<reco::PFJet>::const_iterator it_jet3(TIGHTPFJetContainer.begin()), itEnd_jet3(TIGHTPFJetContainer.end());

  std::vector<reco::PFJet>::const_iterator it_jets_Loose(LOOSEPFJetContainer.begin()), itEnd_jets_Loose(LOOSEPFJetContainer.end());
  std::vector<reco::PFJet>::const_iterator it_jets_Tight(TIGHTPFJetContainer.begin()), itEnd_jets_Tight(TIGHTPFJetContainer.end());

  // All event
  for ( int i_loosePFJet=1; it_jets_Loose != itEnd_jets_Loose; ++it_jets_Loose, ++i_loosePFJet )
   {

     if (it_jets_Loose->pt() < 5) continue;
     if (TMath::Abs(it_jets_Loose->eta()) > 2.4) continue;

     b_loosejetPt.push_back(it_jets_Loose->pt());
     b_loosejetEta.push_back(it_jets_Loose->eta());
     b_loosejetPhi.push_back(it_jets_Loose->phi());
     b_loosejetEnergy.push_back(it_jets_Loose->energy());

     b_loosejet_association.push_back(JetVertexAssociation(primaryVertexHandle,vertexVector,it_jets_Loose)); 
 
     jecUnc->setJetEta(it_jets_Loose->eta());
     jecUnc->setJetPt(it_jets_Loose->pt());
     b_loosejetJecUnc.push_back(jecUnc->getUncertainty(true));

   }

  for ( int i_tightPFJet=1; it_jets_Tight != itEnd_jets_Tight; ++it_jets_Tight, ++i_tightPFJet )
   {

     if (it_jets_Tight->pt() < 5) continue;
     if (TMath::Abs(it_jets_Tight->eta()) > 2.4) continue;

     b_tightjetPt.push_back(it_jets_Tight->pt());
     b_tightjetEta.push_back(it_jets_Tight->eta());
     b_tightjetPhi.push_back(it_jets_Tight->phi());
     b_tightjetEnergy.push_back(it_jets_Tight->energy());

     b_tightjet_association.push_back(JetVertexAssociation(primaryVertexHandle,vertexVector,it_jets_Tight)); 
 
     jecUnc->setJetEta(it_jets_Tight->eta());
     jecUnc->setJetPt(it_jets_Tight->pt());
     b_tightjetJecUnc.push_back(jecUnc->getUncertainty(true));

   }


  // DPS part
  TLorentzVector passed_jet;
  double dphi_passed (0);
  double deta_passed (0);
  double dR_passed (0);

  double multiplicity_jets_pt20 = 0;
  double multiplicity_jets_pt75 = 0;

  double jecUnc_passedjet ( 0 );

  //jet selection
  if ( find_leadingPhoton )
  for ( i_PFJet=1; it_jets != itEnd_jets; ++it_jets, ++i_PFJet )
   {
     passed_jet.SetPxPyPzE(it_jets->px(), it_jets->py(), it_jets->pz(), it_jets->energy());

     dphi_passed = leadingPhoton.Phi() - passed_jet.Phi();
     if ( dphi_passed < 0 ) dphi_passed = -dphi_passed;
     if ( dphi_passed > TMath::Pi() ) dphi_passed = 2*TMath::Pi() - dphi_passed;
     deta_passed = leadingPhoton.Eta() - passed_jet.Eta();
     dR_passed = sqrt((dphi_passed)*(dphi_passed)+(deta_passed)*(deta_passed));

     if ( dR_passed > 0.5 ) {

         if( JetVertexAssociation(primaryVertexHandle,vertexVector,it_jets) != 0 ) continue;

         jecUnc->setJetEta(passed_jet.Eta());
         jecUnc->setJetPt(passed_jet.Pt()); // here you must use the CORRECTED jet pt
         jecUnc_jet = jecUnc->getUncertainty(true);

         if( TMath::Abs(passed_jet.Eta()) > 2.4 ) continue;
         if( passed_jet.Pt() < 20 ) continue;
         //if( passed_jet.Pt()+jecUnc_jet < 20 ) continue;
         //if( passed_jet.Pt()-jecUnc_jet < 20 ) continue;        

         multiplicity_jets_pt20++;
	 if( passed_jet.Pt() >= 30 ) multiplicity_jets_pt75++; 
         //if( passed_jet.Pt()+jecUnc_jet >= 75 ) multiplicity_jets_pt75++;
         //if( passed_jet.Pt()-jecUnc_jet >= 75 ) multiplicity_jets_pt75++;

         jecUnc->setJetEta(passed_jet.Eta());
         jecUnc->setJetPt(passed_jet.Pt()); // here you must use the CORRECTED jet pt
         jecUnc_passedjet = jecUnc->getUncertainty(true);

     }
   }



  if ( find_leadingPhoton )
  for ( i_PFJet=1; it_jet1 != itEnd_jet1; ++it_jet1, ++i_PFJet )
   {
     leading_1stjet.SetPxPyPzE(it_jet1->px(), it_jet1->py(), it_jet1->pz(), it_jet1->energy());
     orderOf1stLeadingJet = i_PFJet;

     dphi_1 = leadingPhoton.Phi() - leading_1stjet.Phi();
     if ( dphi_1 < 0 ) dphi_1 = -dphi_1;
     if ( dphi_1 > TMath::Pi() ) dphi_1 = 2*TMath::Pi() - dphi_1;
     deta_1 = leadingPhoton.Eta() - leading_1stjet.Eta();
     dR_1 = sqrt((dphi_1)*(dphi_1)+(deta_1)*(deta_1));

     if ( dR_1 > 0.5 ) {
         cut_jetcleaning_1stjet++;

	 if( JetVertexAssociation(primaryVertexHandle,vertexVector,it_jet1) != 0 ) continue;
	 cut_1stjetvertex++;

         jecUnc->setJetEta(leading_1stjet.Eta());
         jecUnc->setJetPt(leading_1stjet.Pt()); // here you must use the CORRECTED jet pt
         jecUnc_1stjet = jecUnc->getUncertainty(true);

         if( TMath::Abs(leading_1stjet.Eta()) > 2.4 ) continue; 
         if( leading_1stjet.Pt() < 30 ) continue;
         //if( leading_1stjet.Pt()+jecUnc_1stjet < 75 ) continue;
	 //if( leading_1stjet.Pt()-jecUnc_1stjet < 75 ) continue;
 	 cut_1stjet_pTeta++;
	
         orderOf1stLeadingJet = i_PFJet;

         chf_1stjet = it_jet1->chargedHadronEnergyFraction();
         nhf_1stjet = (it_jet1->neutralHadronEnergy()+it_jet1->HFHadronEnergy())/it_jet1->energy();
         cef_1stjet = it_jet1->chargedEmEnergyFraction();
         nef_1stjet = it_jet1->neutralEmEnergyFraction();
         nch_1stjet = it_jet1->chargedMultiplicity();
         nconstituents_1stjet = it_jet1->numberOfDaughters();

         find_1st_jet = true;
         // cout << "(pT, eta, phi) =" << leading_1stjet.Pt()<< "," << leading_1stjet.Eta()<< "," << leading_1stjet.Phi() <<endl;
         if( find_1st_jet )
         for ( j_PFJet=1; it_jet2 != itEnd_jet2; ++it_jet2, ++j_PFJet )
          {
            leading_2ndjet.SetPxPyPzE(it_jet2->px(), it_jet2->py(), it_jet2->pz(), it_jet2->energy());

            if( leading_1stjet.Pt() == leading_2ndjet.Pt() && leading_1stjet.Eta() == leading_2ndjet.Eta() && leading_1stjet.Phi() == leading_2ndjet.Phi() ) continue;
	    orderOf2ndLeadingJet = j_PFJet;

            dphi_2 = leadingPhoton.Phi() - leading_2ndjet.Phi();
            if ( dphi_2 < 0 ) dphi_2 = -dphi_2;
            if ( dphi_2 > TMath::Pi() ) dphi_2 = 2*TMath::Pi() - dphi_2;
            deta_2 = leadingPhoton.Eta() - leading_2ndjet.Eta();
            dR_2 = sqrt((dphi_2)*(dphi_2)+(deta_2)*(deta_2));

            if ( dR_2 > 0.5 ) { 
		cut_jetcleaning_2ndjet++;

	        if( JetVertexAssociation(primaryVertexHandle,vertexVector,it_jet2) != 0 ) continue;
                cut_2ndjetvertex++;

	        jecUnc->setJetEta(leading_2ndjet.Eta());
	  	jecUnc->setJetPt(leading_2ndjet.Pt()); // here you must use the CORRECTED jet pt
         	jecUnc_2ndjet = jecUnc->getUncertainty(true);

                if( TMath::Abs(leading_2ndjet.Eta()) > 2.4 ) continue; 
                if( leading_2ndjet.Pt() < 20 ) continue;
                //if( leading_2ndjet.Pt()+jecUnc_2ndjet < 20 ) continue;
                //if( leading_2ndjet.Pt()-jecUnc_2ndjet < 20 ) continue;
		cut_2ndjet_pTeta++;

                orderOf2ndLeadingJet = j_PFJet;

                chf_2ndjet = it_jet2->chargedHadronEnergyFraction();
                nhf_2ndjet = (it_jet2->neutralHadronEnergy()+it_jet2->HFHadronEnergy())/it_jet2->energy();
                cef_2ndjet = it_jet2->chargedEmEnergyFraction();
                nef_2ndjet = it_jet2->neutralEmEnergyFraction();
                nch_2ndjet = it_jet2->chargedMultiplicity();
                nconstituents_2ndjet = it_jet2->numberOfDaughters();

                find_2nd_jet = true;
                //cout << "(pT, eta, phi) =" << leading_2ndjet.Pt()<< "," << leading_2ndjet.Eta()<< "," << leading_2ndjet.Phi() <<endl;
                if ( find_2nd_jet ) {
                   for ( k_PFJet=1; it_jet3 != itEnd_jet3; ++it_jet3, ++k_PFJet )
                    {
                      leading_3rdjet.SetPxPyPzE(it_jet3->px(), it_jet3->py(), it_jet3->pz(), it_jet3->energy());
		      orderOf3rdLeadingJet = k_PFJet;

                      if( leading_1stjet.Pt() == leading_3rdjet.Pt() && leading_1stjet.Eta() == leading_3rdjet.Eta() && leading_1stjet.Phi() == leading_3rdjet.Phi() ) continue;
                      if( leading_2ndjet.Pt() == leading_3rdjet.Pt() && leading_2ndjet.Eta() == leading_3rdjet.Eta() && leading_2ndjet.Phi() == leading_3rdjet.Phi() ) continue;

                      dphi_3 = leadingPhoton.Phi() - leading_3rdjet.Phi();
                      if ( dphi_3 < 0 ) dphi_3 = -dphi_3;
                      if ( dphi_3 > TMath::Pi() ) dphi_3 = 2*TMath::Pi() - dphi_3;
                      deta_3 = leadingPhoton.Eta() - leading_3rdjet.Eta();
                      dR_3 = sqrt((dphi_3)*(dphi_3)+(deta_3)*(deta_3));

                      if ( dR_3 > 0.5 ) {
			  cut_jetcleaning_3rdjet++;

			  if(JetVertexAssociation(primaryVertexHandle,vertexVector,it_jet3) != 0) continue;
	                  cut_3rdjetvertex++;

		          jecUnc->setJetEta(leading_3rdjet.Eta());
		          jecUnc->setJetPt(leading_3rdjet.Pt()); // here you must use the CORRECTED jet pt
		          jecUnc_3rdjet = jecUnc->getUncertainty(true);

                          if( TMath::Abs(leading_3rdjet.Eta()) > 2.4 ) continue;
                          if( leading_3rdjet.Pt() < 20 ) continue; 
                          //if( leading_3rdjet.Pt()+jecUnc_3rdjet < 20 ) continue;
                          //if( leading_3rdjet.Pt()-jecUnc_3rdjet < 20 ) continue;
			  cut_3rdjet_pTeta++;

                          orderOf3rdLeadingJet = k_PFJet;

                          chf_3rdjet = it_jet3->chargedHadronEnergyFraction();
                          nhf_3rdjet = (it_jet3->neutralHadronEnergy()+it_jet3->HFHadronEnergy())/it_jet3->energy();
                          cef_3rdjet = it_jet3->chargedEmEnergyFraction();
                          nef_3rdjet = it_jet3->neutralEmEnergyFraction();
                          nch_3rdjet = it_jet3->chargedMultiplicity();
                          nconstituents_3rdjet = it_jet3->numberOfDaughters();

                          find_3rd_jet = true;

                          //123
                          double px_GJ1 = leadingPhoton.Px() + leading_1stjet.Px();
                          double py_GJ1 = leadingPhoton.Py() + leading_1stjet.Py();
                          double pt_GJ1 = sqrt((px_GJ1*px_GJ1)+(py_GJ1*py_GJ1));

                          double px_J2J3 = leading_2ndjet.Px() + leading_3rdjet.Px();
                          double py_J2J3 = leading_2ndjet.Py() + leading_3rdjet.Py();
                          double pt_J2J3 = sqrt((px_J2J3*px_J2J3)+(py_J2J3*py_J2J3));

                          sumOfsquare_pt_GJ1 = pt_GJ1*pt_GJ1;
                          sumOfsquare_pt_J2J3 = pt_J2J3*pt_J2J3;

                          //213
                          double px_GJ2 = leadingPhoton.Px() + leading_2ndjet.Px();
                          double py_GJ2 = leadingPhoton.Py() + leading_2ndjet.Py();
                          double pt_GJ2 = sqrt((px_GJ2*px_GJ2)+(py_GJ2*py_GJ2));

                          double px_J1J3 = leading_1stjet.Px() + leading_3rdjet.Px();
                          double py_J1J3 = leading_1stjet.Py() + leading_3rdjet.Py();
                          double pt_J1J3 = sqrt((px_J1J3*px_J1J3)+(py_J1J3*py_J1J3));

                          sumOfsquare_pt_GJ2 = pt_GJ2*pt_GJ2;
                          sumOfsquare_pt_J1J3 = pt_J1J3*pt_J1J3;

                          //312
                          double px_GJ3 = leadingPhoton.Px() + leading_3rdjet.Px();
                          double py_GJ3 = leadingPhoton.Py() + leading_3rdjet.Py();
                          double pt_GJ3 = sqrt((px_GJ3*px_GJ3)+(py_GJ3*py_GJ3));

                          double px_J1J2 = leading_1stjet.Px() + leading_2ndjet.Px();
                          double py_J1J2 = leading_1stjet.Py() + leading_2ndjet.Py();
                          double pt_J1J2 = sqrt((px_J1J2*px_J1J2)+(py_J1J2*py_J1J2));

                          sumOfsquare_pt_GJ3 = pt_GJ3*pt_GJ3;
                          sumOfsquare_pt_J1J2 = pt_J1J2*pt_J1J2;

                          //num_pair_pt++;
                        }
                      if(find_3rd_jet) break;
                    }
                 }
              }
            if(find_3rd_jet) break;
	    if(orderOf3rdLeadingJet>orderOf2ndLeadingJet) break;
           }
         //if(find_3rd_jet) cout << "(pT, eta, phi) =" << leading_3rdjet.Pt()<< "," << leading_3rdjet.Eta()<< "," << leading_3rdjet.Phi() <<endl;
       }
     if(find_3rd_jet) break;
     if(orderOf2ndLeadingJet>orderOf1stLeadingJet) break;
   }


  if(cut_jetcleaning_1stjet){
    selection_number_RAW = 5;
  }
  if(cut_1stjetvertex){
    selection_number_RAW = 6;
  }
  if(cut_1stjet_pTeta){
    selection_number_RAW = 7;
  }
  if(cut_jetcleaning_2ndjet){
    selection_number_RAW = 8;
  }
  if(cut_2ndjetvertex){
    selection_number_RAW = 9;
  }
  if(cut_2ndjet_pTeta){
    selection_number_RAW = 10;
  }
  if(cut_jetcleaning_3rdjet){
    selection_number_RAW = 11;
  }
  if(cut_3rdjetvertex){
    selection_number_RAW = 12;
  }
  if(cut_3rdjet_pTeta){
    selection_number_RAW = 13;
  }

  if( find_3rd_jet && Cut2_2nd_primary_vtx ) cut_2nd_pvtx++;     // only for selection rate calculation, didn't do anything on the event selection
  if(cut_2nd_pvtx){
    selection_number_RAW = 14;
  }


  err_pt_GJ1 = sqrt(sumOfsquare_pt_GJ1);
  err_pt_J2J3 = sqrt(sumOfsquare_pt_J2J3);
  err_pt_GJ2 = sqrt(sumOfsquare_pt_GJ2);
  err_pt_J1J3 = sqrt(sumOfsquare_pt_J1J3);
  err_pt_GJ3 = sqrt(sumOfsquare_pt_GJ3);
  err_pt_J1J2 = sqrt(sumOfsquare_pt_J1J2);


  //if(Cut2_2nd_primary_vtx) // 2nd pvtx selection
  if(find_3rd_jet){
     //123
     double px_GJ1 = leadingPhoton.Px() + leading_1stjet.Px();
     double py_GJ1 = leadingPhoton.Py() + leading_1stjet.Py();
     double pt_GJ1 = sqrt((px_GJ1*px_GJ1)+(py_GJ1*py_GJ1));

     double px_J2J3 = leading_2ndjet.Px() + leading_3rdjet.Px();
     double py_J2J3 = leading_2ndjet.Py() + leading_3rdjet.Py();
     double pt_J2J3 = sqrt((px_J2J3*px_J2J3)+(py_J2J3*py_J2J3));

     double s1_123 = TMath::Abs(pt_GJ1*pt_GJ1)/err_pt_GJ1;
     double s2_123 = TMath::Abs(pt_J2J3*pt_J2J3)/err_pt_J2J3;

     double S_CDFpt_tmp_123 = sqrt((s1_123)+(s2_123))/sqrt(2);

     TLorentzVector GJ1;
     GJ1.SetPx(px_GJ1);
     GJ1.SetPy(py_GJ1);

     TLorentzVector J2J3;
     J2J3.SetPx(px_J2J3);
     J2J3.SetPy(py_J2J3);

     double deltaS_CDFpt_tmp_123 = GJ1.Phi() - J2J3.Phi();
     if( deltaS_CDFpt_tmp_123 < 0 ) deltaS_CDFpt_tmp_123 = -deltaS_CDFpt_tmp_123;
     if( deltaS_CDFpt_tmp_123 > TMath::Pi() ) deltaS_CDFpt_tmp_123 = 2.*TMath::Pi() - deltaS_CDFpt_tmp_123;

     if( S_CDFpt_tmp_123 < S_CDFpt_reco ) {

       S_CDFpt_reco = S_CDFpt_tmp_123;
       dS_reco = deltaS_CDFpt_tmp_123;

       S_CDFpt_leadingPhoton = leadingPhoton;
       S_CDFpt_leading_1stjet = leading_1stjet;
       S_CDFpt_leading_2ndjet = leading_2ndjet;
       S_CDFpt_leading_3rdjet = leading_3rdjet;
       S_CDFpt_jecUnc_1stjet = jecUnc_1stjet;
       S_CDFpt_jecUnc_2ndjet = jecUnc_2ndjet;
       S_CDFpt_jecUnc_3rdjet = jecUnc_3rdjet;

       find_dS_reco = true;
     }

   }

  //if(Cut2_2nd_primary_vtx) // 2nd pvtx selection
  if(find_dS_reco){
  //if ( find_leadingPhoton ){
  //if ( find_leadingPhoton && multiplicity_jets >= 2 ){        //testing

     intrisic_weight = Event_weight;
     is_DPS_event = 1;

     //vertex info.
     n_vertex = number_vertex;

     //objects properties
     n_jet_pt20 = multiplicity_jets_pt20;
     n_jet_pt75 = multiplicity_jets_pt75;

     pT_leadingPhoton = leadingPhoton.Pt();
     eta_leadingPhoton = leadingPhoton.Eta();
     phi_leadingPhoton = leadingPhoton.Phi();

     if(multiplicity_jets_pt20 >= 1){
       pT_leading1stJet = leading_1stjet.Pt();
       eta_leading1stJet = leading_1stjet.Eta();
       phi_leading1stJet = leading_1stjet.Phi();
       jecUnc_leading1stJet = jecUnc_1stjet;
     }

     if(multiplicity_jets_pt20 >= 2){
       pT_leading2ndJet = leading_2ndjet.Pt();
       eta_leading2ndJet = leading_2ndjet.Eta();
       phi_leading2ndJet = leading_2ndjet.Phi();
       jecUnc_leading2ndJet = jecUnc_2ndjet;
     }

     if(multiplicity_jets_pt20 >= 3){
       pT_leading3rdJet = leading_3rdjet.Pt();
       eta_leading3rdJet = leading_3rdjet.Eta();
       phi_leading3rdJet = leading_3rdjet.Phi();
       jecUnc_leading3rdJet = jecUnc_3rdjet;
     }


     //DPS distinguishing variables

     DPS_S_CDFpT = S_CDFpt_reco;
     DPS_dS_CDFpT = dS_reco;

     DPS_pT_GJ1 = sqrt((S_CDFpt_leadingPhoton.Px()+S_CDFpt_leading_1stjet.Px())*(S_CDFpt_leadingPhoton.Px()+S_CDFpt_leading_1stjet.Px())+(S_CDFpt_leadingPhoton.Py()+S_CDFpt_leading_1stjet.Py())*(S_CDFpt_leadingPhoton.Py()+S_CDFpt_leading_1stjet.Py()));

     DPS_pT_J2J3 = sqrt((S_CDFpt_leading_2ndjet.Px()+S_CDFpt_leading_3rdjet.Px())*(S_CDFpt_leading_2ndjet.Px()+S_CDFpt_leading_3rdjet.Px())+(S_CDFpt_leading_2ndjet.Py()+S_CDFpt_leading_3rdjet.Py())*(S_CDFpt_leading_2ndjet.Py()+S_CDFpt_leading_3rdjet.Py()));

     DPS_imbal_GJ1 = DPS_pT_GJ1/(S_CDFpt_leadingPhoton.Pt()+S_CDFpt_leading_1stjet.Pt());
     DPS_imbal_J2J3 = DPS_pT_J2J3/(S_CDFpt_leading_2ndjet.Pt()+S_CDFpt_leading_3rdjet.Pt());
     DPS_imbal_overall = sqrt((S_CDFpt_leadingPhoton.Px()+S_CDFpt_leading_1stjet.Px()+S_CDFpt_leading_2ndjet.Px()+S_CDFpt_leading_3rdjet.Px())*(S_CDFpt_leadingPhoton.Px()+S_CDFpt_leading_1stjet.Px()+S_CDFpt_leading_2ndjet.Px()+S_CDFpt_leading_3rdjet.Px())+(S_CDFpt_leadingPhoton.Py()+S_CDFpt_leading_1stjet.Py()+S_CDFpt_leading_2ndjet.Py()+S_CDFpt_leading_3rdjet.Py())*(S_CDFpt_leadingPhoton.Py()+S_CDFpt_leading_1stjet.Py()+S_CDFpt_leading_2ndjet.Py()+S_CDFpt_leading_3rdjet.Py()))/(S_CDFpt_leadingPhoton.Pt()+S_CDFpt_leading_1stjet.Pt()+S_CDFpt_leading_2ndjet.Pt()+S_CDFpt_leading_3rdjet.Pt());


     DPS_MaxEta_jet = TMath::Abs(eta_leading1stJet);
     if ( TMath::Abs(eta_leading1stJet) < TMath::Abs(eta_leading2ndJet) )
       {
         DPS_MaxEta_jet = TMath::Abs(eta_leading2ndJet);
         if ( TMath::Abs(eta_leading2ndJet) < TMath::Abs(eta_leading3rdJet) )
           {
             DPS_MaxEta_jet = TMath::Abs(eta_leading3rdJet);
           }
       }
     else if ( TMath::Abs(eta_leading1stJet) < TMath::Abs(eta_leading3rdJet) )
       {
         DPS_MaxEta_jet = TMath::Abs(eta_leading3rdJet);
         if ( TMath::Abs(eta_leading3rdJet) < TMath::Abs(eta_leading2ndJet) )
           {
             DPS_MaxEta_jet = TMath::Abs(eta_leading2ndJet);
           }
       }

     DPS_MinPt_jet = pT_leading1stJet;
     if ( pT_leading1stJet > pT_leading2ndJet )
       {
         DPS_MinPt_jet = pT_leading2ndJet;
         if ( pT_leading2ndJet > pT_leading3rdJet )
           {
             DPS_MinPt_jet = pT_leading3rdJet;
           }
       }
     else if ( pT_leading1stJet > pT_leading3rdJet )
       {
         DPS_MinPt_jet = pT_leading3rdJet;
         if ( pT_leading3rdJet > pT_leading2ndJet )
           {
             DPS_MinPt_jet = pT_leading2ndJet;
           }
       }


     DPS_dPhi_GJ1 = phi_leadingPhoton - phi_leading1stJet;
     if ( DPS_dPhi_GJ1 < 0 ) DPS_dPhi_GJ1 = -DPS_dPhi_GJ1;
     if ( DPS_dPhi_GJ1 > TMath::Pi() ) DPS_dPhi_GJ1 = 2.*(TMath::Pi()) - DPS_dPhi_GJ1;

     DPS_dPhi_GJ2 = phi_leadingPhoton - phi_leading2ndJet;
     if ( DPS_dPhi_GJ2 < 0 ) DPS_dPhi_GJ2 = -DPS_dPhi_GJ2;
     if ( DPS_dPhi_GJ2 > TMath::Pi() ) DPS_dPhi_GJ2 = 2.*(TMath::Pi()) - DPS_dPhi_GJ2;

     DPS_dPhi_GJ3 = phi_leadingPhoton - phi_leading3rdJet;
     if ( DPS_dPhi_GJ3 < 0 ) DPS_dPhi_GJ3 = -DPS_dPhi_GJ3;
     if ( DPS_dPhi_GJ3 > TMath::Pi() ) DPS_dPhi_GJ3 = 2.*(TMath::Pi()) - DPS_dPhi_GJ3;

     DPS_dPhi_J1J2 = phi_leading1stJet - phi_leading2ndJet;
     if ( DPS_dPhi_J1J2 < 0 ) DPS_dPhi_J1J2 = -DPS_dPhi_J1J2;
     if ( DPS_dPhi_J1J2 > TMath::Pi() ) DPS_dPhi_J1J2 = 2.*(TMath::Pi()) - DPS_dPhi_J1J2;

     DPS_dPhi_J1J3 = phi_leading1stJet - phi_leading3rdJet;
     if ( DPS_dPhi_J1J3 < 0 ) DPS_dPhi_J1J3 = -DPS_dPhi_J1J3;
     if ( DPS_dPhi_J1J3 > TMath::Pi() ) DPS_dPhi_J1J3 = 2.*(TMath::Pi()) - DPS_dPhi_J1J3;

     DPS_dPhi_J2J3 = phi_leading2ndJet - phi_leading3rdJet;
     if ( DPS_dPhi_J2J3 < 0 ) DPS_dPhi_J2J3 = -DPS_dPhi_J2J3;
     if ( DPS_dPhi_J2J3 > TMath::Pi() ) DPS_dPhi_J2J3 = 2.*(TMath::Pi()) - DPS_dPhi_J2J3;

     Et_ratio_J1G = S_CDFpt_leading_1stjet.Et() / S_CDFpt_leadingPhoton.Et();
     Et_ratio_J3J2 = S_CDFpt_leading_3rdjet.Et() / S_CDFpt_leading_2ndjet.Et();

     //Bjorken-x dependence

     DPS_x1_GJ = pT_leadingPhoton*(TMath::Exp(eta_leadingPhoton)+TMath::Exp(eta_leading1stJet))/7000.;
     DPS_x1_JJ = (S_CDFpt_leading_2ndjet.Et()+S_CDFpt_leading_3rdjet.Et())*(TMath::Exp(eta_leading2ndJet)+TMath::Exp(eta_leading3rdJet))/14000.;
     DPS_x2_GJ = pT_leadingPhoton*(TMath::Exp(-eta_leadingPhoton)+TMath::Exp(-eta_leading1stJet))/7000.;
     DPS_x2_JJ = (S_CDFpt_leading_2ndjet.Et()+S_CDFpt_leading_3rdjet.Et())*(TMath::Exp(-eta_leading2ndJet)+TMath::Exp(-eta_leading3rdJet))/14000.;


  }


  //
  //Gen level event (counterpart of Reco Level), version I ->Event by Eveny study
  //
  //if(!onlyRECO && find_dS_reco){
  if(!onlyRECO){

     gen_is_DPS_event = 0;

     // gen level analysis                                                                                                 
                                                                                                                           
     e.getByLabel( genPartCollName   , CandHandleMCGamma );     //photon-> for gen-Iso calculation
     e.getByLabel( genJetCollName    , GenJetsHandle    );
                                                                                                                           
     std::vector<GenParticle> GenGamma;
     std::vector<GenJet> GenJetContainer;
                                                                                                                         
     GenGamma.clear();
     GenJetContainer.clear();
                                                                                                                           
     //Gen-Photon
     if (CandHandleMCGamma->size()){
      for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
      it_gen != it_gen_End;it_gen++)
        {
          const reco::Candidate &p = (*it_gen);
          if (p.numberOfMothers() < 1) continue;
          if (p.status() != 1) continue;
          if (abs(p.pdgId()) != 22) continue;        //for Dijet events
          GenGamma.push_back(*it_gen);
        }
                                                                                                                           
      std::stable_sort(GenGamma.begin(),GenGamma.end(),GenPhotonSort());
     }
                                                                                                                           
                                                                                                                           
     // GenJets
     if (GenJetsHandle->size()){
       for ( GenJetCollection::const_iterator it(GenJetsHandle->begin()), itEnd(GenJetsHandle->end());
             it!=itEnd; ++it )
         {
           GenJetContainer.push_back(*it);
         }
                                                                                                                           
       std::stable_sort(GenJetContainer.begin(),GenJetContainer.end(),GenJetSort());
     }
 
     // dS and dPhi for Gen-level
    
     double S_CDFpt_gen = 99999.;
     double dS_gen = 99999.;
    
     bool find_dS_gen = false;
    
     bool find_leadingPhoton_gen = false;
     bool find_1st_jet_gen = false;
     bool find_2nd_jet_gen = false;
     bool find_3rd_jet_gen = false;
    
     TLorentzVector leadingPhoton_gen;
    
     TLorentzVector S_CDFpt_leadingPhoton_gen;
    
     double genIso = 99999.;

     int gen_MomId[] = {1, 2, 3, 4, 5, 6, 7, 8, 21, 22};   //pdgId for the mother particle of gen-photon (quark, antiquark, gluon, photon)
     vector<int> igen_MomId(gen_MomId, gen_MomId + 10);    //
    
     std::vector<GenParticle>::const_iterator it_gengam(GenGamma.begin()), itEnd_gengam(GenGamma.end());
     for( int i_MonteCarloGamma(0); it_gengam != itEnd_gengam; ++it_gengam, ++i_MonteCarloGamma ){
    
           leadingPhoton_gen.SetPxPyPzE(it_gengam->px(),it_gengam->py(),it_gengam->pz(),it_gengam->energy());
    
           //cout<<v->Pt()<<endl;
    
           if( TMath::Abs(leadingPhoton_gen.Eta()) > 2.5 ) continue;
           if( TMath::Abs(leadingPhoton_gen.Eta()) <= 1.566 && TMath::Abs(leadingPhoton_gen.Eta()) >= 1.4442 ) continue;
           if( leadingPhoton_gen.Pt() < 30. ) continue;
    
           genIso = getGenCalIso(CandHandleMCGamma, it_gengam, 0.4, false, false);
           if( genIso > 5. ) continue;

           vector<int>::iterator it_find = find(igen_MomId.begin(), igen_MomId.end(), TMath::Abs(it_gengam->mother()->pdgId()));
           //if(it_find == igen_MomId.end()) continue;
    
           find_leadingPhoton_gen = true;
	   genIsoDR04 = genIso;
           genMomId = it_gengam->mother()->pdgId();
           break;
     }

    
     TLorentzVector leading_1stjet_gen;
     TLorentzVector leading_2ndjet_gen;
     TLorentzVector leading_3rdjet_gen;
    
     TLorentzVector S_CDFpt_leading_1stjet_gen;
     TLorentzVector S_CDFpt_leading_2ndjet_gen;
     TLorentzVector S_CDFpt_leading_3rdjet_gen;
    
     int orderOf1stLeadingJet_gen ( 0 );
     int orderOf2ndLeadingJet_gen ( 0 );
     int orderOf3rdLeadingJet_gen ( 0 );
    
     double sumOfsquare_pt_GJ1_gen ( 0 );
     double sumOfsquare_pt_J2J3_gen( 0 );
     double sumOfsquare_pt_GJ2_gen ( 0 );
     double sumOfsquare_pt_J1J3_gen( 0 );
     double sumOfsquare_pt_GJ3_gen ( 0 );
     double sumOfsquare_pt_J1J2_gen( 0 );
     double err_pt_GJ1_gen ( 0 );
     double err_pt_J2J3_gen ( 0 );
     double err_pt_GJ2_gen ( 0 );
     double err_pt_J1J3_gen ( 0 );
     double err_pt_GJ3_gen ( 0 );
     double err_pt_J1J2_gen ( 0 );
    
     std::vector<GenJet>::const_iterator it_genjets(GenJetContainer.begin()), itEnd_genjets(GenJetContainer.end());
     std::vector<GenJet>::const_iterator it_genjet1(GenJetContainer.begin()), itEnd_genjet1(GenJetContainer.end());
     std::vector<GenJet>::const_iterator it_genjet2(GenJetContainer.begin()), itEnd_genjet2(GenJetContainer.end());
     std::vector<GenJet>::const_iterator it_genjet3(GenJetContainer.begin()), itEnd_genjet3(GenJetContainer.end());
     
     TLorentzVector passed_genjet;
     double dphi_passed_gen (0);
     double deta_passed_gen (0);
     double dR_passed_gen (0);
     
     double multiplicity_genjets_pt20 = 0;
     double multiplicity_genjets_pt75 = 0;
     
     //jet selection
     if ( find_leadingPhoton_gen )
     for ( int i_InclusiveJet=1; it_genjets != itEnd_genjets; ++it_genjets, ++i_InclusiveJet )
      {
        passed_genjet.SetPxPyPzE(it_genjets->px(), it_genjets->py(), it_genjets->pz(), it_genjets->energy());
     
        dphi_passed_gen = leadingPhoton_gen.Phi() - passed_genjet.Phi();
        if ( dphi_passed_gen < 0 ) dphi_passed_gen = -dphi_passed_gen;
        if ( dphi_passed_gen > TMath::Pi() ) dphi_passed_gen = 2*TMath::Pi() - dphi_passed_gen;
        deta_passed_gen = leadingPhoton_gen.Eta() - passed_genjet.Eta();
        dR_passed_gen = sqrt((dphi_passed_gen)*(dphi_passed_gen)+(deta_passed_gen)*(deta_passed_gen));
     
        if ( dR_passed_gen > 0.5 ) {
     
            if( TMath::Abs(passed_genjet.Eta()) > 2.4 ) continue;
            if( passed_genjet.Pt() < 20 ) continue;
     
            multiplicity_genjets_pt20++;
	    if( passed_genjet.Pt() >= 30 ) multiplicity_genjets_pt75++;
     
        }
      }

    
     if ( find_leadingPhoton_gen )
     for ( int i_InclusiveJet(1); it_genjet1 != itEnd_genjet1; ++it_genjet1, ++i_InclusiveJet )
      {
        leading_1stjet_gen.SetPxPyPzE(it_genjet1->px(), it_genjet1->py(), it_genjet1->pz(), it_genjet1->energy());
    
        double dphi_1_gen = leadingPhoton_gen.Phi() - leading_1stjet_gen.Phi();
        if ( dphi_1_gen < 0 ) dphi_1_gen = -dphi_1_gen;
        if ( dphi_1_gen > TMath::Pi() ) dphi_1_gen = 2*TMath::Pi() - dphi_1_gen;
        double deta_1_gen = leadingPhoton_gen.Eta() - leading_1stjet_gen.Eta();
        double dR_1_gen = sqrt((dphi_1_gen)*(dphi_1_gen)+(deta_1_gen)*(deta_1_gen));
    
        if ( dR_1_gen > 0.5 ) {
    
            if( TMath::Abs(leading_1stjet_gen.Eta()) > 2.4 ) continue;
            if( leading_1stjet_gen.Pt() < 30 ) continue;
    
            orderOf1stLeadingJet_gen = i_InclusiveJet;
            find_1st_jet_gen = true;
            //cout << "Jet1 (pT, eta, phi) =" << leading_1stjet_gen.Pt()<< "," << leading_1stjet_gen.Eta()<< "," << leading_1stjet_gen.Phi() <<endl;
            if( find_1st_jet_gen )
            for ( int j_InclusiveJet(1); it_genjet2 != itEnd_genjet2; ++it_genjet2, ++j_InclusiveJet )
             {
               leading_2ndjet_gen.SetPxPyPzE(it_genjet2->px(), it_genjet2->py(), it_genjet2->pz(), it_genjet2->energy());
               if( leading_1stjet_gen.Pt() == leading_2ndjet_gen.Pt() && leading_1stjet_gen.Eta() == leading_2ndjet_gen.Eta() && leading_1stjet_gen.Phi() == leading_2ndjet_gen.Phi() ) continue;
               //if ( j_InclusiveJet == orderOf1stLeadingJet_gen ) continue;
    
               double dphi_2_gen = leadingPhoton_gen.Phi() - leading_2ndjet_gen.Phi();
               if ( dphi_2_gen < 0 ) dphi_2_gen = -dphi_2_gen;
               if ( dphi_2_gen > TMath::Pi() ) dphi_2_gen = 2*TMath::Pi() - dphi_2_gen;
               double deta_2_gen = leadingPhoton_gen.Eta() - leading_2ndjet_gen.Eta();
               double dR_2_gen = sqrt((dphi_2_gen)*(dphi_2_gen)+(deta_2_gen)*(deta_2_gen));
    
               if ( dR_2_gen > 0.5 ) {
    
                   if( TMath::Abs(leading_2ndjet_gen.Eta()) > 2.4 ) continue;
                   if( leading_2ndjet_gen.Pt() < 20 ) continue;
    
                   orderOf2ndLeadingJet_gen = j_InclusiveJet;
                   find_2nd_jet_gen = true;
                   //cout << "Jet2 (pT, eta, phi) =" << leading_2ndjet_gen.Pt()<< "," << leading_2ndjet_gen.Eta()<< "," << leading_2ndjet_gen.Phi() <<endl;
                   if ( find_2nd_jet_gen ) {
                      for ( int k_InclusiveJet(1); it_genjet3 != itEnd_genjet3; ++it_genjet3, ++k_InclusiveJet )
                       {
                         leading_3rdjet_gen.SetPxPyPzE(it_genjet3->px(), it_genjet3->py(), it_genjet3->pz(), it_genjet3->energy());
                         if( leading_1stjet_gen.Pt() == leading_3rdjet_gen.Pt() && leading_1stjet_gen.Eta() == leading_3rdjet_gen.Eta() && leading_1stjet_gen.Phi() == leading_3rdjet_gen.Phi() ) continue;
                         if( leading_2ndjet_gen.Pt() == leading_3rdjet_gen.Pt() && leading_2ndjet_gen.Eta() == leading_3rdjet_gen.Eta() && leading_2ndjet_gen.Phi() == leading_3rdjet_gen.Phi() ) continue;
    
                         double dphi_3_gen = leadingPhoton_gen.Phi() - leading_3rdjet_gen.Phi();
                         if ( dphi_3_gen < 0 ) dphi_3_gen = -dphi_3_gen;
                         if ( dphi_3_gen > TMath::Pi() ) dphi_3_gen = 2*TMath::Pi() - dphi_3_gen;
                         double deta_3_gen = leadingPhoton_gen.Eta() - leading_3rdjet_gen.Eta();
                         double dR_3_gen = sqrt((dphi_3_gen)*(dphi_3_gen)+(deta_3_gen)*(deta_3_gen));
    
                         if ( dR_3_gen > 0.5 ) {
                             cut_jetcleaning_3rdjet++;
    
                             if( TMath::Abs(leading_3rdjet_gen.Eta()) > 2.4 ) continue;
                             if( leading_3rdjet_gen.Pt() < 20 ) continue;
    
                             orderOf3rdLeadingJet_gen = k_InclusiveJet;
                             find_3rd_jet_gen = true;
    
                             //123
                             double px_GJ1_gen = leadingPhoton_gen.Px() + leading_1stjet_gen.Px();
                             double py_GJ1_gen = leadingPhoton_gen.Py() + leading_1stjet_gen.Py();
                             double pt_GJ1_gen = sqrt((px_GJ1_gen*px_GJ1_gen)+(py_GJ1_gen*py_GJ1_gen));
    
                             double px_J2J3_gen = leading_2ndjet_gen.Px() + leading_3rdjet_gen.Px();
                             double py_J2J3_gen = leading_2ndjet_gen.Py() + leading_3rdjet_gen.Py();
                             double pt_J2J3_gen = sqrt((px_J2J3_gen*px_J2J3_gen)+(py_J2J3_gen*py_J2J3_gen));
    
                             sumOfsquare_pt_GJ1_gen = pt_GJ1_gen*pt_GJ1_gen;
                             sumOfsquare_pt_J2J3_gen = pt_J2J3_gen*pt_J2J3_gen;
    
                             //213
                             double px_GJ2_gen = leadingPhoton_gen.Px() + leading_2ndjet_gen.Px();
                             double py_GJ2_gen = leadingPhoton_gen.Py() + leading_2ndjet_gen.Py();
                             double pt_GJ2_gen = sqrt((px_GJ2_gen*px_GJ2_gen)+(py_GJ2_gen*py_GJ2_gen));
    
                             double px_J1J3_gen = leading_1stjet_gen.Px() + leading_3rdjet_gen.Px();
                             double py_J1J3_gen = leading_1stjet_gen.Py() + leading_3rdjet_gen.Py();
                             double pt_J1J3_gen = sqrt((px_J1J3_gen*px_J1J3_gen)+(py_J1J3_gen*py_J1J3_gen));
    
                             sumOfsquare_pt_GJ2_gen = pt_GJ2_gen*pt_GJ2_gen;
                             sumOfsquare_pt_J1J3_gen = pt_J1J3_gen*pt_J1J3_gen;
    
                             //312
                             double px_GJ3_gen = leadingPhoton_gen.Px() + leading_3rdjet_gen.Px();
                             double py_GJ3_gen = leadingPhoton_gen.Py() + leading_3rdjet_gen.Py();
                             double pt_GJ3_gen = sqrt((px_GJ3_gen*px_GJ3_gen)+(py_GJ3_gen*py_GJ3_gen));
    
                             double px_J1J2_gen = leading_1stjet_gen.Px() + leading_2ndjet_gen.Px();
                             double py_J1J2_gen = leading_1stjet_gen.Py() + leading_2ndjet_gen.Py();
                             double pt_J1J2_gen = sqrt((px_J1J2_gen*px_J1J2_gen)+(py_J1J2_gen*py_J1J2_gen));
    
                             sumOfsquare_pt_GJ3_gen = pt_GJ3_gen*pt_GJ3_gen;
                             sumOfsquare_pt_J1J2_gen = pt_J1J2_gen*pt_J1J2_gen;
    
                             //num_pair_pt++;
                           }
                         if(find_3rd_jet_gen) break;
                       }
                    }
                 }
               if(find_3rd_jet_gen) break;
               if(orderOf3rdLeadingJet_gen>orderOf2ndLeadingJet_gen) break;
              }
            //if(find_3rd_jet_gen) cout << "Jet3 (pT, eta, phi) =" << leading_3rdjet_gen.Pt()<< "," << leading_3rdjet_gen.Eta()<< "," << leading_3rdjet_gen.Phi() <<endl;
          }
        if(find_3rd_jet_gen) break;
        if(orderOf2ndLeadingJet_gen>orderOf1stLeadingJet_gen) break;
      }
    
     err_pt_GJ1_gen = sqrt(sumOfsquare_pt_GJ1_gen);
     err_pt_J2J3_gen = sqrt(sumOfsquare_pt_J2J3_gen);
     err_pt_GJ2_gen = sqrt(sumOfsquare_pt_GJ2_gen);
     err_pt_J1J3_gen = sqrt(sumOfsquare_pt_J1J3_gen);
     err_pt_GJ3_gen = sqrt(sumOfsquare_pt_GJ3_gen);
     err_pt_J1J2_gen = sqrt(sumOfsquare_pt_J1J2_gen);
    
    
     if(find_3rd_jet_gen){
        //123
        double px_GJ1_gen = leadingPhoton_gen.Px() + leading_1stjet_gen.Px();
        double py_GJ1_gen = leadingPhoton_gen.Py() + leading_1stjet_gen.Py();
        double pt_GJ1_gen = sqrt((px_GJ1_gen*px_GJ1_gen)+(py_GJ1_gen*py_GJ1_gen));
    
        double px_J2J3_gen = leading_2ndjet_gen.Px() + leading_3rdjet_gen.Px();
        double py_J2J3_gen = leading_2ndjet_gen.Py() + leading_3rdjet_gen.Py();
        double pt_J2J3_gen = sqrt((px_J2J3_gen*px_J2J3_gen)+(py_J2J3_gen*py_J2J3_gen));
    
        double s1_123_gen = TMath::Abs(pt_GJ1_gen*pt_GJ1_gen)/err_pt_GJ1_gen;
        double s2_123_gen = TMath::Abs(pt_J2J3_gen*pt_J2J3_gen)/err_pt_J2J3_gen;
    
        double S_CDFpt_tmp_123_gen = sqrt((s1_123_gen)+(s2_123_gen))/sqrt(2);
    
        TLorentzVector GJ1;
        GJ1.SetPx(px_GJ1_gen);
        GJ1.SetPy(py_GJ1_gen);
    
        TLorentzVector J2J3;
        J2J3.SetPx(px_J2J3_gen);
        J2J3.SetPy(py_J2J3_gen);
    
        double deltaS_CDFpt_tmp_123_gen = GJ1.Phi() - J2J3.Phi();
        if( deltaS_CDFpt_tmp_123_gen < 0 ) deltaS_CDFpt_tmp_123_gen = -deltaS_CDFpt_tmp_123_gen;
        if( deltaS_CDFpt_tmp_123_gen > TMath::Pi() ) deltaS_CDFpt_tmp_123_gen = 2.*TMath::Pi() - deltaS_CDFpt_tmp_123_gen;
    
        if( S_CDFpt_tmp_123_gen < S_CDFpt_gen ) {
          S_CDFpt_gen = S_CDFpt_tmp_123_gen;
          dS_gen = deltaS_CDFpt_tmp_123_gen;
          S_CDFpt_leadingPhoton_gen = leadingPhoton_gen;
          S_CDFpt_leading_1stjet_gen = leading_1stjet_gen;
          S_CDFpt_leading_2ndjet_gen = leading_2ndjet_gen;
          S_CDFpt_leading_3rdjet_gen = leading_3rdjet_gen;
          find_dS_gen = true;
        }
     }
    
      if(find_dS_gen){

        gen_intrisic_weight = Event_weight;
        gen_n_jet_pt20 = multiplicity_genjets_pt20;
        gen_n_jet_pt75 = multiplicity_genjets_pt75;

        gen_is_DPS_event = 1;
  
        gen_pT_leadingPhoton = S_CDFpt_leadingPhoton_gen.Pt();
        gen_eta_leadingPhoton = S_CDFpt_leadingPhoton_gen.Eta();
        gen_phi_leadingPhoton = S_CDFpt_leadingPhoton_gen.Phi();

	gen_pT_leading1stJet = S_CDFpt_leading_1stjet_gen.Pt();
        gen_eta_leading1stJet = S_CDFpt_leading_1stjet_gen.Eta();
        gen_phi_leading1stJet = S_CDFpt_leading_1stjet_gen.Phi();

        gen_pT_leading2ndJet = S_CDFpt_leading_2ndjet_gen.Pt();
        gen_eta_leading2ndJet = S_CDFpt_leading_2ndjet_gen.Eta();
        gen_phi_leading2ndJet = S_CDFpt_leading_2ndjet_gen.Phi();

        gen_pT_leading3rdJet = S_CDFpt_leading_3rdjet_gen.Pt();
        gen_eta_leading3rdJet = S_CDFpt_leading_3rdjet_gen.Eta();
        gen_phi_leading3rdJet = S_CDFpt_leading_3rdjet_gen.Phi();


        //DPS distinguishing variables
        
        gen_DPS_S_CDFpT = S_CDFpt_gen;
        gen_DPS_dS_CDFpT = dS_gen;
        
        gen_DPS_pT_GJ1 = sqrt((S_CDFpt_leadingPhoton_gen.Px()+S_CDFpt_leading_1stjet_gen.Px())*(S_CDFpt_leadingPhoton_gen.Px()+S_CDFpt_leading_1stjet_gen.Px())+(S_CDFpt_leadingPhoton_gen.Py()+S_CDFpt_leading_1stjet_gen.Py())*(S_CDFpt_leadingPhoton_gen.Py()+S_CDFpt_leading_1stjet_gen.Py()));
        
        gen_DPS_pT_J2J3 = sqrt((S_CDFpt_leading_2ndjet_gen.Px()+S_CDFpt_leading_3rdjet_gen.Px())*(S_CDFpt_leading_2ndjet_gen.Px()+S_CDFpt_leading_3rdjet_gen.Px())+(S_CDFpt_leading_2ndjet_gen.Py()+S_CDFpt_leading_3rdjet_gen.Py())*(S_CDFpt_leading_2ndjet_gen.Py()+S_CDFpt_leading_3rdjet_gen.Py()));
        
        gen_DPS_imbal_GJ1 = gen_DPS_pT_GJ1/(S_CDFpt_leadingPhoton_gen.Pt()+S_CDFpt_leading_1stjet_gen.Pt());
        gen_DPS_imbal_J2J3 = gen_DPS_pT_J2J3/(S_CDFpt_leading_2ndjet_gen.Pt()+S_CDFpt_leading_3rdjet_gen.Pt());
        gen_DPS_imbal_overall = sqrt((S_CDFpt_leadingPhoton_gen.Px()+S_CDFpt_leading_1stjet_gen.Px()+S_CDFpt_leading_2ndjet_gen.Px()+S_CDFpt_leading_3rdjet_gen.Px())*(S_CDFpt_leadingPhoton_gen.Px()+S_CDFpt_leading_1stjet_gen.Px()+S_CDFpt_leading_2ndjet_gen.Px()+S_CDFpt_leading_3rdjet_gen.Px())+(S_CDFpt_leadingPhoton_gen.Py()+S_CDFpt_leading_1stjet_gen.Py()+S_CDFpt_leading_2ndjet_gen.Py()+S_CDFpt_leading_3rdjet_gen.Py())*(S_CDFpt_leadingPhoton_gen.Py()+S_CDFpt_leading_1stjet_gen.Py()+S_CDFpt_leading_2ndjet_gen.Py()+S_CDFpt_leading_3rdjet_gen.Py()))/(S_CDFpt_leadingPhoton_gen.Pt()+S_CDFpt_leading_1stjet_gen.Pt()+S_CDFpt_leading_2ndjet_gen.Pt()+S_CDFpt_leading_3rdjet_gen.Pt());
        
        
        gen_DPS_MaxEta_jet = TMath::Abs(gen_eta_leading1stJet);
        if ( TMath::Abs(gen_eta_leading1stJet) < TMath::Abs(gen_eta_leading2ndJet) )
          {
            gen_DPS_MaxEta_jet = TMath::Abs(gen_eta_leading2ndJet);
            if ( TMath::Abs(gen_eta_leading2ndJet) < TMath::Abs(gen_eta_leading3rdJet) )
              {
                gen_DPS_MaxEta_jet = TMath::Abs(gen_eta_leading3rdJet);
              }
          }
        else if ( TMath::Abs(gen_eta_leading1stJet) < TMath::Abs(gen_eta_leading3rdJet) )
          {
            gen_DPS_MaxEta_jet = TMath::Abs(gen_eta_leading3rdJet);
            if ( TMath::Abs(gen_eta_leading3rdJet) < TMath::Abs(gen_eta_leading2ndJet) )
              {
                gen_DPS_MaxEta_jet = TMath::Abs(gen_eta_leading2ndJet);
              }
          }
        
        gen_DPS_MinPt_jet = gen_pT_leading1stJet;
        if ( gen_pT_leading1stJet > gen_pT_leading2ndJet )
          {
            gen_DPS_MinPt_jet = gen_pT_leading2ndJet;
            if ( gen_pT_leading2ndJet > gen_pT_leading3rdJet )
              {
                gen_DPS_MinPt_jet = gen_pT_leading3rdJet;
              }
          }
        else if ( gen_pT_leading1stJet > gen_pT_leading3rdJet )
          {
            gen_DPS_MinPt_jet = gen_pT_leading3rdJet;
            if ( gen_pT_leading3rdJet > gen_pT_leading2ndJet )
              {
                gen_DPS_MinPt_jet = gen_pT_leading2ndJet;
              }
          }
        
        gen_DPS_dPhi_GJ1 = gen_phi_leadingPhoton - gen_phi_leading1stJet;
        if ( gen_DPS_dPhi_GJ1 < 0 ) gen_DPS_dPhi_GJ1 = -gen_DPS_dPhi_GJ1;
        if ( gen_DPS_dPhi_GJ1 > TMath::Pi() ) gen_DPS_dPhi_GJ1 = 2.*(TMath::Pi()) - gen_DPS_dPhi_GJ1;
        
        gen_DPS_dPhi_GJ2 = gen_phi_leadingPhoton - gen_phi_leading2ndJet;
        if ( gen_DPS_dPhi_GJ2 < 0 ) gen_DPS_dPhi_GJ2 = -gen_DPS_dPhi_GJ2;
        if ( gen_DPS_dPhi_GJ2 > TMath::Pi() ) gen_DPS_dPhi_GJ2 = 2.*(TMath::Pi()) - gen_DPS_dPhi_GJ2;
        
        gen_DPS_dPhi_GJ3 = gen_phi_leadingPhoton - gen_phi_leading3rdJet;
        if ( gen_DPS_dPhi_GJ3 < 0 ) gen_DPS_dPhi_GJ3 = -gen_DPS_dPhi_GJ3;
        if ( gen_DPS_dPhi_GJ3 > TMath::Pi() ) gen_DPS_dPhi_GJ3 = 2.*(TMath::Pi()) - gen_DPS_dPhi_GJ3;
        
        gen_DPS_dPhi_J1J2 = gen_phi_leading1stJet - gen_phi_leading2ndJet;
        if ( gen_DPS_dPhi_J1J2 < 0 ) gen_DPS_dPhi_J1J2 = -gen_DPS_dPhi_J1J2;
        if ( gen_DPS_dPhi_J1J2 > TMath::Pi() ) gen_DPS_dPhi_J1J2 = 2.*(TMath::Pi()) - gen_DPS_dPhi_J1J2;
        
        gen_DPS_dPhi_J1J3 = gen_phi_leading1stJet - gen_phi_leading3rdJet;
        if ( gen_DPS_dPhi_J1J3 < 0 ) gen_DPS_dPhi_J1J3 = -gen_DPS_dPhi_J1J3;
        if ( gen_DPS_dPhi_J1J3 > TMath::Pi() ) gen_DPS_dPhi_J1J3 = 2.*(TMath::Pi()) - gen_DPS_dPhi_J1J3;
        
        gen_DPS_dPhi_J2J3 = gen_phi_leading2ndJet - gen_phi_leading3rdJet;
        if ( gen_DPS_dPhi_J2J3 < 0 ) gen_DPS_dPhi_J2J3 = -gen_DPS_dPhi_J2J3;
        if ( gen_DPS_dPhi_J2J3 > TMath::Pi() ) gen_DPS_dPhi_J2J3 = 2.*(TMath::Pi()) - gen_DPS_dPhi_J2J3;
        
        gen_Et_ratio_J1G = S_CDFpt_leading_1stjet_gen.Et() / S_CDFpt_leadingPhoton_gen.Et();
        gen_Et_ratio_J3J2 = S_CDFpt_leading_3rdjet_gen.Et() / S_CDFpt_leading_2ndjet_gen.Et();
        
        
        //Bjorken-x dependence
        
        gen_DPS_x1_GJ = gen_pT_leadingPhoton*(TMath::Exp(gen_eta_leadingPhoton)+TMath::Exp(gen_eta_leading1stJet))/7000.;
        gen_DPS_x1_JJ = (S_CDFpt_leading_2ndjet_gen.Et()+S_CDFpt_leading_3rdjet_gen.Et())*(TMath::Exp(gen_eta_leading2ndJet)+TMath::Exp(gen_eta_leading3rdJet))/14000.;
        gen_DPS_x2_GJ = gen_pT_leadingPhoton*(TMath::Exp(-gen_eta_leadingPhoton)+TMath::Exp(-gen_eta_leading1stJet))/7000.;
        gen_DPS_x2_JJ = (S_CDFpt_leading_2ndjet_gen.Et()+S_CDFpt_leading_3rdjet_gen.Et())*(TMath::Exp(-gen_eta_leading2ndJet)+TMath::Exp(-gen_eta_leading3rdJet))/14000.;

 
     }

    if(!onlyRECO&&(find_dS_gen||find_dS_reco)) DPS_AnalysisTree->Fill();  //MC

  }


  //if(find_dS_reco) store();
  AnalysisTree->Fill();
  if(onlyRECO&&find_dS_reco) DPS_AnalysisTree->Fill();  //DATA

  delete jecUnc; 

}

void AnalysisRootpleProducer::endJob()
{
  //   cout << "Printing list of PDG id's: " << endl;
  //   std::sort(pdgidList.begin(), pdgidList.end());
  //   for (int iParticle(0), iParticleEnd( pdgidList.size() ); iParticle<iParticleEnd; ++iParticle)
  //     {
  //       cout << pdgidList[iParticle] << endl;
  //     }
}

