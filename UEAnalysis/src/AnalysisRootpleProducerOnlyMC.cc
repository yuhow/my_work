// Authors: F. Ambroglini, L. Fano', F. Bechtel, Y.H. Chang
#include <QCDAnalysis/UEAnalysis/interface/AnalysisRootpleProducerOnlyMC.h>
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h" 

//using namespace pat;
using namespace edm;
using namespace std;
using namespace reco;
using namespace ROOT::Math::VectorUtil;


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


// get amount of generator isolation
// default cut value of etMin is 0.0
// return number of particles and sumEt surrounding candidate

Float_t AnalysisRootpleProducerOnlyMC::getGenCalIso(edm::Handle<reco::GenParticleCollection> handle,
					   std::vector<GenParticle>::const_iterator thisPho,const Float_t dRMax,
					   bool removeMu, bool removeNu)
{
  const Float_t etMin = 0.0;
  Float_t genCalIsoSum = 0.0;
  if(!handle.isValid())return genCalIsoSum;

  for (reco::GenParticleCollection::const_iterator it_gen = 
	 handle->begin(); it_gen!=handle->end(); it_gen++){

    if(it_gen->px() == thisPho->px() && it_gen->py() == thisPho->py() && it_gen->pz() == thisPho->pz() && it_gen->energy() == thisPho->energy() && it_gen->pdgId() == thisPho->pdgId())continue;      // can't be the original photon
    if(it_gen->status()!=1 )continue;    // need to be a stable particle
    //if(it_gen->pdgId() == 22)continue;
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


 
void AnalysisRootpleProducerOnlyMC::store(){

  GEN_DPS_AnalysisTree->Fill();

}

void AnalysisRootpleProducerOnlyMC::fillEventInfo(int e){
}

AnalysisRootpleProducerOnlyMC::AnalysisRootpleProducerOnlyMC( const ParameterSet& pset )
{
  // flag to ignore gen-level analysis

  // particle, track and jet collections
  genJetCollName      = pset.getParameter<InputTag>( "GenJetCollectionName"      );
  genPartCollName     = pset.getParameter<InputTag>( "GenPartCollectionName"     );

  piG = acos(-1.);
  pdgidList.reserve(200);
}

void AnalysisRootpleProducerOnlyMC::beginJob()
{

  edm::Service<TFileService> fs;

  TFileDirectory event_info = fs->mkdir( "Event_info" );
  TFileDirectory photon_property = fs->mkdir( "Photon_property" );
  TFileDirectory jet_property    = fs->mkdir( "jet_property"    );
  TFileDirectory validation      = fs->mkdir( "validation"      );
  TFileDirectory DPS_analysis    = fs->mkdir( "DPS_analysis"    );

  //plots of Event_info
  //plots of photon properties
  h_pT_leadingPhoton_B  = photon_property.make<TH1D> ("h_pT_leadingPhoton_B","h_pT_leadingPhoton_B",300,0.,600.);
  h_pT_leadingPhoton_E  = photon_property.make<TH1D> ("h_pT_leadingPhoton_E","h_pT_leadingPhoton_E",300,0.,600.);
  h_eta_leadingPhoton_B = photon_property.make<TH1D> ("h_eta_leadingPhoton_B","h_eta_leadingPhoton_B",100,-3.,3.);
  h_eta_leadingPhoton_E = photon_property.make<TH1D> ("h_eta_leadingPhoton_E","h_eta_leadingPhoton_E",100,-3.,3.);
  h_phi_leadingPhoton_B = photon_property.make<TH1D> ("h_phi_leadingPhoton_B","h_phi_leadingPhoton_B",100,-3.15,3.15);
  h_phi_leadingPhoton_E = photon_property.make<TH1D> ("h_phi_leadingPhoton_E","h_phi_leadingPhoton_E",100,-3.15,3.15);
  h_pT_leadingPhoton_B  ->Sumw2();
  h_pT_leadingPhoton_E  ->Sumw2();
  h_eta_leadingPhoton_B ->Sumw2();
  h_eta_leadingPhoton_E ->Sumw2();
  h_phi_leadingPhoton_B ->Sumw2();
  h_phi_leadingPhoton_E ->Sumw2();

  //plots of jet properties
  h_multiplicity_jet  = validation.make<TH1D> ("h_multiplicity_jet","h_multiplicity_jet",101,-0.5,100.5);
  h_multiplicity_jet  ->Sumw2();

  h_pT_leading1stjet  = jet_property.make<TH1D> ("h_pT_leading1stjet","h_pT_leading1stjet",300,0.,600.);
  h_eta_leading1stjet = jet_property.make<TH1D> ("h_eta_leading1stjet","h_eta_leading1stjet",100,-3.,3.);
  h_phi_leading1stjet = jet_property.make<TH1D> ("h_phi_leading1stjet","h_phi_leading1stjet",100,-3.15,3.15);
  h_pT_leading2ndjet  = jet_property.make<TH1D> ("h_pT_leading2ndjet","h_pT_leading2ndjet",300,0.,600.);
  h_eta_leading2ndjet = jet_property.make<TH1D> ("h_eta_leading2ndjet","h_eta_leading2ndjet",100,-3.,3.);
  h_phi_leading2ndjet = jet_property.make<TH1D> ("h_phi_leading2ndjet","h_phi_leading2ndjet",100,-3.15,3.15);
  h_pT_leading3rdjet  = jet_property.make<TH1D> ("h_pT_leading3rdjet","h_pT_leading3rdjet",300,0.,600.);
  h_eta_leading3rdjet = jet_property.make<TH1D> ("h_eta_leading3rdjet","h_eta_leading3rdjet",100,-3.,3.);
  h_phi_leading3rdjet = jet_property.make<TH1D> ("h_phi_leading3rdjet","h_phi_leading3rdjet",100,-3.15,3.15);
  h_pT_leading1stjet  ->Sumw2();
  h_eta_leading1stjet ->Sumw2();
  h_phi_leading1stjet ->Sumw2();
  h_pT_leading2ndjet  ->Sumw2();
  h_eta_leading2ndjet ->Sumw2();
  h_phi_leading2ndjet ->Sumw2();
  h_pT_leading3rdjet  ->Sumw2();
  h_eta_leading3rdjet ->Sumw2();
  h_phi_leading3rdjet ->Sumw2();

  //validation
  h_selection_eff = validation.make<TH1D> ("h_selection_eff","h_selection_eff",30,0.,30.);

  //DPS analysis
  h_dPhiGamma1stJet        = DPS_analysis.make<TH1D> ("h_dPhiGamma1stJet","h_dPhiGamma1stJet",360,0.,3.15);
  h_dPhiGamma2ndJet        = DPS_analysis.make<TH1D> ("h_dPhiGamma2ndJet","h_dPhiGamma2ndJet",360,0.,3.15);
  h_dPhiGamma3rdJet        = DPS_analysis.make<TH1D> ("h_dPhiGamma3rdJet","h_dPhiGamma3rdJet",360,0.,3.15);
  h_dPhi1stJet2ndJet       = DPS_analysis.make<TH1D> ("h_dPhi1stJet2ndJet","h_dPhi1stJet2ndJet",360,0.,3.15);
  h_dPhi1stJet3rdJet       = DPS_analysis.make<TH1D> ("h_dPhi1stJet3rdJet","h_dPhi1stJet3rdJet",360,0.,3.15);
  h_dPhi2ndJet3rdJet       = DPS_analysis.make<TH1D> ("h_dPhi2ndJet3rdJet","h_dPhi2ndJet3rdJet",360,0.,3.15);
  h_MaxEta_Jet             = DPS_analysis.make<TH1D> ("h_MaxEta_Jet","h_MaxEta_Jet",50,0.,3.);
  h_MinPt_Jet              = DPS_analysis.make<TH1D> ("h_MinPt_Jet","h_MinPt_Jet",300,0.,600.);
  h_pT_G_Jet1              = DPS_analysis.make<TH1D> ("h_pT_G_Jet1","h_pT_G_Jet1",300,0.,600.);
  h_pT_Jet2_Jet3           = DPS_analysis.make<TH1D> ("h_pT_Jet2_Jet3","h_pT_Jet2_Jet3",300,0.,600.);
  h_pT_imbalance_G_Jet1    = DPS_analysis.make<TH1D> ("h_pT_imbalance_G_Jet1","h_pT_imbalance_G_Jet1",360,0.,1.);
  h_pT_imbalance_Jet2_Jet3 = DPS_analysis.make<TH1D> ("h_pT_imbalance_Jet2_Jet3","h_pT_imbalance_Jet2_Jet3",360,0.,1.);
  h_pT_imbalance_overall   = DPS_analysis.make<TH1D> ("h_pT_imbalance_overall","h_pT_imbalance_overall",360,0.,1.);
  h_ratio_EtJ1_EtG         = DPS_analysis.make<TH1D> ("h_ratio_EtJ1_EtG","h_ratio_EtJ1_EtG",100,0.,10.);
  h_ratio_EtJ3_EtJ2        = DPS_analysis.make<TH1D> ("h_ratio_EtJ3_EtJ2","h_ratio_EtJ3_EtJ2",100,0.,10.);
  h_S_CDFpt                = DPS_analysis.make<TH1D> ("h_S_CDFpt","h_S_CDFpt",5000,0.,50.);
  h_dS_CDFpt               = DPS_analysis.make<TH1D> ("h_dS_CDFpt","h_dS_CDFpt",360,0.,3.15);
  h_dPhiGamma1stJet        ->Sumw2();
  h_dPhiGamma2ndJet        ->Sumw2();
  h_dPhiGamma3rdJet        ->Sumw2();
  h_dPhi1stJet2ndJet       ->Sumw2();
  h_dPhi1stJet3rdJet       ->Sumw2();
  h_dPhi2ndJet3rdJet       ->Sumw2();
  h_MaxEta_Jet             ->Sumw2();
  h_MinPt_Jet              ->Sumw2();
  h_pT_G_Jet1              ->Sumw2();
  h_pT_Jet2_Jet3           ->Sumw2();
  h_pT_imbalance_G_Jet1    ->Sumw2();
  h_pT_imbalance_Jet2_Jet3 ->Sumw2();
  h_pT_imbalance_overall   ->Sumw2();
  h_ratio_EtJ1_EtG         ->Sumw2();
  h_ratio_EtJ3_EtJ2        ->Sumw2();
  h_S_CDFpt                ->Sumw2();
  h_dS_CDFpt               ->Sumw2();



  // use TFileService for output to root file

  GEN_AnalysisTree = fs->make<TTree>("GEN_AnalysisTree","GEN Analysis Tree");   //for all event

  //event info
  GEN_AnalysisTree->Branch("gen_intrisic_weight_RAW",&gen_intrisic_weight_RAW,"gen_intrisic_weight_RAW/D");
  GEN_AnalysisTree->Branch("gen_selection_number_RAW",&gen_selection_number_RAW,"gen_selection_number_RAW/I");
  GEN_AnalysisTree->Branch("gen_pT_leadingPhoton_RAW",&gen_pT_leadingPhoton_RAW,"gen_pT_leadingPhoton_RAW/D");


  GEN_DPS_AnalysisTree = fs->make<TTree>("GEN_DPS_AnalysisTree","GEN DPS Analysis Tree");   //for photon+3jets event

  //event info
  GEN_DPS_AnalysisTree->Branch("gen_intrisic_weight",&gen_intrisic_weight,"gen_intrisic_weight/D");
  GEN_DPS_AnalysisTree->Branch("gen_n_photon_pt75",&gen_n_photon_pt75,"gen_n_photon_pt75/I");
  GEN_DPS_AnalysisTree->Branch("gen_n_jet_pt20",&gen_n_jet_pt20,"gen_n_jet_pt20/I");
  GEN_DPS_AnalysisTree->Branch("gen_n_jet_pt75",&gen_n_jet_pt75,"gen_n_jet_pt75/I");
  GEN_DPS_AnalysisTree->Branch("gen_is_DPS_event",&gen_is_DPS_event,"gen_is_DPS_event/I");

  //photon
  GEN_DPS_AnalysisTree->Branch("genMomId",&genMomId,"genMomId/I");
  GEN_DPS_AnalysisTree->Branch("genIsoDR04",&genIsoDR04,"genIsoDR04/D");
  GEN_DPS_AnalysisTree->Branch("interaction_tag_leadingPhoton",&interaction_tag_leadingPhoton,"interaction_tag_leadingPhoton/I");
  GEN_DPS_AnalysisTree->Branch("gen_pT_leadingPhoton",&gen_pT_leadingPhoton,"gen_pT_leadingPhoton/D");
  GEN_DPS_AnalysisTree->Branch("gen_eta_leadingPhoton",&gen_eta_leadingPhoton,"gen_eta_leadingPhoton/D");
  GEN_DPS_AnalysisTree->Branch("gen_phi_leadingPhoton",&gen_phi_leadingPhoton,"gen_phi_leadingPhoton/D");

  //jet
  GEN_DPS_AnalysisTree->Branch("interaction_tag_leading1stJet",&interaction_tag_leading1stJet,"interaction_tag_leading1stJet/I");
  GEN_DPS_AnalysisTree->Branch("gen_pT_leading1stJet",&gen_pT_leading1stJet,"gen_pT_leading1stJet/D");
  GEN_DPS_AnalysisTree->Branch("gen_eta_leading1stJet",&gen_eta_leading1stJet,"gen_eta_leading1stJet/D");
  GEN_DPS_AnalysisTree->Branch("gen_phi_leading1stJet",&gen_phi_leading1stJet,"gen_phi_leading1stJet/D");
  GEN_DPS_AnalysisTree->Branch("interaction_tag_leading2ndJet",&interaction_tag_leading2ndJet,"interaction_tag_leading2ndJet/I");
  GEN_DPS_AnalysisTree->Branch("gen_pT_leading2ndJet",&gen_pT_leading2ndJet,"gen_pT_leading2ndJet/D");
  GEN_DPS_AnalysisTree->Branch("gen_eta_leading2ndJet",&gen_eta_leading2ndJet,"gen_eta_leading2ndJet/D");
  GEN_DPS_AnalysisTree->Branch("gen_phi_leading2ndJet",&gen_phi_leading2ndJet,"gen_phi_leading2ndJet/D");
  GEN_DPS_AnalysisTree->Branch("interaction_tag_leading3rdJet",&interaction_tag_leading3rdJet,"interaction_tag_leading3rdJet/I");
  GEN_DPS_AnalysisTree->Branch("gen_pT_leading3rdJet",&gen_pT_leading3rdJet,"gen_pT_leading3rdJet/D");
  GEN_DPS_AnalysisTree->Branch("gen_eta_leading3rdJet",&gen_eta_leading3rdJet,"gen_eta_leading3rdJet/D");
  GEN_DPS_AnalysisTree->Branch("gen_phi_leading3rdJet",&gen_phi_leading3rdJet,"gen_phi_leading3rdJet/D");

  //DPS analysis
  GEN_DPS_AnalysisTree->Branch("gen_DPS_S_CDFpT",&gen_DPS_S_CDFpT,"gen_DPS_S_CDFpT/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_dS_CDFpT",&gen_DPS_dS_CDFpT,"gen_DPS_dS_CDFpT/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_pT_GJ1",&gen_DPS_pT_GJ1,"gen_DPS_pT_GJ1/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_pT_J2J3",&gen_DPS_pT_J2J3,"gen_DPS_pT_J2J3/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_imbal_GJ1",&gen_DPS_imbal_GJ1,"gen_DPS_imbal_GJ1/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_imbal_J2J3",&gen_DPS_imbal_J2J3,"gen_DPS_imbal_J2J3/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_imbal_overall",&gen_DPS_imbal_overall,"gen_DPS_imbal_overall/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_dPhi_GJ1",&gen_DPS_dPhi_GJ1,"gen_DPS_dPhi_GJ1/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_dPhi_GJ2",&gen_DPS_dPhi_GJ2,"gen_DPS_dPhi_GJ2/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_dPhi_GJ3",&gen_DPS_dPhi_GJ3,"gen_DPS_dPhi_GJ3/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_dPhi_J1J2",&gen_DPS_dPhi_J1J2,"gen_DPS_dPhi_J1J2/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_dPhi_J1J3",&gen_DPS_dPhi_J1J3,"gen_DPS_dPhi_J1J3/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_dPhi_J2J3",&gen_DPS_dPhi_J2J3,"gen_DPS_dPhi_J2J3/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_MaxEta_jet",&gen_DPS_MaxEta_jet,"gen_DPS_MaxEta_jet/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_MinPt_jet",&gen_DPS_MinPt_jet,"gen_DPS_MinPt_jet/D");
  GEN_DPS_AnalysisTree->Branch("gen_Et_ratio_J1G",&gen_Et_ratio_J1G,"gen_Et_ratio_J1G/D");
  GEN_DPS_AnalysisTree->Branch("gen_Et_ratio_J3J2",&gen_Et_ratio_J3J2,"gen_Et_ratio_J3J2/D");

  //Bjorken-x dependence
  GEN_DPS_AnalysisTree->Branch("gen_DPS_x1_GJ",&gen_DPS_x1_GJ,"gen_DPS_x1_GJ/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_x1_JJ",&gen_DPS_x1_JJ,"gen_DPS_x1_JJ/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_x2_GJ",&gen_DPS_x2_GJ,"gen_DPS_x2_GJ/D");
  GEN_DPS_AnalysisTree->Branch("gen_DPS_x2_JJ",&gen_DPS_x2_JJ,"gen_DPS_x2_JJ/D");

  //Gen-Photon study, pt>75
  GEN_Photon_AnalysisTree = fs->make<TTree>("GEN_Photon_AnalysisTree","GEN Analysis Tree for Photon");   //for all event

  //event info
  GEN_Photon_AnalysisTree->Branch("GenPhoton_Pt","vector<double>",&b_genphotonPt);
  GEN_Photon_AnalysisTree->Branch("GenPhoton_Eta","vector<double>",&b_genphotonEta);
  GEN_Photon_AnalysisTree->Branch("GenPhoton_Phi","vector<double>",&b_genphotonPhi);
  GEN_Photon_AnalysisTree->Branch("GenPhoton_Iso","vector<double>",&b_genphotonIso);
  GEN_Photon_AnalysisTree->Branch("GenPhoton_Mom","vector<int>",&b_genphotonMom);
  GEN_Photon_AnalysisTree->Branch("GenPhoton_Tag","vector<int>",&b_genphotonTag);

  //If it's a DPS event
  GEN_Photon_AnalysisTree->Branch("GenPhoton_DPS",&GenPhoton_DPS,"GenPhoton_DPS/I");

}

  
void AnalysisRootpleProducerOnlyMC::analyze( const Event& e, const edm::EventSetup& iSetup )
{

  gen_intrisic_weight_RAW = -1;
  gen_selection_number_RAW = 0;
  gen_pT_leadingPhoton_RAW = -999;
  //info of event
  gen_intrisic_weight = -1;
  gen_n_photon_pt75 = -1;
  gen_n_jet_pt20 = -1;
  gen_n_jet_pt75 = -1;
  gen_is_DPS_event = -1;
  //photon info
  genMomId = 0;
  genIsoDR04 = -999;
  interaction_tag_leadingPhoton = 0;
  gen_pT_leadingPhoton = -999;
  gen_eta_leadingPhoton = -999;
  gen_phi_leadingPhoton = -999;
  //jet info
  interaction_tag_leading1stJet = 0;
  gen_pT_leading1stJet = -999;
  gen_eta_leading1stJet = -999;
  gen_phi_leading1stJet = -999;
  interaction_tag_leading2ndJet = 0;
  gen_pT_leading2ndJet = -999;
  gen_eta_leading2ndJet = -999;
  gen_phi_leading2ndJet = -999;
  interaction_tag_leading3rdJet = 0;
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

  //for gen-photon study, pt>75
  b_genphotonPt.clear(); 
  b_genphotonEta.clear();
  b_genphotonPhi.clear();
  b_genphotonIso.clear();
  b_genphotonMom.clear();
  b_genphotonTag.clear();
  GenPhoton_DPS = 0;

  // intrinsic event weight
  double Event_weight;
  edm::Handle<GenEventInfoProduct> hEventInfo;
  e.getByLabel("generator", hEventInfo);
  if (hEventInfo.isValid()) {
    Event_weight = hEventInfo->weight();
  }
  else
    Event_weight = 1.;

  gen_intrisic_weight_RAW = Event_weight;
  //Event_weight = 1.;

 // gen level analysis

    e.getByLabel( genPartCollName   , CandHandleMCGamma );     //photon-> for gen-Iso calculation
    e.getByLabel( genJetCollName    , GenJetsHandle    );


  ///-------------------------------
    //const HepMC::GenEvent* Evt = EvtHandle->GetEvent() ;
    
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
       //cout<<p.pdgId()<<endl;
       //if (p.numberOfMothers() < 1) continue;
       if (p.status() != 1) continue;
       if (p.pt()<75) continue;
       if (abs(p.pdgId()) != 22) continue;        //for Dijet events
       //cout<<p.status()<<endl;
       GenGamma.push_back(*it_gen);
     }

   std::stable_sort(GenGamma.begin(),GenGamma.end(),GenPhotonSort());
  } 
  cout<<"number of stable photons="<<GenGamma.size()<<endl;

  // GenJets
  if (GenJetsHandle->size()){
    for ( GenJetCollection::const_iterator it(GenJetsHandle->begin()), itEnd(GenJetsHandle->end());
          it!=itEnd; ++it )
      {
        GenJetContainer.push_back(*it);
      }

    std::stable_sort(GenJetContainer.begin(),GenJetContainer.end(),GenJetSort());
  }


  h_selection_eff->Fill(1,Event_weight); //input events
  gen_selection_number_RAW = 1;


  // DPS event tag, 1->YES, 0->NO

  gen_is_DPS_event = 0;

  
  // dS and dPhi for Gen-level

  double S_CDFpt_gen = 99999.;
  double dS_gen = 99999.;
  
  bool find_dS_gen = false;

  bool find_leadingPhoton = false;
  bool find_1st_jet = false;
  bool find_2nd_jet = false;
  bool find_3rd_jet = false;

  int cut_photon_pTeta (0);
  int cut_photon_genIso(0);
  int cut_photon_mom   (0);

  TLorentzVector leadingPhoton;

  TLorentzVector S_CDFpt_leadingPhoton;

  double genIso = 99999.;

  int gen_MomId[] = {1, 2, 3, 4, 5, 6, 7, 8, 21, 22};   //pdgId for the mother particle of gen-photon (quark, antiquark, gluon, photon)
  vector<int> igen_MomId(gen_MomId, gen_MomId + 10);    //

  double multiplicity_photons_pt75 = 0;

  //vector<int> genMomProcess[2];
  //vector<int> genMomPdgId[2];
  //vector<int> genMomIndex[2];

  //genMomProcess[0].clear();
  //genMomProcess[1].clear();
  //genMomPdgId[0].clear();
  //genMomPdgId[1].clear();
  //genMomIndex[0].clear();
  //genMomIndex[1].clear();

  const int upper_photon = 10;
  const int upper_level  = 40;

  int genMomProcess[upper_photon][upper_level];
  int genMomPdgId[upper_photon][upper_level];
  int genMomIndex[upper_photon][upper_level];

  //initial the array...
  for(int i_initial = 0; i_initial < upper_photon; i_initial++){
    for(int j_initial = 0; j_initial < upper_level; j_initial++){
      
      genMomProcess[i_initial][j_initial] = -1;
      genMomPdgId[i_initial][j_initial] = 0;
      genMomIndex[i_initial][j_initial] = 999999;
    }
  }


  int photon_index = 0;
  //cout<<GenGamma.size()<<endl;

  std::vector<GenParticle>::const_iterator it_gam_tmp(GenGamma.begin()), itEnd_gam_tmp(GenGamma.end());
  for( int i_MonteCarloGamma(0); it_gam_tmp != itEnd_gam_tmp; ++it_gam_tmp, ++i_MonteCarloGamma ){

        //cout<<v->Pt()<<endl;
        double pT_photon ( it_gam_tmp->pt()  );
        double eta_photon( it_gam_tmp->eta() );

        if( TMath::Abs(eta_photon) > 2.5 ) continue;
        if( TMath::Abs(eta_photon) <= 1.566 && TMath::Abs(eta_photon) >= 1.4442 ) continue;
        if( pT_photon < 75. ) continue;

        genIso = getGenCalIso(CandHandleMCGamma, it_gam_tmp, 0.4, false, false);
        b_genphotonPt.push_back(it_gam_tmp->pt());
        b_genphotonEta.push_back(it_gam_tmp->eta());
        b_genphotonPhi.push_back(it_gam_tmp->phi());
        b_genphotonIso.push_back(genIso);
        b_genphotonMom.push_back(TMath::Abs(it_gam_tmp->mother()->pdgId()));
	
	//cout<<genIso<<endl;

        if( genIso > 5. ) continue;

        //L-1 
        bool Level_1 = false;
	const reco::Candidate &p_L1 = (*it_gam_tmp);

        if (p_L1.numberOfMothers()>0) {

	  Level_1 = true;
	  
	  int ord_mom=-1;
          for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end()); 
               it_gen != it_gen_End;it_gen++)
           {
	        ord_mom++;
		if (p_L1.mother()->p4()==it_gen->p4()) break;

	   }

	  //genMomProcess[photon_index].push_back(p_L1.mother()->status());
	  //genMomPdgId[photon_index].push_back(p_L1.mother()->pdgId());
	  //genMomIndex[photon_index].push_back(ord_mom);
	  genMomProcess[photon_index][0] = p_L1.mother()->status();
	  genMomPdgId[photon_index][0] = p_L1.mother()->pdgId();
	  genMomIndex[photon_index][0] = ord_mom;
	  cout<<"Mother'status="<<p_L1.mother()->status()<<", Id="<<p_L1.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
	}

	//L-2
	bool Level_2 = false;

        if (Level_1) { 
	  const reco::Candidate &p_L2 = (*p_L1.mother());

          if (Level_1 && p_L2.numberOfMothers()>0) {

	    Level_2 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L2.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L2.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L2.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][1] = p_L2.mother()->status();
            genMomPdgId[photon_index][1] = p_L2.mother()->pdgId();
            genMomIndex[photon_index][1] = ord_mom;
	    cout<<"GMother'status="<<p_L2.mother()->status()<<", Id="<<p_L2.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
	  }
	}

	//L-3
        bool Level_3 = false;

	if (Level_2) {
	  const reco::Candidate &p_L2 = (*p_L1.mother());
	  const reco::Candidate &p_L3 = (*p_L2.mother());

          if (Level_2 && p_L3.numberOfMothers()>0) {

            Level_3 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L3.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L3.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L3.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][2] = p_L3.mother()->status();
            genMomPdgId[photon_index][2] = p_L3.mother()->pdgId();
            genMomIndex[photon_index][2] = ord_mom;
  	    cout<<"GGMother'status="<<p_L3.mother()->status()<<", Id="<<p_L3.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
  	  }
	}

	//L-4
        bool Level_4 = false;

        if (Level_3) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());

          if (Level_3 && p_L4.numberOfMothers()>0) {
          
            Level_4 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L4.mother()->p4()==it_gen->p4()) break;
          
             }

            //genMomProcess[photon_index].push_back(p_L4.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L4.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);          
            genMomProcess[photon_index][3] = p_L4.mother()->status();
            genMomPdgId[photon_index][3] = p_L4.mother()->pdgId();
            genMomIndex[photon_index][3] = ord_mom;
            cout<<"GGGMother'status="<<p_L4.mother()->status()<<", Id="<<p_L4.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
	}

	//L-5
        bool Level_5 = false;

        if (Level_4) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());

          if (Level_4 && p_L5.numberOfMothers()>0) {
          
            Level_5 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L5.mother()->p4()==it_gen->p4()) break;
          
             }

            //genMomProcess[photon_index].push_back(p_L5.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L5.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);          
            genMomProcess[photon_index][4] = p_L5.mother()->status();
            genMomPdgId[photon_index][4] = p_L5.mother()->pdgId();
            genMomIndex[photon_index][4] = ord_mom;
            cout<<"GGGGMother'status="<<p_L5.mother()->status()<<", Id="<<p_L5.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
	}

	//L-6
        bool Level_6 = false;

        if (Level_5) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());

	  if (Level_5 && p_L6.numberOfMothers()>0) {
	  
	    Level_6 = true;
	    int ord_mom=-1;
	    for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
	         it_gen != it_gen_End;it_gen++)
	     {
	          ord_mom++;
	          if (p_L6.mother()->p4()==it_gen->p4()) break;
	  
	     }

            //genMomProcess[photon_index].push_back(p_L6.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L6.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);	  
            genMomProcess[photon_index][5] = p_L6.mother()->status();
            genMomPdgId[photon_index][5] = p_L6.mother()->pdgId();
            genMomIndex[photon_index][5] = ord_mom;
	    cout<<"GGGGGMother'status="<<p_L6.mother()->status()<<", Id="<<p_L6.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
	  }
	}

	//L-7
        bool Level_7 = false;

        if (Level_6) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());

	  if (Level_6 && p_L7.numberOfMothers()>0) {
	  
	    Level_7 = true;
	    int ord_mom=-1;
	    for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
	         it_gen != it_gen_End;it_gen++)
	     {
	          ord_mom++;
	          if (p_L7.mother()->p4()==it_gen->p4()) break;
	  
	     }

            //genMomProcess[photon_index].push_back(p_L7.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L7.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);	  
            genMomProcess[photon_index][6] = p_L7.mother()->status();
            genMomPdgId[photon_index][6] = p_L7.mother()->pdgId();
            genMomIndex[photon_index][6] = ord_mom;
	    cout<<"GGGGGGMother'status="<<p_L7.mother()->status()<<", Id="<<p_L7.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
	  }
	}

        //L-8
        bool Level_8 = false;

        if (Level_7) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());

	  if (Level_7 && p_L8.numberOfMothers()>0) {
	  
	    Level_8 = true;
	    int ord_mom=-1;
	    for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
	         it_gen != it_gen_End;it_gen++)
	     {
	          ord_mom++;
	          if (p_L8.mother()->p4()==it_gen->p4()) break;
	  
	     }

            //genMomProcess[photon_index].push_back(p_L8.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L8.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);	  
            genMomProcess[photon_index][7] = p_L8.mother()->status();
            genMomPdgId[photon_index][7] = p_L8.mother()->pdgId();
            genMomIndex[photon_index][7] = ord_mom;
	    cout<<"GGGGGGGMother'status="<<p_L8.mother()->status()<<", Id="<<p_L8.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
	  }
	}

        //L-9
        bool Level_9 = false;

        if (Level_8) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());

	  if (Level_8 && p_L9.numberOfMothers()>0) {
	  
	    Level_9 = true;
	    int ord_mom=-1;
	    for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
	         it_gen != it_gen_End;it_gen++)
	     {
	          ord_mom++;
	          if (p_L9.mother()->p4()==it_gen->p4()) break;
	  
	     }

            //genMomProcess[photon_index].push_back(p_L9.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L9.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);	  
            genMomProcess[photon_index][8] = p_L9.mother()->status();
            genMomPdgId[photon_index][8] = p_L9.mother()->pdgId();
            genMomIndex[photon_index][8] = ord_mom;
	    cout<<"GGGGGGGGMother'status="<<p_L9.mother()->status()<<", Id="<<p_L9.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
	  }
	}

        //L-10
        bool Level_10 = false;

        if (Level_9) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());

          if (Level_9 && p_L10.numberOfMothers()>0) {

            Level_10 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L10.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L10.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L10.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][9] = p_L10.mother()->status();
            genMomPdgId[photon_index][9] = p_L10.mother()->pdgId();
            genMomIndex[photon_index][9] = ord_mom;
            cout<<"GGGGGGGGGMother'status="<<p_L10.mother()->status()<<", Id="<<p_L10.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-11
        bool Level_11 = false;

        if (Level_10) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());

          if (Level_10 && p_L11.numberOfMothers()>0) {

            Level_11 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L11.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L11.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L11.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][10] = p_L11.mother()->status();
            genMomPdgId[photon_index][10] = p_L11.mother()->pdgId();
            genMomIndex[photon_index][10] = ord_mom;
            cout<<"GGGGGGGGGGMother'status="<<p_L11.mother()->status()<<", Id="<<p_L11.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-12
        bool Level_12 = false;

        if (Level_11) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());

          if (Level_11 && p_L12.numberOfMothers()>0) {

            Level_12 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L12.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L12.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L12.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][11] = p_L12.mother()->status();
            genMomPdgId[photon_index][11] = p_L12.mother()->pdgId();
            genMomIndex[photon_index][11] = ord_mom;
            cout<<"GGGGGGGGGGGMother'status="<<p_L12.mother()->status()<<", Id="<<p_L12.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-13
        bool Level_13 = false;

        if (Level_12) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());

          if (Level_12 && p_L13.numberOfMothers()>0) {

            Level_13 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L13.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L13.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L13.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][12] = p_L13.mother()->status();
            genMomPdgId[photon_index][12] = p_L13.mother()->pdgId();
            genMomIndex[photon_index][12] = ord_mom;
            cout<<"GGGGGGGGGGGGMother'status="<<p_L13.mother()->status()<<", Id="<<p_L13.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-14
        bool Level_14 = false;

        if (Level_13) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());

          if (Level_13 && p_L14.numberOfMothers()>0) {

            Level_14 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L14.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L14.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L14.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][13] = p_L14.mother()->status();
            genMomPdgId[photon_index][13] = p_L14.mother()->pdgId();
            genMomIndex[photon_index][13] = ord_mom;
            cout<<"GGGGGGGGGGGGGMother'status="<<p_L14.mother()->status()<<", Id="<<p_L14.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-15
        bool Level_15 = false;

        if (Level_14) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());

          if (Level_14 && p_L15.numberOfMothers()>0) {

            Level_15 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L15.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L15.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L15.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][14] = p_L15.mother()->status();
            genMomPdgId[photon_index][14] = p_L15.mother()->pdgId();
            genMomIndex[photon_index][14] = ord_mom;
            cout<<"GGGGGGGGGGGGGGMother'status="<<p_L15.mother()->status()<<", Id="<<p_L15.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-16
        bool Level_16 = false;

        if (Level_15) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());

          if (Level_15 && p_L16.numberOfMothers()>0) {

            Level_16 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L16.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L16.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L16.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][15] = p_L16.mother()->status();
            genMomPdgId[photon_index][15] = p_L16.mother()->pdgId();
            genMomIndex[photon_index][15] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGMother'status="<<p_L16.mother()->status()<<", Id="<<p_L16.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-17
        bool Level_17 = false;

        if (Level_16) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());

          if (Level_16 && p_L17.numberOfMothers()>0) {

            Level_17 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L17.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L17.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L17.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][16] = p_L17.mother()->status();
            genMomPdgId[photon_index][16] = p_L17.mother()->pdgId();
            genMomIndex[photon_index][16] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGMother'status="<<p_L17.mother()->status()<<", Id="<<p_L17.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-18
        bool Level_18 = false;

        if (Level_17) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());

          if (Level_17 && p_L18.numberOfMothers()>0) {

            Level_18 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L18.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L18.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L18.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][17] = p_L18.mother()->status();
            genMomPdgId[photon_index][17] = p_L18.mother()->pdgId();
            genMomIndex[photon_index][17] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGMother'status="<<p_L18.mother()->status()<<", Id="<<p_L18.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-19
        bool Level_19 = false;

        if (Level_18) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());

          if (Level_18 && p_L19.numberOfMothers()>0) {

            Level_19 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L19.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L19.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L19.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][18] = p_L19.mother()->status();
            genMomPdgId[photon_index][18] = p_L19.mother()->pdgId();
            genMomIndex[photon_index][18] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGMother'status="<<p_L19.mother()->status()<<", Id="<<p_L19.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-20
        bool Level_20 = false;

        if (Level_19) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());

          if (Level_19 && p_L20.numberOfMothers()>0) {

            Level_20 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L20.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L20.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L20.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][19] = p_L20.mother()->status();
            genMomPdgId[photon_index][19] = p_L20.mother()->pdgId();
            genMomIndex[photon_index][19] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGMother'status="<<p_L20.mother()->status()<<", Id="<<p_L20.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-21
        bool Level_21 = false;

        if (Level_20) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());

          if (Level_20 && p_L21.numberOfMothers()>0) {

            Level_21 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L21.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L21.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L21.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][20] = p_L21.mother()->status();
            genMomPdgId[photon_index][20] = p_L21.mother()->pdgId();
            genMomIndex[photon_index][20] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGMother'status="<<p_L21.mother()->status()<<", Id="<<p_L21.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-22
        bool Level_22 = false;

        if (Level_21) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());

          if (Level_21 && p_L22.numberOfMothers()>0) {

            Level_22 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L22.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L22.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L22.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][21] = p_L22.mother()->status();
            genMomPdgId[photon_index][21] = p_L22.mother()->pdgId();
            genMomIndex[photon_index][21] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L22.mother()->status()<<", Id="<<p_L22.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-23
        bool Level_23 = false;

        if (Level_22) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());

          if (Level_22 && p_L23.numberOfMothers()>0) {

            Level_23 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L23.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L23.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L23.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][22] = p_L23.mother()->status();
            genMomPdgId[photon_index][22] = p_L23.mother()->pdgId();
            genMomIndex[photon_index][22] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L23.mother()->status()<<", Id="<<p_L23.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-24
        bool Level_24 = false;

        if (Level_23) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());

          if (Level_23 && p_L24.numberOfMothers()>0) {

            Level_24 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L24.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L24.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L24.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][23] = p_L24.mother()->status();
            genMomPdgId[photon_index][23] = p_L24.mother()->pdgId();
            genMomIndex[photon_index][23] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L24.mother()->status()<<", Id="<<p_L24.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-25
        bool Level_25 = false;

        if (Level_24) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());

          if (Level_24 && p_L25.numberOfMothers()>0) {

            Level_25 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L25.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L25.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L25.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][24] = p_L25.mother()->status();
            genMomPdgId[photon_index][24] = p_L25.mother()->pdgId();
            genMomIndex[photon_index][24] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L25.mother()->status()<<", Id="<<p_L25.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-26
        bool Level_26 = false;

        if (Level_25) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());

          if (Level_25 && p_L26.numberOfMothers()>0) {

            Level_26 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L26.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L26.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L26.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][25] = p_L26.mother()->status();
            genMomPdgId[photon_index][25] = p_L26.mother()->pdgId();
            genMomIndex[photon_index][25] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L26.mother()->status()<<", Id="<<p_L26.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-27
        bool Level_27 = false;

        if (Level_26) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());

          if (Level_26 && p_L27.numberOfMothers()>0) {

            Level_27 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L27.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L27.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L27.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][26] = p_L27.mother()->status();
            genMomPdgId[photon_index][26] = p_L27.mother()->pdgId();
            genMomIndex[photon_index][26] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L27.mother()->status()<<", Id="<<p_L27.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-28
        bool Level_28 = false;

        if (Level_27) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());

          if (Level_27 && p_L28.numberOfMothers()>0) {

            Level_28 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L28.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L28.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L28.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][27] = p_L28.mother()->status();
            genMomPdgId[photon_index][27] = p_L28.mother()->pdgId();
            genMomIndex[photon_index][27] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L28.mother()->status()<<", Id="<<p_L28.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-29
        bool Level_29 = false;

        if (Level_28) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());

          if (Level_28 && p_L29.numberOfMothers()>0) {

            Level_29 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L29.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L29.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L29.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][28] = p_L29.mother()->status();
            genMomPdgId[photon_index][28] = p_L29.mother()->pdgId();
            genMomIndex[photon_index][28] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L29.mother()->status()<<", Id="<<p_L29.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-30
        bool Level_30 = false;

        if (Level_29) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());

          if (Level_29 && p_L30.numberOfMothers()>0) {

            Level_30 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L30.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L30.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L30.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][29] = p_L30.mother()->status();
            genMomPdgId[photon_index][29] = p_L30.mother()->pdgId();
            genMomIndex[photon_index][29] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L30.mother()->status()<<", Id="<<p_L30.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-31
        bool Level_31 = false;

        if (Level_30) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());

          if (Level_30 && p_L31.numberOfMothers()>0) {

            Level_31 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L31.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L31.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L31.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][30] = p_L31.mother()->status();
            genMomPdgId[photon_index][30] = p_L31.mother()->pdgId();
            genMomIndex[photon_index][30] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L31.mother()->status()<<", Id="<<p_L31.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-32
        bool Level_32 = false;

        if (Level_31) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());
          const reco::Candidate &p_L32 = (*p_L31.mother());

          if (Level_31 && p_L32.numberOfMothers()>0) {

            Level_32 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L32.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L32.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L32.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][31] = p_L32.mother()->status();
            genMomPdgId[photon_index][31] = p_L32.mother()->pdgId();
            genMomIndex[photon_index][31] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L32.mother()->status()<<", Id="<<p_L32.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-33
        bool Level_33 = false;

        if (Level_32) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());
          const reco::Candidate &p_L32 = (*p_L31.mother());
          const reco::Candidate &p_L33 = (*p_L32.mother());

          if (Level_32 && p_L33.numberOfMothers()>0) {

            Level_33 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L33.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L33.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L33.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][32] = p_L33.mother()->status();
            genMomPdgId[photon_index][32] = p_L33.mother()->pdgId();
            genMomIndex[photon_index][32] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L33.mother()->status()<<", Id="<<p_L33.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-34
        bool Level_34 = false;

        if (Level_33) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());
          const reco::Candidate &p_L32 = (*p_L31.mother());
          const reco::Candidate &p_L33 = (*p_L32.mother());
          const reco::Candidate &p_L34 = (*p_L33.mother());

          if (Level_33 && p_L34.numberOfMothers()>0) {

            Level_34 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L34.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L34.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L34.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][33] = p_L34.mother()->status();
            genMomPdgId[photon_index][33] = p_L34.mother()->pdgId();
            genMomIndex[photon_index][33] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L34.mother()->status()<<", Id="<<p_L34.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-35
        bool Level_35 = false;

        if (Level_34) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());
          const reco::Candidate &p_L32 = (*p_L31.mother());
          const reco::Candidate &p_L33 = (*p_L32.mother());
          const reco::Candidate &p_L34 = (*p_L33.mother());
          const reco::Candidate &p_L35 = (*p_L34.mother());

          if (Level_34 && p_L35.numberOfMothers()>0) {

            Level_35 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L35.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L35.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L35.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][34] = p_L35.mother()->status();
            genMomPdgId[photon_index][34] = p_L35.mother()->pdgId();
            genMomIndex[photon_index][34] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L35.mother()->status()<<", Id="<<p_L35.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-36
        bool Level_36 = false;

        if (Level_35) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());
          const reco::Candidate &p_L32 = (*p_L31.mother());
          const reco::Candidate &p_L33 = (*p_L32.mother());
          const reco::Candidate &p_L34 = (*p_L33.mother());
          const reco::Candidate &p_L35 = (*p_L34.mother());
          const reco::Candidate &p_L36 = (*p_L35.mother());

          if (Level_35 && p_L36.numberOfMothers()>0) {

            Level_36 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L36.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L36.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L36.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][35] = p_L36.mother()->status();
            genMomPdgId[photon_index][35] = p_L36.mother()->pdgId();
            genMomIndex[photon_index][35] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L36.mother()->status()<<", Id="<<p_L36.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-37
        bool Level_37 = false;

        if (Level_36) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());
          const reco::Candidate &p_L32 = (*p_L31.mother());
          const reco::Candidate &p_L33 = (*p_L32.mother());
          const reco::Candidate &p_L34 = (*p_L33.mother());
          const reco::Candidate &p_L35 = (*p_L34.mother());
          const reco::Candidate &p_L36 = (*p_L35.mother());
          const reco::Candidate &p_L37 = (*p_L36.mother());

          if (Level_36 && p_L37.numberOfMothers()>0) {

            Level_37 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L37.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L37.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L37.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][36] = p_L37.mother()->status();
            genMomPdgId[photon_index][36] = p_L37.mother()->pdgId();
            genMomIndex[photon_index][36] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L37.mother()->status()<<", Id="<<p_L37.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-38
        bool Level_38 = false;

        if (Level_37) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());
          const reco::Candidate &p_L32 = (*p_L31.mother());
          const reco::Candidate &p_L33 = (*p_L32.mother());
          const reco::Candidate &p_L34 = (*p_L33.mother());
          const reco::Candidate &p_L35 = (*p_L34.mother());
          const reco::Candidate &p_L36 = (*p_L35.mother());
          const reco::Candidate &p_L37 = (*p_L36.mother());
          const reco::Candidate &p_L38 = (*p_L37.mother());

          if (Level_37 && p_L38.numberOfMothers()>0) {

            Level_38 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L38.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L38.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L38.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][37] = p_L38.mother()->status();
            genMomPdgId[photon_index][37] = p_L38.mother()->pdgId();
            genMomIndex[photon_index][37] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L38.mother()->status()<<", Id="<<p_L38.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-39
        bool Level_39 = false;

        if (Level_38) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());
          const reco::Candidate &p_L32 = (*p_L31.mother());
          const reco::Candidate &p_L33 = (*p_L32.mother());
          const reco::Candidate &p_L34 = (*p_L33.mother());
          const reco::Candidate &p_L35 = (*p_L34.mother());
          const reco::Candidate &p_L36 = (*p_L35.mother());
          const reco::Candidate &p_L37 = (*p_L36.mother());
          const reco::Candidate &p_L38 = (*p_L37.mother());
          const reco::Candidate &p_L39 = (*p_L38.mother());

          if (Level_38 && p_L39.numberOfMothers()>0) {

            Level_39 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L39.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L39.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L39.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][38] = p_L39.mother()->status();
            genMomPdgId[photon_index][38] = p_L39.mother()->pdgId();
            genMomIndex[photon_index][38] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L39.mother()->status()<<", Id="<<p_L39.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

        //L-40
        bool Level_40 = false;

        if (Level_39) {
          const reco::Candidate &p_L2 = (*p_L1.mother());
          const reco::Candidate &p_L3 = (*p_L2.mother());
          const reco::Candidate &p_L4 = (*p_L3.mother());
          const reco::Candidate &p_L5 = (*p_L4.mother());
          const reco::Candidate &p_L6 = (*p_L5.mother());
          const reco::Candidate &p_L7 = (*p_L6.mother());
          const reco::Candidate &p_L8 = (*p_L7.mother());
          const reco::Candidate &p_L9 = (*p_L8.mother());
          const reco::Candidate &p_L10 = (*p_L9.mother());
          const reco::Candidate &p_L11 = (*p_L10.mother());
          const reco::Candidate &p_L12 = (*p_L11.mother());
          const reco::Candidate &p_L13 = (*p_L12.mother());
          const reco::Candidate &p_L14 = (*p_L13.mother());
          const reco::Candidate &p_L15 = (*p_L14.mother());
          const reco::Candidate &p_L16 = (*p_L15.mother());
          const reco::Candidate &p_L17 = (*p_L16.mother());
          const reco::Candidate &p_L18 = (*p_L17.mother());
          const reco::Candidate &p_L19 = (*p_L18.mother());
          const reco::Candidate &p_L20 = (*p_L19.mother());
          const reco::Candidate &p_L21 = (*p_L20.mother());
          const reco::Candidate &p_L22 = (*p_L21.mother());
          const reco::Candidate &p_L23 = (*p_L22.mother());
          const reco::Candidate &p_L24 = (*p_L23.mother());
          const reco::Candidate &p_L25 = (*p_L24.mother());
          const reco::Candidate &p_L26 = (*p_L25.mother());
          const reco::Candidate &p_L27 = (*p_L26.mother());
          const reco::Candidate &p_L28 = (*p_L27.mother());
          const reco::Candidate &p_L29 = (*p_L28.mother());
          const reco::Candidate &p_L30 = (*p_L29.mother());
          const reco::Candidate &p_L31 = (*p_L30.mother());
          const reco::Candidate &p_L32 = (*p_L31.mother());
          const reco::Candidate &p_L33 = (*p_L32.mother());
          const reco::Candidate &p_L34 = (*p_L33.mother());
          const reco::Candidate &p_L35 = (*p_L34.mother());
          const reco::Candidate &p_L36 = (*p_L35.mother());
          const reco::Candidate &p_L37 = (*p_L36.mother());
          const reco::Candidate &p_L38 = (*p_L37.mother());
          const reco::Candidate &p_L39 = (*p_L38.mother());
          const reco::Candidate &p_L40 = (*p_L39.mother());

          if (Level_39 && p_L40.numberOfMothers()>0) {

            Level_40 = true;
            int ord_mom=-1;
            for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
                 it_gen != it_gen_End;it_gen++)
             {
                  ord_mom++;
                  if (p_L40.mother()->p4()==it_gen->p4()) break;

             }

            //genMomProcess[photon_index].push_back(p_L40.mother()->status());
            //genMomPdgId[photon_index].push_back(p_L40.mother()->pdgId());
            //genMomIndex[photon_index].push_back(ord_mom);
            genMomProcess[photon_index][39] = p_L40.mother()->status();
            genMomPdgId[photon_index][39] = p_L40.mother()->pdgId();
            genMomIndex[photon_index][39] = ord_mom;
            cout<<"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGMother'status="<<p_L40.mother()->status()<<", Id="<<p_L40.mother()->pdgId()<<", Idx="<<ord_mom<<endl;
          }
        }

/*
        bool Parton_match_photon = false;

        for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
        it_gen != it_gen_End;it_gen++)
          {
       
            double dphi_match_G = it_gam_tmp->phi() - it_gen->phi();
            if ( dphi_match_G < 0 ) dphi_match_G = -dphi_match_G;
            if ( dphi_match_G > TMath::Pi() ) dphi_match_G = 2*TMath::Pi() - dphi_match_G;
            double deta_match_G = it_gam_tmp->eta() - it_gen->eta();
            double dR_match_G = sqrt((dphi_match_G)*(dphi_match_G)+(deta_match_G)*(deta_match_G));
       
            if (!Parton_match_photon&&dR_match_G<=0.3&&it_gen->status()==23) {
              Parton_match_photon = true;
              b_genphotonTag.push_back(1);
            }
       
            if (!Parton_match_photon&&dR_match_G<=0.3&&it_gen->status()==33) {
              Parton_match_photon = true;
              b_genphotonTag.push_back(2);
            }
          }

        if(!Parton_match_photon)
        for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
        it_gen != it_gen_End;it_gen++)
          {

            double dphi_match_G = it_gam_tmp->phi() - it_gen->phi();
            if ( dphi_match_G < 0 ) dphi_match_G = -dphi_match_G;
            if ( dphi_match_G > TMath::Pi() ) dphi_match_G = 2*TMath::Pi() - dphi_match_G;
            double deta_match_G = it_gam_tmp->eta() - it_gen->eta();
            double dR_match_G = sqrt((dphi_match_G)*(dphi_match_G)+(deta_match_G)*(deta_match_G));

            if (!Parton_match_photon&&dR_match_G<=0.3&&(it_gen->status()==43||it_gen->status()==44)) {
              Parton_match_photon = true;
              b_genphotonTag.push_back(3);
            }

            if (!Parton_match_photon&&dR_match_G<=0.3&&(it_gen->status()==51||it_gen->status()==52)) {
              Parton_match_photon = true;
              b_genphotonTag.push_back(4);
            }
          }

        if (!Parton_match_photon) b_genphotonTag.push_back(5);
*/

  	//if (photon_index==0) break;

	photon_index++;       
	


        if( genIso > 5. ) continue;

	//cout<<it_gam_tmp->status()<<endl;

        //vector<int>::iterator it_find = find(igen_MomId.begin(), igen_MomId.end(), TMath::Abs(it_gam_tmp->mother()->pdgId()));
        //if(it_find == igen_MomId.end()) continue;

	multiplicity_photons_pt75++;

  }

//  //vector form...
//  //cout<<"size="<<genMomProcess[0].size()<<endl;;
//  //cout<<genMomPdgId[0].size()<<endl;;
//  //cout<<genMomIndex[0].size()<<endl;;
// 
//  for(unsigned int i_photon = 1; i_photon<=b_genphotonPt.size(); ++i_photon){
// 
//    int final_level = 0;
// 
//    int index_tag = 99999;
//    int index_tag_tmp = 99999;
// 
//    vector<int>::iterator iter_index = genMomIndex[i_photon-1].begin();
//    for(int ix = 1; iter_index != genMomIndex[i_photon-1].end(); ++iter_index, ++ix){
//        
//        index_tag_tmp = *iter_index;
//        if (index_tag_tmp<index_tag) {
//          index_tag = index_tag_tmp;
//          //cout<<"decreasing...:"<<ix<<endl;
//        }
// 
//        if (index_tag_tmp>index_tag) {
//          final_level = ix-1;
//          //cout<<"increasing...:"<<ix<<endl;
//          break;
//        }
// 
//        //cout<<*iter_index<<endl;
//    }
// 
//    vector<int>::iterator iter_process = genMomProcess[i_photon-1].begin();
//    for(int ix = 1; iter_process != genMomProcess[i_photon-1].end(); ++iter_process, ++ix){
// 
//        if (ix==final_level) b_genphotonTag.push_back(*iter_process);
// 
//        //if (ix==final_level) cout<<*iter_process<<endl;
//    }
// 
//  }

  //array form...

  for(unsigned int i_photon = 1; i_photon<=b_genphotonPt.size(); ++i_photon){

    int final_level = 0;

    int index_tag = 99999;
    int index_tag_tmp = 99999;

    for(int ix = 0; ix < upper_level; ++ix){

        index_tag_tmp = genMomIndex[i_photon-1][ix];
        if (index_tag_tmp<index_tag && index_tag_tmp!=999999) {
	  final_level = ix-1;
          index_tag = index_tag_tmp;
          //cout<<"decreasing...:"<<ix<<","<<index_tag<<","<<index_tag_tmp<<endl;
        }

        if (index_tag_tmp>index_tag && index_tag_tmp!=999999) {
          final_level = ix-1;
          //cout<<"increasing...:"<<ix<<","<<index_tag<<","<<index_tag_tmp<<endl;
          break;
        }

	//if (TMath::Abs(genMomPdgId[i_photon-1][ix])==2212) {
	//  final_level = ix-1;
	//  break;
	//}

    }

    for(int ix = 0; ix < upper_level; ++ix){

        if (ix==final_level) b_genphotonTag.push_back(genMomProcess[i_photon-1][ix]);

        //if (ix==final_level) cout<<"!!->"<<genMomProcess[i_photon-1][ix]<<endl;
    }

  }

  std::vector<GenParticle>::const_iterator it_gam(GenGamma.begin()), itEnd_gam(GenGamma.end());
  for( int i_MonteCarloGamma(0); it_gam != itEnd_gam; ++it_gam, ++i_MonteCarloGamma ){

	leadingPhoton.SetPxPyPzE(it_gam->px(),it_gam->py(),it_gam->pz(),it_gam->energy());

        //cout<<v->Pt()<<endl;
        double pT_photon ( leadingPhoton.Pt()  );
        double eta_photon( leadingPhoton.Eta() );

        if( TMath::Abs(eta_photon) > 2.5 ) continue;
	if( TMath::Abs(eta_photon) <= 1.566 && TMath::Abs(eta_photon) >= 1.4442 ) continue;
        if( pT_photon < 75. ) continue;
        cut_photon_pTeta++;        

	gen_pT_leadingPhoton_RAW = pT_photon;

        genIso = getGenCalIso(CandHandleMCGamma, it_gam, 0.4, false, false);
        if( genIso > 5. ) continue;
        cut_photon_genIso++;

        //vector<int>::iterator it_find = find(igen_MomId.begin(), igen_MomId.end(), TMath::Abs(it_gam->mother()->pdgId()));
        //if(it_find == igen_MomId.end()) continue;
	cut_photon_mom++;

        find_leadingPhoton = true;
        genMomId = it_gam->mother()->pdgId();
	cout<<"find isolated photon"<<endl;
        break;	 
  }
  
  if(cut_photon_pTeta) {
    gen_selection_number_RAW = 2;
    h_selection_eff->Fill(2,Event_weight);
  }
  if(cut_photon_genIso) {
    gen_selection_number_RAW = 3;
    h_selection_eff->Fill(3,Event_weight);
  }
  if(cut_photon_mom) {
    gen_selection_number_RAW = 4;
    h_selection_eff->Fill(4,Event_weight);
  }

  TLorentzVector leading_1stjet;
  TLorentzVector leading_2ndjet;
  TLorentzVector leading_3rdjet;

  TLorentzVector S_CDFpt_leading_1stjet;
  TLorentzVector S_CDFpt_leading_2ndjet;
  TLorentzVector S_CDFpt_leading_3rdjet;

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
  int cut_1stjet_pTeta (0);
  int cut_jetcleaning_2ndjet (0);
  int cut_2ndjet_pTeta (0);
  int cut_jetcleaning_3rdjet (0);
  int cut_3rdjet_pTeta (0);

  std::vector<GenJet>::const_iterator it_jets(GenJetContainer.begin()), itEnd_jets(GenJetContainer.end());
  std::vector<GenJet>::const_iterator it_jet1(GenJetContainer.begin()), itEnd_jet1(GenJetContainer.end());
  std::vector<GenJet>::const_iterator it_jet2(GenJetContainer.begin()), itEnd_jet2(GenJetContainer.end());
  std::vector<GenJet>::const_iterator it_jet3(GenJetContainer.begin()), itEnd_jet3(GenJetContainer.end());

  TLorentzVector passed_jet;
  double dphi_passed (0);
  double deta_passed (0);
  double dR_passed (0);

  double multiplicity_jets_pt20 = 0;
  double multiplicity_jets_pt75 = 0;

  //jet selection
  if ( find_leadingPhoton )
  for ( int i_InclusiveJet=1; it_jets != itEnd_jets; ++it_jets, ++i_InclusiveJet )
   {
     passed_jet.SetPxPyPzE(it_jets->px(), it_jets->py(), it_jets->pz(), it_jets->energy());

     dphi_passed = leadingPhoton.Phi() - passed_jet.Phi();
     if ( dphi_passed < 0 ) dphi_passed = -dphi_passed;
     if ( dphi_passed > TMath::Pi() ) dphi_passed = 2*TMath::Pi() - dphi_passed;
     deta_passed = leadingPhoton.Eta() - passed_jet.Eta();
     dR_passed = sqrt((dphi_passed)*(dphi_passed)+(deta_passed)*(deta_passed));

     if ( dR_passed > 0.5 ) {

         if( TMath::Abs(passed_jet.Eta()) > 2.4 ) continue;
         if( passed_jet.Pt() < 20 ) continue;

         multiplicity_jets_pt20++;
	 if( passed_jet.Pt() >= 75 ) multiplicity_jets_pt75++;

     }
   }

  cout<<"# of pT>20 jets="<<multiplicity_jets_pt20<<endl;
  cout<<"# of pT>75 jets="<<multiplicity_jets_pt75<<endl;  

  if ( find_leadingPhoton )
  for ( int i_InclusiveJet(1); it_jet1 != itEnd_jet1; ++it_jet1, ++i_InclusiveJet )
   {
     leading_1stjet.SetPxPyPzE(it_jet1->px(), it_jet1->py(), it_jet1->pz(), it_jet1->energy());

     double dphi_1 = leadingPhoton.Phi() - leading_1stjet.Phi();
     if ( dphi_1 < 0 ) dphi_1 = -dphi_1;
     if ( dphi_1 > TMath::Pi() ) dphi_1 = 2*TMath::Pi() - dphi_1;
     double deta_1 = leadingPhoton.Eta() - leading_1stjet.Eta();
     double dR_1 = sqrt((dphi_1)*(dphi_1)+(deta_1)*(deta_1));

     if ( dR_1 > 0.5 ) {
	 cut_jetcleaning_1stjet++;

         if( TMath::Abs(leading_1stjet.Eta()) > 2.4 ) continue;
         if( leading_1stjet.Pt() < 75 ) continue;
	 cut_1stjet_pTeta++;

         orderOf1stLeadingJet = i_InclusiveJet;
         find_1st_jet = true;
         //cout << "Jet1 (pT, eta, phi) =" << leading_1stjet.Pt()<< "," << leading_1stjet.Eta()<< "," << leading_1stjet.Phi() <<endl;
         if( find_1st_jet )
	 for ( int j_InclusiveJet(1); it_jet2 != itEnd_jet2; ++it_jet2, ++j_InclusiveJet )
          {
            leading_2ndjet.SetPxPyPzE(it_jet2->px(), it_jet2->py(), it_jet2->pz(), it_jet2->energy());
            if( leading_1stjet.Pt() == leading_2ndjet.Pt() && leading_1stjet.Eta() == leading_2ndjet.Eta() && leading_1stjet.Phi() == leading_2ndjet.Phi() ) continue;
	    //if ( j_InclusiveJet == orderOf1stLeadingJet ) continue;
	    
            double dphi_2 = leadingPhoton.Phi() - leading_2ndjet.Phi();
            if ( dphi_2 < 0 ) dphi_2 = -dphi_2;
            if ( dphi_2 > TMath::Pi() ) dphi_2 = 2*TMath::Pi() - dphi_2;
            double deta_2 = leadingPhoton.Eta() - leading_2ndjet.Eta();
            double dR_2 = sqrt((dphi_2)*(dphi_2)+(deta_2)*(deta_2));
	    
	    if ( dR_2 > 0.5 ) {
                cut_jetcleaning_2ndjet++;

                if( TMath::Abs(leading_2ndjet.Eta()) > 2.4 ) continue;
                if( leading_2ndjet.Pt() < 20 ) continue;
                cut_2ndjet_pTeta++;

                orderOf2ndLeadingJet = j_InclusiveJet;
                find_2nd_jet = true;
                //cout << "Jet2 (pT, eta, phi) =" << leading_2ndjet.Pt()<< "," << leading_2ndjet.Eta()<< "," << leading_2ndjet.Phi() <<endl;
                if ( find_2nd_jet ) {
	           for ( int k_InclusiveJet(1); it_jet3 != itEnd_jet3; ++it_jet3, ++k_InclusiveJet )
                    {
                      leading_3rdjet.SetPxPyPzE(it_jet3->px(), it_jet3->py(), it_jet3->pz(), it_jet3->energy());
                      if( leading_1stjet.Pt() == leading_3rdjet.Pt() && leading_1stjet.Eta() == leading_3rdjet.Eta() && leading_1stjet.Phi() == leading_3rdjet.Phi() ) continue;
                      if( leading_2ndjet.Pt() == leading_3rdjet.Pt() && leading_2ndjet.Eta() == leading_3rdjet.Eta() && leading_2ndjet.Phi() == leading_3rdjet.Phi() ) continue;
	   	      
                      double dphi_3 = leadingPhoton.Phi() - leading_3rdjet.Phi();
                      if ( dphi_3 < 0 ) dphi_3 = -dphi_3;
                      if ( dphi_3 > TMath::Pi() ) dphi_3 = 2*TMath::Pi() - dphi_3;
                      double deta_3 = leadingPhoton.Eta() - leading_3rdjet.Eta();
                      double dR_3 = sqrt((dphi_3)*(dphi_3)+(deta_3)*(deta_3));

		      if ( dR_3 > 0.5 ) {
                          cut_jetcleaning_3rdjet++;

                          if( TMath::Abs(leading_3rdjet.Eta()) > 2.4 ) continue;
                          if( leading_3rdjet.Pt() < 20 ) continue;
                          cut_3rdjet_pTeta++;

                          orderOf3rdLeadingJet = k_InclusiveJet;
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
         //if(find_3rd_jet) cout << "Jet3 (pT, eta, phi) =" << leading_3rdjet.Pt()<< "," << leading_3rdjet.Eta()<< "," << leading_3rdjet.Phi() <<endl;
       }
     if(find_3rd_jet) break;
     if(orderOf2ndLeadingJet>orderOf1stLeadingJet) break;
   }

  if(cut_jetcleaning_1stjet) {
    gen_selection_number_RAW = 5;
    h_selection_eff->Fill(5,Event_weight);
  }
  if(cut_1stjet_pTeta) {
    gen_selection_number_RAW = 6;
    h_selection_eff->Fill(6,Event_weight);
  }
  if(cut_jetcleaning_2ndjet) {
    gen_selection_number_RAW = 7;
    h_selection_eff->Fill(7,Event_weight);
  }
  if(cut_2ndjet_pTeta) {
    gen_selection_number_RAW = 8;
    h_selection_eff->Fill(8,Event_weight);
  }
  if(cut_jetcleaning_3rdjet) {
    gen_selection_number_RAW = 9;
    h_selection_eff->Fill(9,Event_weight);
  }
  if(cut_3rdjet_pTeta) {
    gen_selection_number_RAW = 10;
    h_selection_eff->Fill(10,Event_weight);
  }


  err_pt_GJ1 = sqrt(sumOfsquare_pt_GJ1);
  err_pt_J2J3 = sqrt(sumOfsquare_pt_J2J3);
  err_pt_GJ2 = sqrt(sumOfsquare_pt_GJ2);
  err_pt_J1J3 = sqrt(sumOfsquare_pt_J1J3);
  err_pt_GJ3 = sqrt(sumOfsquare_pt_GJ3);
  err_pt_J1J2 = sqrt(sumOfsquare_pt_J1J2);


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

     if( S_CDFpt_tmp_123 < S_CDFpt_gen ) {
       S_CDFpt_gen = S_CDFpt_tmp_123;
       dS_gen = deltaS_CDFpt_tmp_123;
       S_CDFpt_leadingPhoton = leadingPhoton;
       S_CDFpt_leading_1stjet = leading_1stjet;
       S_CDFpt_leading_2ndjet = leading_2ndjet;
       S_CDFpt_leading_3rdjet = leading_3rdjet;
       find_dS_gen = true;
     }
/*
     //213
     double px_GJ2 = leadingPhoton.Px() + leading_2ndjet.Px();
     double py_GJ2 = leadingPhoton.Py() + leading_2ndjet.Py();
     double pt_GJ2 = sqrt((px_GJ2*px_GJ2)+(py_GJ2*py_GJ2));

     double px_J1J3 = leading_1stjet.Px() + leading_3rdjet.Px();
     double py_J1J3 = leading_1stjet.Py() + leading_3rdjet.Py();
     double pt_J1J3 = sqrt((px_J1J3*px_J1J3)+(py_J1J3*py_J1J3));

     double s1_213 = TMath::Abs(pt_GJ2*pt_GJ2)/err_pt_GJ2;
     double s2_213 = TMath::Abs(pt_J1J3*pt_J1J3)/err_pt_J1J3;

     double S_CDFpt_tmp_213 = sqrt((s1_213)+(s2_213))/sqrt(2);

     TLorentzVector GJ2;
     GJ2.SetPx(px_GJ2);
     GJ2.SetPy(py_GJ2);

     TLorentzVector J1J3;
     J1J3.SetPx(px_J1J3);
     J1J3.SetPy(py_J1J3);

     double deltaS_CDFpt_tmp_213 = GJ2.Phi() - J1J3.Phi();
     if( deltaS_CDFpt_tmp_213 < 0 ) deltaS_CDFpt_tmp_213 = -deltaS_CDFpt_tmp_213;
     if( deltaS_CDFpt_tmp_213 > TMath::Pi() ) deltaS_CDFpt_tmp_213 = 2.*TMath::Pi() - deltaS_CDFpt_tmp_213;

     if( S_CDFpt_tmp_213 < S_CDFpt_gen ) {
       S_CDFpt_gen = S_CDFpt_tmp_213;
       dS_gen = deltaS_CDFpt_tmp_213;
       S_CDFpt_leadingPhoton = leadingPhoton;
       S_CDFpt_leading_1stjet = leading_2ndjet;
       S_CDFpt_leading_2ndjet = leading_1stjet;
       S_CDFpt_leading_3rdjet = leading_3rdjet;
       find_dS_gen = true;
     }

     //312
     double px_GJ3 = leadingPhoton.Px() + leading_3rdjet.Px();
     double py_GJ3 = leadingPhoton.Py() + leading_3rdjet.Py();
     double pt_GJ3 = sqrt((px_GJ3*px_GJ3)+(py_GJ3*py_GJ3));

     double px_J1J2 = leading_1stjet.Px() + leading_2ndjet.Px();
     double py_J1J2 = leading_1stjet.Py() + leading_2ndjet.Py();
     double pt_J1J2 = sqrt((px_J1J2*px_J1J2)+(py_J1J2*py_J1J2));

     double s1_312 = TMath::Abs(pt_GJ3*pt_GJ3)/err_pt_GJ3;
     double s2_312 = TMath::Abs(pt_J1J2*pt_J1J2)/err_pt_J1J2;

     double S_CDFpt_tmp_312 = sqrt((s1_312)+(s2_312))/sqrt(2);

     TLorentzVector GJ3;
     GJ3.SetPx(px_GJ3);
     GJ3.SetPy(py_GJ3);

     TLorentzVector J1J2;
     J1J2.SetPx(px_J1J2);
     J1J2.SetPy(py_J1J2);

     double deltaS_CDFpt_tmp_312 = GJ3.Phi() - J1J2.Phi();
     if( deltaS_CDFpt_tmp_312 < 0 ) deltaS_CDFpt_tmp_312 = -deltaS_CDFpt_tmp_312;
     if( deltaS_CDFpt_tmp_312 > TMath::Pi() ) deltaS_CDFpt_tmp_312 = 2.*TMath::Pi() - deltaS_CDFpt_tmp_312;

     if( S_CDFpt_tmp_312 < S_CDFpt_gen ) {
       S_CDFpt_gen = S_CDFpt_tmp_312;
       dS_gen = deltaS_CDFpt_tmp_312;
       S_CDFpt_leadingPhoton = leadingPhoton;
       S_CDFpt_leading_1stjet = leading_3rdjet;
       S_CDFpt_leading_2ndjet = leading_1stjet;
       S_CDFpt_leading_3rdjet = leading_2ndjet;
       find_dS_gen = true;
      }
*/
  }

 if (find_dS_gen==true) cout<<"It's a photon+3jets event!!"<<endl;

 //interaction tag for selected particles

 bool Parton_match_photon = false;
 bool Parton_match_jet1 = false;
 bool Parton_match_jet2 = false;
 bool Parton_match_jet3 = false;

 if(find_dS_gen){

  for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
  it_gen != it_gen_End;it_gen++)
    {

      double dphi_match_G = S_CDFpt_leadingPhoton.Phi() - it_gen->phi();
      if ( dphi_match_G < 0 ) dphi_match_G = -dphi_match_G;
      if ( dphi_match_G > TMath::Pi() ) dphi_match_G = 2*TMath::Pi() - dphi_match_G;
      double deta_match_G = S_CDFpt_leadingPhoton.Eta() - it_gen->eta();
      double dR_match_G = sqrt((dphi_match_G)*(dphi_match_G)+(deta_match_G)*(deta_match_G));

      double dphi_match_J1 = S_CDFpt_leading_1stjet.Phi() - it_gen->phi();
      if ( dphi_match_J1 < 0 ) dphi_match_J1 = -dphi_match_J1;
      if ( dphi_match_J1 > TMath::Pi() ) dphi_match_J1 = 2*TMath::Pi() - dphi_match_J1;
      double deta_match_J1 = S_CDFpt_leading_1stjet.Eta() - it_gen->eta();
      double dR_match_J1 = sqrt((dphi_match_J1)*(dphi_match_J1)+(deta_match_J1)*(deta_match_J1));

      double dphi_match_J2 = S_CDFpt_leading_2ndjet.Phi() - it_gen->phi();
      if ( dphi_match_J2 < 0 ) dphi_match_J2 = -dphi_match_J2;
      if ( dphi_match_J2 > TMath::Pi() ) dphi_match_J2 = 2*TMath::Pi() - dphi_match_J2;
      double deta_match_J2 = S_CDFpt_leading_2ndjet.Eta() - it_gen->eta();
      double dR_match_J2 = sqrt((dphi_match_J2)*(dphi_match_J2)+(deta_match_J2)*(deta_match_J2));

      double dphi_match_J3 = S_CDFpt_leading_3rdjet.Phi() - it_gen->phi();
      if ( dphi_match_J3 < 0 ) dphi_match_J3 = -dphi_match_J3;
      if ( dphi_match_J3 > TMath::Pi() ) dphi_match_J3 = 2*TMath::Pi() - dphi_match_J3;
      double deta_match_J3 = S_CDFpt_leading_3rdjet.Eta() - it_gen->eta();
      double dR_match_J3 = sqrt((dphi_match_J3)*(dphi_match_J3)+(deta_match_J3)*(deta_match_J3));

      if (!Parton_match_photon&&dR_match_G<=0.3&&it_gen->status()==23) {
	Parton_match_photon = true;
	interaction_tag_leadingPhoton = 1;
      }

      if (!Parton_match_photon&&dR_match_G<=0.3&&it_gen->status()==33) {
        Parton_match_photon = true;
        interaction_tag_leadingPhoton = 2;
      }

      if (!Parton_match_jet1&&dR_match_J1<=0.5&&it_gen->status()==23) {
	Parton_match_jet1 = true;
	interaction_tag_leading1stJet = 1;
      }

      if (!Parton_match_jet1&&dR_match_J1<=0.5&&it_gen->status()==33) {
        Parton_match_jet1 = true;
        interaction_tag_leading1stJet = 2;
      }

      if (!Parton_match_jet2&&dR_match_J2<=0.5&&it_gen->status()==23) {
	Parton_match_jet2 = true;
        interaction_tag_leading2ndJet = 1;
      }

      if (!Parton_match_jet2&&dR_match_J2<=0.5&&it_gen->status()==33) {
        Parton_match_jet2 = true;
        interaction_tag_leading2ndJet = 2;
      }

      if (!Parton_match_jet3&&dR_match_J3<=0.5&&it_gen->status()==23) {
	Parton_match_jet3 = true;
        interaction_tag_leading3rdJet = 1;
      }

      if (!Parton_match_jet3&&dR_match_J3<=0.5&&it_gen->status()==33) {
        Parton_match_jet3 = true;
        interaction_tag_leading3rdJet = 2;
      }

    }
  }

/*
 //background filter (photon from MPI)

 bool is_signal = false;
 bool is_hard_enough_HI = false;
 bool is_hard_enough_MPI = false;
 if(find_dS_gen){

  for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
  it_gen != it_gen_End;it_gen++)
    {
      if (it_gen->status()==23&&it_gen->pt()>=20) is_hard_enough_HI = true; //for QCD
    }

  for (GenParticleCollection::const_iterator it_gen(CandHandleMCGamma->begin()), it_gen_End(CandHandleMCGamma->end());
  it_gen != it_gen_End;it_gen++)
    {

      //if (it_gen->numberOfMothers() < 1) continue;
      //if (it_gen->status() != 33) continue;

      //if (it_gen->status()==23&&it_gen->pt()>=50) is_hard_enough_HI = true; // for photonjet samples
      //if (is_hard_enough_HI&&it_gen->status()==33&&it_gen->pt()>=20) is_hard_enough_MPI = true; // for photonjet samples

      if (is_hard_enough_HI&&it_gen->status()==33&&it_gen->pdgId()==22&&it_gen->pt()>=75) is_hard_enough_MPI = true; // for QCD samples


      double dphi_match_G = S_CDFpt_leadingPhoton.Phi() - it_gen->phi();
      if ( dphi_match_G < 0 ) dphi_match_G = -dphi_match_G;
      if ( dphi_match_G > TMath::Pi() ) dphi_match_G = 2*TMath::Pi() - dphi_match_G;
      double deta_match_G = S_CDFpt_leadingPhoton.Eta() - it_gen->eta();
      double dR_match_G = sqrt((dphi_match_G)*(dphi_match_G)+(deta_match_G)*(deta_match_G));

      double dphi_match_J1 = S_CDFpt_leading_1stjet.Phi() - it_gen->phi();
      if ( dphi_match_J1 < 0 ) dphi_match_J1 = -dphi_match_J1;
      if ( dphi_match_J1 > TMath::Pi() ) dphi_match_J1 = 2*TMath::Pi() - dphi_match_J1;
      double deta_match_J1 = S_CDFpt_leading_1stjet.Eta() - it_gen->eta();
      double dR_match_J1 = sqrt((dphi_match_J1)*(dphi_match_J1)+(deta_match_J1)*(deta_match_J1));

      double dphi_match_J2 = S_CDFpt_leading_2ndjet.Phi() - it_gen->phi();
      if ( dphi_match_J2 < 0 ) dphi_match_J2 = -dphi_match_J2;
      if ( dphi_match_J2 > TMath::Pi() ) dphi_match_J2 = 2*TMath::Pi() - dphi_match_J2;
      double deta_match_J2 = S_CDFpt_leading_2ndjet.Eta() - it_gen->eta();
      double dR_match_J2 = sqrt((dphi_match_J2)*(dphi_match_J2)+(deta_match_J2)*(deta_match_J2));

      double dphi_match_J3 = S_CDFpt_leading_3rdjet.Phi() - it_gen->phi();
      if ( dphi_match_J3 < 0 ) dphi_match_J3 = -dphi_match_J3;
      if ( dphi_match_J3 > TMath::Pi() ) dphi_match_J3 = 2*TMath::Pi() - dphi_match_J3;
      double deta_match_J3 = S_CDFpt_leading_3rdjet.Eta() - it_gen->eta();
      double dR_match_J3 = sqrt((dphi_match_J3)*(dphi_match_J3)+(deta_match_J3)*(deta_match_J3));

      //matching
      //if (dR_match_J2<=0.5||dR_match_J3<=0.5) is_signal = true;   //2nd hard dijet from MPI
      //if (dR_match_G<=0.3&&it_gen->status()==33&&it_gen->pt()>=20) is_signal = true;   //photon from MPI (2nd hard interaction)
    }
  }
*/
  if(find_dS_gen){
  //if(find_dS_gen && is_hard_enough_MPI){  // with pt hat minimal selection
  //if(find_dS_gen && is_hard_enough_MPI && is_signal){  // with pt hat minimal selection and matching

     gen_intrisic_weight = Event_weight;

     gen_is_DPS_event = 1;
    
     //for gen-photon study
     GenPhoton_DPS = 1;

     //objects properties
     gen_n_photon_pt75 = multiplicity_photons_pt75;
     gen_n_jet_pt20 = multiplicity_jets_pt20;
     gen_n_jet_pt75 = multiplicity_jets_pt75;

     h_multiplicity_jet->Fill(multiplicity_jets_pt20,Event_weight);

     genIsoDR04 = genIso;

     gen_pT_leadingPhoton = S_CDFpt_leadingPhoton.Pt();
     gen_eta_leadingPhoton = S_CDFpt_leadingPhoton.Eta();
     gen_phi_leadingPhoton = S_CDFpt_leadingPhoton.Phi();
 
     gen_pT_leading1stJet = S_CDFpt_leading_1stjet.Pt();
     gen_eta_leading1stJet = S_CDFpt_leading_1stjet.Eta();
     gen_phi_leading1stJet = S_CDFpt_leading_1stjet.Phi();

     gen_pT_leading2ndJet = S_CDFpt_leading_2ndjet.Pt();
     gen_eta_leading2ndJet = S_CDFpt_leading_2ndjet.Eta();
     gen_phi_leading2ndJet = S_CDFpt_leading_2ndjet.Phi();
  
     gen_pT_leading3rdJet = S_CDFpt_leading_3rdjet.Pt();
     gen_eta_leading3rdJet = S_CDFpt_leading_3rdjet.Eta();
     gen_phi_leading3rdJet = S_CDFpt_leading_3rdjet.Phi();

     if ( TMath::Abs(gen_eta_leadingPhoton) < 1.4442 ) //barrel
      {
        h_pT_leadingPhoton_B->Fill(gen_pT_leadingPhoton,Event_weight);
	h_eta_leadingPhoton_B->Fill(gen_eta_leadingPhoton,Event_weight);
	h_phi_leadingPhoton_B->Fill(gen_phi_leadingPhoton,Event_weight);
      }
     if ( TMath::Abs(gen_eta_leadingPhoton) < 2.5 && TMath::Abs(gen_eta_leadingPhoton) > 1.566 ) //endcap
      {
        h_pT_leadingPhoton_E->Fill(gen_pT_leadingPhoton,Event_weight);
        h_eta_leadingPhoton_E->Fill(gen_eta_leadingPhoton,Event_weight);
        h_phi_leadingPhoton_E->Fill(gen_phi_leadingPhoton,Event_weight);
      }

     h_pT_leading1stjet->Fill(gen_pT_leading1stJet,Event_weight);
     h_eta_leading1stjet->Fill(gen_eta_leading1stJet,Event_weight);
     h_phi_leading1stjet->Fill(gen_phi_leading1stJet,Event_weight);
     h_pT_leading2ndjet->Fill(gen_pT_leading2ndJet,Event_weight);
     h_eta_leading2ndjet->Fill(gen_eta_leading2ndJet,Event_weight);
     h_phi_leading2ndjet->Fill(gen_phi_leading2ndJet,Event_weight);
     h_pT_leading3rdjet->Fill(gen_pT_leading3rdJet,Event_weight);
     h_eta_leading3rdjet->Fill(gen_eta_leading3rdJet,Event_weight);
     h_phi_leading3rdjet->Fill(gen_phi_leading3rdJet,Event_weight);


     //DPS distinguishing variables

     gen_DPS_S_CDFpT = S_CDFpt_gen;
     gen_DPS_dS_CDFpT = dS_gen;

     h_S_CDFpt->Fill(gen_DPS_S_CDFpT,Event_weight);
     h_dS_CDFpt->Fill(gen_DPS_dS_CDFpT,Event_weight);

     gen_DPS_pT_GJ1 = sqrt((S_CDFpt_leadingPhoton.Px()+S_CDFpt_leading_1stjet.Px())*(S_CDFpt_leadingPhoton.Px()+S_CDFpt_leading_1stjet.Px())+(S_CDFpt_leadingPhoton.Py()+S_CDFpt_leading_1stjet.Py())*(S_CDFpt_leadingPhoton.Py()+S_CDFpt_leading_1stjet.Py()));

     gen_DPS_pT_J2J3 = sqrt((S_CDFpt_leading_2ndjet.Px()+S_CDFpt_leading_3rdjet.Px())*(S_CDFpt_leading_2ndjet.Px()+S_CDFpt_leading_3rdjet.Px())+(S_CDFpt_leading_2ndjet.Py()+S_CDFpt_leading_3rdjet.Py())*(S_CDFpt_leading_2ndjet.Py()+S_CDFpt_leading_3rdjet.Py()));
   
     gen_DPS_imbal_GJ1 = gen_DPS_pT_GJ1/(S_CDFpt_leadingPhoton.Pt()+S_CDFpt_leading_1stjet.Pt());
     gen_DPS_imbal_J2J3 = gen_DPS_pT_J2J3/(S_CDFpt_leading_2ndjet.Pt()+S_CDFpt_leading_3rdjet.Pt());
     gen_DPS_imbal_overall = sqrt((S_CDFpt_leadingPhoton.Px()+S_CDFpt_leading_1stjet.Px()+S_CDFpt_leading_2ndjet.Px()+S_CDFpt_leading_3rdjet.Px())*(S_CDFpt_leadingPhoton.Px()+S_CDFpt_leading_1stjet.Px()+S_CDFpt_leading_2ndjet.Px()+S_CDFpt_leading_3rdjet.Px())+(S_CDFpt_leadingPhoton.Py()+S_CDFpt_leading_1stjet.Py()+S_CDFpt_leading_2ndjet.Py()+S_CDFpt_leading_3rdjet.Py())*(S_CDFpt_leadingPhoton.Py()+S_CDFpt_leading_1stjet.Py()+S_CDFpt_leading_2ndjet.Py()+S_CDFpt_leading_3rdjet.Py()))/(S_CDFpt_leadingPhoton.Pt()+S_CDFpt_leading_1stjet.Pt()+S_CDFpt_leading_2ndjet.Pt()+S_CDFpt_leading_3rdjet.Pt());

     h_pT_G_Jet1->Fill(gen_DPS_pT_GJ1,Event_weight);
     h_pT_Jet2_Jet3->Fill(gen_DPS_pT_J2J3,Event_weight);

     h_pT_imbalance_G_Jet1->Fill(gen_DPS_imbal_GJ1,Event_weight);
     h_pT_imbalance_Jet2_Jet3->Fill(gen_DPS_imbal_J2J3,Event_weight);
     h_pT_imbalance_overall->Fill(gen_DPS_imbal_overall,Event_weight);


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

     h_MaxEta_Jet->Fill(gen_DPS_MaxEta_jet,Event_weight);
     h_MinPt_Jet->Fill(gen_DPS_MinPt_jet,Event_weight);

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

     gen_Et_ratio_J1G = S_CDFpt_leading_1stjet.Et() / S_CDFpt_leadingPhoton.Et();
     gen_Et_ratio_J3J2 = S_CDFpt_leading_3rdjet.Et() / S_CDFpt_leading_2ndjet.Et();

     h_dPhiGamma1stJet->Fill(gen_DPS_dPhi_GJ1,Event_weight);
     h_dPhiGamma2ndJet->Fill(gen_DPS_dPhi_GJ2,Event_weight);
     h_dPhiGamma3rdJet->Fill(gen_DPS_dPhi_GJ3,Event_weight);
     h_dPhi1stJet2ndJet->Fill(gen_DPS_dPhi_J1J2,Event_weight);
     h_dPhi1stJet3rdJet->Fill(gen_DPS_dPhi_J1J3,Event_weight);
     h_dPhi2ndJet3rdJet->Fill(gen_DPS_dPhi_J2J3,Event_weight);
     h_ratio_EtJ1_EtG->Fill(gen_Et_ratio_J1G,Event_weight);
     h_ratio_EtJ3_EtJ2->Fill(gen_Et_ratio_J3J2,Event_weight);

     //Bjorken-x dependence

     gen_DPS_x1_GJ = gen_pT_leadingPhoton*(TMath::Exp(gen_eta_leadingPhoton)+TMath::Exp(gen_eta_leading1stJet))/7000.;
     gen_DPS_x1_JJ = (S_CDFpt_leading_2ndjet.Et()+S_CDFpt_leading_3rdjet.Et())*(TMath::Exp(gen_eta_leading2ndJet)+TMath::Exp(gen_eta_leading3rdJet))/14000.;
     gen_DPS_x2_GJ = gen_pT_leadingPhoton*(TMath::Exp(-gen_eta_leadingPhoton)+TMath::Exp(-gen_eta_leading1stJet))/7000.;
     gen_DPS_x2_JJ = (S_CDFpt_leading_2ndjet.Et()+S_CDFpt_leading_3rdjet.Et())*(TMath::Exp(-gen_eta_leading2ndJet)+TMath::Exp(-gen_eta_leading3rdJet))/14000.;

  }

  //if(find_dS_gen) store();

  GEN_AnalysisTree->Fill();
  GEN_Photon_AnalysisTree->Fill();
  if(find_dS_gen) GEN_DPS_AnalysisTree->Fill();

}

void AnalysisRootpleProducerOnlyMC::endJob()
{
  //   cout << "Printing list of PDG id's: " << endl;
  //   std::sort(pdgidList.begin(), pdgidList.end());
  //   for (int iParticle(0), iParticleEnd( pdgidList.size() ); iParticle<iParticleEnd; ++iParticle)
  //     {
  //       cout << pdgidList[iParticle] << endl;
  //     }
}

