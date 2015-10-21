// Authors: F. Ambroglini, L. Fano', F. Bechtel
#include <QCDAnalysis/UEAnalysis/interface/AnalysisRootpleProducer.h>
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

using namespace pat;
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

class BasicJetSort{
public:
  bool operator()(const reco::TrackJet& a, const reco::TrackJet& b) {
    return a.pt() > b.pt();
  }
};

class CaloJetSort{
public:
  bool operator()(const CaloJet& a, const CaloJet& b) {
    return a.pt() > b.pt();
  }
};




 
void AnalysisRootpleProducer::store(){

  AnalysisTree->Fill();

}

void AnalysisRootpleProducer::fillEventInfo(int e){
  EventKind = e;
}


bool AnalysisRootpleProducer::selectStorePhoton(const edm::Event& e, const edm::EventSetup& iSetup){	
        // Tool to get cluster shapes
        // Photon Section: store kMaxPhotons in the events as an array in the tree

  //First step: Get photon details
  Handle<reco::PhotonCollection> photons;
  e.getByLabel(photonProducer_, photons);

  //Second step: Sort photons according to pT
  reco::PhotonCollection myphotons;
  for (reco::PhotonCollection::const_iterator phoItr = photons->begin(); phoItr != photons->end(); ++phoItr) {  
    myphotons.push_back(*phoItr);
  }
  GreaterByPt<Photon> pTComparator_;
  std::sort(myphotons.begin(), myphotons.end(), pTComparator_);

  //Third step: Loop over "photon" collection until we find a decent High pT Photon
  bool hiPtPhotonFound = false;
  for (reco::PhotonCollection::const_iterator phoItr = photons->begin(); phoItr!=photons->end() && !hiPtPhotonFound; ++phoItr) {  
    if(phoItr->pt() < ptMin_ || fabs(phoItr->eta()) > etaMax_) continue;

    // Dump photon kinematics and AOD
    Photon photon = Photon(*phoItr);

    // NOTE: since CMSSW_3_1_x all photons are corrected to the primary vertex
    //       hence, Photon::setVertex() leaves photon object unchanged
    photon.setVertex(vtx_);
    storePhotonAOD(&photon, e, iSetup, _ntuple, "PHOLEAD_");
  
    ///_gammaPtHist ->Fill(phoItr->et());
    ///_gammaEtaHist->Fill(phoItr->eta());
    ///float photon_phi = phoItr->phi();  // phi is over a whole circle, use fmod to collapse together all ecal modules
    // Only fill phiMod plot with barrel photons
    ///if (fabs(phoItr->eta())<1.5) _gammaPhiModHist->Fill( fmod(photon_phi+3.14159,20.0*3.141592/180.0)-10.0*3.141592/180.0 );
  			
    hiPtPhotonFound = true;
  }
  return (hiPtPhotonFound);
}


void SinglePhotonAnalyzer::storePhotonAOD(Photon * photon,  const edm::Event& e, const edm::EventSetup &iSetup, HTuple *tpl, const char* prefx) {

  edm::Handle<EcalRecHitCollection> EBReducedRecHits;
  e.getByLabel(ebReducedRecHitCollection_, EBReducedRecHits);
  edm::Handle<EcalRecHitCollection> EEReducedRecHits;
  e.getByLabel(eeReducedRecHitCollection_, EEReducedRecHits); 
  // get the channel status from the DB
  edm::ESHandle<EcalChannelStatus> chStatus;
  iSetup.get<EcalChannelStatusRcd>().get(chStatus);

  EcalClusterLazyTools lazyTool(e, iSetup, ebReducedRecHitCollection_, eeReducedRecHitCollection_ );   
  
  const reco::CaloClusterPtr  seed = (*photon).superCluster()->seed();

// Dump photon reco details

  if( storePhysVectors_ ) { 
    tpl->Column(prx+"p4",       TLorentzVector(photon->px(),photon->py(),photon->pz(),photon->energy()));
  } else { 
    tpl->Column(prx+"energy",photon->energy());
    tpl->Column(prx+"pt",    photon->pt());
    tpl->Column(prx+"eta",   photon->eta());
    tpl->Column(prx+"phi",   photon->phi());
  }

// phiMod = distance in phi to nearest ECAL module boundary

  tpl->Column(prx+"r9",         photon ->r9());
  tpl->Column(prx+"isEBGap",    ((photon->isEBGap())? 1:0));
  tpl->Column(prx+"isEEGap",    ((photon->isEEGap())? 1:0));
  tpl->Column(prx+"isEBEEGap",  ((photon->isEBEEGap())? 1:0));
  tpl->Column(prx+"isTransGap", ((fabs(photon->eta()) > ecalBarrelMaxEta_ && fabs(photon->eta()) < ecalEndcapMinEta_) ? 1:0));
  tpl->Column(prx+"isEB",       ((photon->isEB())? 1:0));
  tpl->Column(prx+"isEE",       ((photon->isEE())? 1:0));
    
// Super-cluster parameters

  tpl->Column(prx+"ESRatio",            getESRatio(photon, e, iSetup));  //ES Ratio

  // Cluster shape variables
  DetId id = lazyTool.getMaximum(*seed).first; 
  float time  = -999., outOfTimeChi2 = -999., chi2 = -999.;
  int   flags=-1, severity = -1; 
  const EcalRecHitCollection & rechits = ( photon->isEB() ? *EBReducedRecHits : *EEReducedRecHits); 
  EcalRecHitCollection::const_iterator it = rechits.find( id );
  if( it != rechits.end() ) { 
	  time = it->time(); 
	  outOfTimeChi2 = it->outOfTimeChi2();
	  chi2 = it->chi2();
	  flags = it->recoFlag();
	  severity = EcalSeverityLevelAlgo::severityLevel( id, rechits, *chStatus );
  }

  tpl->Column(prx+"seedRecoFlag",flags);
  tpl->Column(prx+"seedSeverity",severity);

// Photon shower shape parameters 
  tpl->Column(prx+"sigmaIetaIeta",photon->sigmaIetaIeta());

// AOD isolation and identification
  tpl->Column(prx+"hadronicOverEm",      photon->hadronicOverEm());

// Delta R= 0.4
  tpl->Column(prx+"ecalRecHitSumEtConeDR04",     photon->ecalRecHitSumEtConeDR04());
  tpl->Column(prx+"hcalTowerSumEtConeDR04",      photon->hcalTowerSumEtConeDR04());
  tpl->Column(prx+"trkSumPtHollowConeDR04",      photon->trkSumPtHollowConeDR04());
 
}

Float_t AnalysisRootpleProducer::getESRatio(Photon *photon, const edm::Event& e, const edm::EventSetup& iSetup){

  //get Geometry
  ESHandle<CaloGeometry> caloGeometry;
  iSetup.get<CaloGeometryRecord>().get(caloGeometry);
  const CaloSubdetectorGeometry *geometry = caloGeometry->getSubdetectorGeometry(DetId::Ecal, EcalPreshower);
  const CaloSubdetectorGeometry *& geometry_p = geometry;

  // Get ES rechits
  edm::Handle<EcalRecHitCollection> PreshowerRecHits;
  e.getByLabel(InputTag("ecalPreshowerRecHit","EcalRecHitsES"), PreshowerRecHits);
  if( PreshowerRecHits.isValid() ) EcalRecHitCollection preshowerHits(*PreshowerRecHits);

  Float_t esratio=1.;

   if (fabs(photon->eta())>1.62) {

    const reco::CaloClusterPtr seed = (*photon).superCluster()->seed();    
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

void AnalysisRootpleProducer::storeVertex(const edm::Event& e){
	///////////////////////////////////////////////////////////////////////
	// Vertex Section: store BeamSpot and Primary Vertex of the event    //
	///////////////////////////////////////////////////////////////////////
	
	// Get the Beam Spot
  reco::BeamSpot beamSpot;
  edm::Handle<reco::BeamSpot> recoBeamSpotHandle;
  e.getByLabel(beamSpotProducer_,recoBeamSpotHandle);
  beamSpot = *recoBeamSpotHandle;
  
	// Get the primary event vertex
  Handle<reco::VertexCollection> vertexHandle;
  e.getByLabel(vertexProducer_, vertexHandle);
  reco::VertexCollection vertexCollection = *(vertexHandle.product());
  vtx_.SetXYZ(0.,0.,0.);
  double chi2(-1), ndof(-1), normChi2(-1), vtxXError(-1),  vtxYError(-1), vtxZError(-1);
  Int_t vtxNTrk(0), vtxNTrkWeight05(0), nVtxGood(0);
  Bool_t vtxIsFake(kTRUE);
  if (vertexCollection.size()>0) {    
    vtxIsFake = vertexCollection.begin()->isFake();
    vtx_ = vertexCollection.begin()->position();  
    vtxXError = vertexCollection.begin()->xError();
    vtxYError = vertexCollection.begin()->yError();
    vtxZError = vertexCollection.begin()->zError();
    chi2      = vertexCollection.begin()->chi2();  
    ndof      = vertexCollection.begin()->ndof();  
    normChi2  = vertexCollection.begin()->normalizedChi2();  
    vtxNTrk   = vertexCollection.begin()->tracksSize();
		
    vtxNTrkWeight05 = 0;
    reco::Vertex::trackRef_iterator ittrk;
    for(ittrk = vertexCollection.begin()->tracks_begin(); ittrk!= vertexCollection.begin()->tracks_end(); ++ittrk)
      if ( vertexCollection.begin()->trackWeight(*ittrk) > 0.5 ) vtxNTrkWeight05++;
		
  }
	
    nVtxGood = 0;
    reco::VertexCollection::const_iterator vert = vertexCollection.begin(); 
    for( ; vert!=vertexCollection.end(); ++vert){
      if ( !(vert->isFake()) && vert->ndof() > 4 && fabs(vert->z()) < 15) nVtxGood++;		
    }

  // Store beam spot 
  if( storePhysVectors_ ) {
    _ntuple->Column("beamSpot", TVector3(beamSpot.x0(),beamSpot.y0(),beamSpot.z0()) );
  } else {
    _ntuple->Column("beamSpotX", beamSpot.x0() );
    _ntuple->Column("beamSpotY", beamSpot.y0() );
    _ntuple->Column("beamSpotZ", beamSpot.z0() );
  }
	
	// Store primary vertex     
  _ntuple->Column("vtxIsFake"  ,vtxIsFake);
  if( storePhysVectors_ ) { 
      _ntuple->Column("vtx"       ,TVector3(vtx_.x(),vtx_.y(),vtx_.z()));
  } else {
    _ntuple->Column("vtxX"       ,vtx_.X());
    _ntuple->Column("vtxY"       ,vtx_.Y());
    _ntuple->Column("vtxZ"       ,vtx_.Z());
  }

  if( storePhysVectors_ ) { 
    _ntuple->Column("vtxError"       ,TVector3(vtxXError,vtxYError,vtxZError));
  } else {
    _ntuple->Column("vtxXError"      ,vtxXError);
    _ntuple->Column("vtxYError"      ,vtxYError);
    _ntuple->Column("vtxZError"      ,vtxZError);
  }
  _ntuple->Column("vtxNTrk"        ,vtxNTrk);
  _ntuple->Column("vtxNTrkWeight05",vtxNTrkWeight05);
  _ntuple->Column("vtxChi2"        ,chi2);
  _ntuple->Column("vtxNdof"        ,ndof);
  _ntuple->Column("vtxNormChi2"    ,normChi2);
  _ntuple->Column("nVtxAll"        ,(Int_t) vertexCollection.size());
  _ntuple->Column("nVtxGood"       ,nVtxGood);
	
}


AnalysisRootpleProducer::AnalysisRootpleProducer( const ParameterSet& pset )
{
  // flag to ignore gen-level analysis
  onlyRECO = pset.getParameter<bool>("OnlyRECO");

  // particle, track and jet collections
  mcEvent             = pset.getParameter<InputTag>( "MCEvent"                   );
  genJetCollName      = pset.getParameter<InputTag>( "GenJetCollectionName"      );
  chgJetCollName      = pset.getParameter<InputTag>( "ChgGenJetCollectionName"   );
  tracksJetCollName   = pset.getParameter<InputTag>( "TracksJetCollectionName"   );
  recoCaloJetCollName = pset.getParameter<InputTag>( "RecoCaloJetCollectionName" );
  chgGenPartCollName  = pset.getParameter<InputTag>( "ChgGenPartCollectionName"  );
  tracksCollName      = pset.getParameter<InputTag>( "TracksCollectionName"      );
  genEventScaleTag    = pset.getParameter<InputTag>( "genEventScale"             );

  // photon analysis
  storePhysVectors_           = pset.getUntrackedParameter<bool>("StorePhysVectors",  false);
  photonProducer_             = pset.getParameter<InputTag>("PhotonProducer"); 
  ebReducedRecHitCollection_  = pset.getParameter<edm::InputTag>("ebReducedRecHitCollection");
  eeReducedRecHitCollection_  = pset.getParameter<edm::InputTag>("eeReducedRecHitCollection");
  ptMin_                      = pset.getUntrackedParameter<double>("GammaPtMin", 20);
  etaMax_                     = pset.getUntrackedParameter<double>("GammaEtaMax",3);
  ecalBarrelMaxEta_           = pset.getUntrackedParameter<double>("EcalBarrelMaxEta",1.45);
  ecalEndcapMinEta_           = pset.getUntrackedParameter<double>("EcalEndcapMinEta",1.55);
  vertexProducer_             = pset.getParameter<InputTag>("VertexProducer");
  beamSpotProducer_           = pset.getParameter<edm::InputTag>("BeamSpotProducer");


  //   cout << genJetCollName.label() << endl;
  //   cout << chgJetCollName.label() << endl;
  //   cout << tracksJetCollName.label() << endl;
  //   cout << recoCaloJetCollName.label() << endl;

  // trigger results
  triggerResultsTag = pset.getParameter<InputTag>("triggerResults");
  triggerEventTag   = pset.getParameter<InputTag>("triggerEvent"  );
  //   hltFilterTag      = pset.getParameter<InputTag>("hltFilter");
  //   triggerName       = pset.getParameter<InputTag>("triggerName");

  piG = acos(-1.);
  pdgidList.reserve(200);
}

void AnalysisRootpleProducer::beginJob()
{
 
  // use TFileService for output to root file
  AnalysisTree = fs->make<TTree>("AnalysisTree","MBUE Analysis Tree ");

  AnalysisTree->Branch("EventKind",&EventKind,"EventKind/I");

  // save TClonesArrays of TLorentzVectors
  // i.e. store 4-vectors of particles and jets
  
 
  MonteCarlo = new TClonesArray("TLorentzVector", 10000);
  AnalysisTree->Branch("MonteCarlo", "TClonesArray", &MonteCarlo, 128000, 0);

  MonteCarlo2 = new TClonesArray("TVector", 10000);
  AnalysisTree->Branch("MonteCarlo2", "TClonesArray", &MonteCarlo2,128000, 0);

  Track = new TClonesArray("TLorentzVector", 10000);
  AnalysisTree->Branch("Track", "TClonesArray", &Track, 128000, 0);

  Parton = new TClonesArray("TLorentzVector", 10000);
  AnalysisTree->Branch("Parton", "TClonesArray", &Parton, 128000, 0);

  AssVertex = new TClonesArray("TLorentzVector", 10000);
  AnalysisTree->Branch("AssVertex", "TClonesArray", &AssVertex, 128000, 0);

  InclusiveJet = new TClonesArray("TLorentzVector", 10000);
  AnalysisTree->Branch("InclusiveJet", "TClonesArray", &InclusiveJet, 128000, 0);

  ChargedJet = new TClonesArray("TLorentzVector", 10000);
  AnalysisTree->Branch("ChargedJet", "TClonesArray", &ChargedJet, 128000, 0);

  TracksJet = new TClonesArray("TLorentzVector", 10000);
  AnalysisTree->Branch("TracksJet", "TClonesArray", &TracksJet, 128000, 0);

  CalorimeterJet = new TClonesArray("TLorentzVector", 10000);
  AnalysisTree->Branch("CalorimeterJet", "TClonesArray", &CalorimeterJet, 128000, 0);

  acceptedTriggers = new TClonesArray("TObjString", 10000);
  AnalysisTree->Branch("acceptedTriggers", "TClonesArray", &acceptedTriggers, 128000, 0);

  AnalysisTree->Branch("genEventScale", &genEventScale, "genEventScale/D");
 
  AnalysisTree->Branch("eventNum",&eventNum,"eventNum/I");
  AnalysisTree->Branch("lumiBlock",&lumiBlock,"lumiBlock/I");
  AnalysisTree->Branch("runNumber",&runNumber,"runNumber/I");
  AnalysisTree->Branch("bx",&bx,"bx/I");

  AnalysisTree->Branch("vertex",&vertex_,"npv[10]/I:pvx[10]/D:pvxErr[10]/D:pvy[10]/D:pvyErr[10]/D:pvz[10]/D:pvzErr[10]/D:pvntk[10]",128000);
  AnalysisTree->Branch("trackextraue_",&trackextraue_,"pvtkp[5000]/D:pvtkpt[5000]/D:pvtketa[5000]/D:pvtkphi[5000]/D:pvtknhit[5000]/D:pvtkchi2norm[5000]/D:pvtkd0[5000]/D:pvtkdoErr[5000]/D:pvtkdz[5000]/D:pvtkdzErr[5000]/D",128000);

  AnalysisTree->Branch("trackinjet_",&trackinjet_,"tkn[100]/I:tkp[5000]/D:tkpt[5000]/D:tketa[5000]/D:tkphi[5000]/D:tknhit[5000]/D:tkchi2norm[5000]/D:tkd0[5000]/D:tkdoErr[5000]/D:tkdz[5000]/D:tkdzErr[5000]/D",128000);

  PhotonAOD = new TClonesArray("TLorentzVector", 10000);  
  AnalysisTree->Branch("PhotonAOD", "TClonesArray", &PhotonAOD, 128000, 0);


  //AnalysisTree->Branch("npv",&m_npv,"npv/I");
  //AnalysisTree->Branch("pvx",m_pvx, "pvx[npv]/D");
  //AnalysisTree->Branch("pvy",m_pvy, "pvy[npv]/D");
  //AnalysisTree->Branch("pvz",m_pvz, "pvz[npv]/D");
  //AnalysisTree->Branch("pvxErr",m_pvxErr, "pvxErr[npv]/D");
  //AnalysisTree->Branch("pvyErr",m_pvyErr, "pvyErr[npv]/D");
  //AnalysisTree->Branch("pvzErr",m_pvzErr, "pvzErr[npv]/D");
  //  AnalysisTree->Branch("pvntk", m_pvntk, "pvntk[npv]/I");
  
  //AnalysisTree->Branch("pvtkp",m_pvtkp,"pvtkp[npv]/D");
  //AnalysisTree->Branch("pvtkpt",m_pvtkpt,"pvtkpt[5000]/D");
  //AnalysisTree->Branch("pvtketa",m_pvtketa,"pvtketa[5000]/D");
  //AnalysisTree->Branch("pvtkphi",m_pvtkphi,"pvtkphi[5000]/D");
  //AnalysisTree->Branch("pvtkchi2norm",m_pvtkchi2norm,"pvtkchi2norm[5000]/D");
  //AnalysisTree->Branch("pvtknhit",m_pvtknhit,"pvtknhit[5000]/D");
  //AnalysisTree->Branch("pvtkd0",m_pvtkd0,"pvtkd0[5000]/D");
  //AnalysisTree->Branch("pvtkd0Err",m_pvtkd0Err,"pvtkd0Err[5000]/D");
  //AnalysisTree->Branch("pvtkdz",m_pvtkdz,"pvtkdz[5000]/D");
  //AnalysisTree->Branch("pvtkdzErr",m_pvtkdzErr,"pvtkdzErr[5000]/D");

  //AnalysisTree->Branch("ntk",&m_ntk,"ntk/I");
  //AnalysisTree->Branch("tkpt",m_tkpt,"tkpt[ntk]/D");
  //AnalysisTree->Branch("tketa",m_tketa,"tketa[ntk]/D");
  //AnalysisTree->Branch("tkphi",m_tkphi,"tkphi[ntk]/D");
  //AnalysisTree->Branch("tkchi2norm",m_tkchi2norm,"tkchi2norm[ntk]/D");
  //AnalysisTree->Branch("tknhit",m_tknhit,"tknhit[ntk]/D");
  //AnalysisTree->Branch("tkd0",m_tkd0,"tkd0[ntk]/D");
  //AnalysisTree->Branch("tkd0Err",m_tkd0Err,"tkd0Err[ntk]/D");
  //AnalysisTree->Branch("tkdz",m_tkdz,"tkdz[ntk]/D");
  //AnalysisTree->Branch("tkdzErr",m_tkdzErr,"tkdzErr[ntk]/D");

}

  
void AnalysisRootpleProducer::analyze( const Event& e, const EventSetup& )
{
  ///
  /// Pythia: genEventScaleTag = "genEventScale"
  /// Herwig: genEventScaleTag = "genEventKTValue"
  ///

  // if ( e.getByLabel( genEventScaleTag, genEventScaleHandle ) ) genEventScale = *genEventScaleHandle;
 
  eventNum   = e.id().event() ;
  runNumber  = e.id().run() ;
  lumiBlock  = e.luminosityBlock() ;
  bx = e.bunchCrossing();
  if(!onlyRECO){
  Handle<GenEventInfoProduct> hEventInfo;
  e.getByLabel(genEventScaleTag , hEventInfo);
 if (hEventInfo->binningValues().size() > 0)
   { 
    genEventScale = hEventInfo->binningValues()[0];
   }  
 //partoni salvo
 Handle<reco::GenParticleCollection>  genParticles;
  reco::GenParticle p1;
  reco::GenParticle p2; 
  if (e.getByLabel("genParticles", genParticles))
    {
      for( size_t i = 0; i < genParticles->size(); ++ i ) {
 
      	if(i==4){p1 = (*genParticles)[ i ]; 
	new((*Parton)[0]) TLorentzVector(p1.px(), p1.py(), p1.pz(), p1.energy());
	} 
	if(i==5){p2 = (*genParticles)[ i ]; 
	new((*Parton)[i]) TLorentzVector(p2.px(), p2.py(), p2.pz(), p2.energy());
	}   
    
      }
    }

  }
// access trigger bits by TriggerEvent
  //   acceptedTriggers->Clear();
  //   unsigned int iAcceptedTriggers( 0 );
  //   if (e.getByLabel( triggerEventTag, triggerEvent ) )
  //     {
  //        // look at TriggerEvent 
  
  //       LogDebug("UEAnalysis") << "triggerEvent has " << triggerEvent.product()->sizeFilters() << " filters and "
  // 			     << "triggerEvent has " << triggerEvent.product()->sizeObjects() << " objects";
  
  //       LogDebug("UEAnalysis") << "size of object collection is " << triggerEvent.product()->getObjects().size() 
  // 			     << "usedProcessName() " << triggerEvent.product()->usedProcessName();
  
  //       for ( size_type index( 0 ) ; index < triggerEvent.product()->sizeFilters() ; ++index )
  // 	{
  // 	  LogDebug("UEAnalysis") << "filterLabel(size_type index) " << triggerEvent.product()->filterLabel(index);
  
  // 	  // save name of accepted trigger
  // 	  new((*acceptedTriggers)[iAcceptedTriggers]) TObjString( triggerEvent.product()->filterLabel(index).c_str() );
  // 	  ++iAcceptedTriggers;  
  // 	}
  //     }


  // access trigger bits by TriggerResults
  if (e.getByLabel( triggerResultsTag, triggerResults ) )
    {
      triggerNames.init( *(triggerResults.product()) );
      
      acceptedTriggers->Clear();
      unsigned int iAcceptedTriggers( 0 ); 
      if ( triggerResults.product()->wasrun() )
   	{
   	  LogDebug("UEAnalysis") << "at least one path out of " << triggerResults.product()->size() 
				 << " ran? " << triggerResults.product()->wasrun();
  
   	  if ( triggerResults.product()->accept() ) 
   	    {
   	      LogDebug("UEAnalysis") << "at least one path accepted? " << triggerResults.product()->accept() ;
  
   	      const unsigned int n_TriggerResults( triggerResults.product()->size() );
   	      for ( unsigned int itrig( 0 ); itrig < n_TriggerResults; ++itrig )
   		{
   		  LogDebug("UEAnalysis") << "path " << triggerNames.triggerName( itrig ) 
   					 << ", module index " << triggerResults.product()->index( itrig )
   					 << ", state (Ready = 0, Pass = 1, Fail = 2, Exception = 3) " << triggerResults.product()->state( itrig )
   					 << ", accept " << triggerResults.product()->accept( itrig );
  
     		  if ( triggerResults.product()->accept( itrig ) )
   		    {
   		      // save name of accepted trigger path
   		      new((*acceptedTriggers)[iAcceptedTriggers]) TObjString( (triggerNames.triggerName( itrig )).c_str() );
   		      ++iAcceptedTriggers;
   		    }
   		}
   	    }
   	}
    }

  // gen level analysis
  // skipped, if onlyRECO flag set to true
  
  if(!onlyRECO){
    
    e.getByLabel( mcEvent           , EvtHandle        );
    e.getByLabel( chgGenPartCollName, CandHandleMC     );
    e.getByLabel( chgJetCollName    , ChgGenJetsHandle );
    e.getByLabel( genJetCollName    , GenJetsHandle    );


    //Primary Vertex
 //primary vertex extraction --------------------------------------------------------------------------

    int ipv = 0;
  edm::Handle<reco::VertexCollection> primaryVertexHandle;
  e.getByLabel("offlinePrimaryVertices",primaryVertexHandle);
  if(primaryVertexHandle->size()>0){
    int ipvtk=0;
    int ipv=0;  
  for(reco::VertexCollection::const_iterator it = primaryVertexHandle->begin(), ed = primaryVertexHandle->end();
	it != ed; ++it) {
     reco::Vertex pv;
     pv = (*it);
     vertex_.pvx[ipv] = pv.x();
     vertex_.pvy[ipv] = pv.y();
     vertex_.pvz[ipv] = pv.z();
     
     vertex_.pvxErr[ipv] = pv.xError();
     vertex_.pvyErr[ipv] = pv.yError();
     vertex_.pvzErr[ipv] = pv.zError();
     
     
     for(reco::Vertex::trackRef_iterator pvt = pv.tracks_begin(); pvt!= pv.tracks_end(); pvt++){
       const reco::Track & track = *pvt->get();
       
       trackextraue_.pvtkpt[ipvtk]=track.pt();
       trackextraue_.pvtkp[ipvtk]=track.p();
       trackextraue_.pvtketa[ipvtk]=track.eta();
       trackextraue_.pvtkphi[ipvtk]=track.phi();
       trackextraue_.pvtkchi2norm[ipvtk]=track.normalizedChi2();
       trackextraue_.pvtkd0[ipvtk]=track.d0();
       trackextraue_.pvtkd0Err[ipvtk]=track.d0Error();
       trackextraue_.pvtkdz[ipvtk]=track.dz();
       trackextraue_.pvtkdzErr[ipvtk]=track.dzError();
       trackextraue_.pvtknhit[ipvtk]=track.recHitsSize();
       
       ipvtk++;
     }
       vertex_.pvntk[ipv] = pv.tracksSize();
       ipv++;
    }
  }
 vertex_.npv = ipv;
  



  ///-------------------------------
    const HepMC::GenEvent* Evt = EvtHandle->GetEvent() ;
    
    EventKind = Evt->signal_process_id();

    std::vector<math::XYZTLorentzVector> GenPart;
    std::vector<GenJet> ChgGenJetContainer;
    std::vector<GenJet> GenJetContainer;
    
    GenPart.clear();
    ChgGenJetContainer.clear();
    GenJetContainer.clear();
    MonteCarlo->Clear();
    InclusiveJet->Clear();
    ChargedJet->Clear();
    Parton->Clear();

    // jets from charged particles at hadron level
    if (ChgGenJetsHandle->size()){

      for ( GenJetCollection::const_iterator it(ChgGenJetsHandle->begin()), itEnd(ChgGenJetsHandle->end());
	    it!=itEnd; ++it)
	{
	  ChgGenJetContainer.push_back(*it);
	}

      std::stable_sort(ChgGenJetContainer.begin(),ChgGenJetContainer.end(),GenJetSort());

      std::vector<GenJet>::const_iterator it(ChgGenJetContainer.begin()), itEnd(ChgGenJetContainer.end());
      for ( int iChargedJet(0); it != itEnd; ++it, ++iChargedJet)
	{
	  new((*ChargedJet)[iChargedJet]) TLorentzVector(it->px(), it->py(), it->pz(), it->energy());
	}
    }


    // GenJets
    if (GenJetsHandle->size()){

      for ( GenJetCollection::const_iterator it(GenJetsHandle->begin()), itEnd(GenJetsHandle->end());
	    it!=itEnd; ++it )
	{
	  GenJetContainer.push_back(*it);

	  // 	  Jet::Constituents constituents( (*it).getJetConstituents() );
	  // 	  //cout << "get " << constituents.size() << " constituents" << endl;
	  // 	  for (int iJC(0); iJC<constituents.size(); ++iJC )
	  // 	    {
	  // 	      //cout << "[" << iJC << "] constituent pT = " << constituents[iJC]->pt() << endl;
	  // 	      if (constituents[iJC]->et()<0.5)
	  // 		{
	  // 		  cout << "ERROR!!! [" << iJC << "] constituent pT = " << constituents[iJC]->pt() << endl;
	  // 		}
	  // 	    }
	}

      std::stable_sort(GenJetContainer.begin(),GenJetContainer.end(),GenJetSort());

      std::vector<GenJet>::const_iterator it(GenJetContainer.begin()), itEnd(GenJetContainer.end());
      for ( int iInclusiveJet(0); it != itEnd; ++it, ++iInclusiveJet)
	{
	  new((*InclusiveJet)[iInclusiveJet]) TLorentzVector(it->px(), it->py(), it->pz(), it->energy());
	}
    }


    // hadron level particles
    if (CandHandleMC->size()){
    
      for (vector<GenParticle>::const_iterator it(CandHandleMC->begin()), itEnd(CandHandleMC->end());
	   it != itEnd;it++)
	{


	  //======
	  // 	  bool found( false );
	  // 	  for (int iParticle(0), iParticleEnd( pdgidList.size() ); iParticle<iParticleEnd; ++iParticle) 
	  // 	    {
	  // 	      //cout << "Particle pdgid " << it->pdgId() << " charge " << it->charge() << endl; 
	  // 	      if ( it->pdgId()==pdgidList[iParticle] )
	  // 		{
	  // 		  found = true;
	  // 		  break;
	  // 		}
	  // 	    }
	  // 	  if (!found) 
	  // 	    {
	  // 	      //cout << "Particle pdgid " << it->pdgId() << " status " << it->status() << endl; 
	  // 	      //cout << "Particle pdgid " << it->pdgId() << " charge " << it->charge() << endl;
	  // 	      pdgidList.push_back( it->pdgId() );
	  // 	    }
	  //======


	  GenPart.push_back(it->p4());
	}

      std::stable_sort(GenPart.begin(),GenPart.end(),GreaterPt());

      std::vector<math::XYZTLorentzVector>::const_iterator it(GenPart.begin()), itEnd(GenPart.end());
      for( int iMonteCarlo(0); it != itEnd; ++it, ++iMonteCarlo )
	{
	 
	  new((*MonteCarlo)[iMonteCarlo]) TLorentzVector(it->Px(), it->Py(), it->Pz(), it->E());
	
	}
    }

  } 

  
  // reco level analysis

  std::vector<math::XYZTLorentzVector> Tracks;
  std::vector<math::XYZPoint> AssVertices; 
  std::vector<CaloJet> RecoCaloJetContainer;
  std::vector<reco::TrackJet> TracksJetContainer;

  Tracks.clear();
  RecoCaloJetContainer.clear();
  TracksJetContainer.clear();
  //new   
  std::vector<math::XYZTLorentzVector> TracksT;
  TracksT.clear();

  Track->Clear();
  TracksJet->Clear();
  CalorimeterJet->Clear();


  if ( e.getByLabel( recoCaloJetCollName, RecoCaloJetsHandle ) )
    {
      if(RecoCaloJetsHandle->size())
	{
	  for(CaloJetCollection::const_iterator it(RecoCaloJetsHandle->begin()), itEnd(RecoCaloJetsHandle->end());
	      it!=itEnd;++it)
	    {
	      RecoCaloJetContainer.push_back(*it);
	    }
	  std::stable_sort(RecoCaloJetContainer.begin(),RecoCaloJetContainer.end(),CaloJetSort());
	  
	  std::vector<CaloJet>::const_iterator it(RecoCaloJetContainer.begin()), itEnd(RecoCaloJetContainer.end());
	  for( int iCalorimeterJet(0); it != itEnd; ++it, ++iCalorimeterJet)
	    {
	      new((*CalorimeterJet)[iCalorimeterJet]) TLorentzVector(it->px(), it->py(), it->pz(), it->energy());
	    }
	}
    }
    
  
if ( e.getByLabel( tracksJetCollName, TracksJetsHandle ) )
    {
      if(TracksJetsHandle->size())
	{
	  for(reco::TrackJetCollection::const_iterator it(TracksJetsHandle->begin()), itEnd(TracksJetsHandle->end());
	      it!=itEnd;++it)
	    {
	      TracksJetContainer.push_back(*it);

	      // 	      Jet::Constituents constituents( (*it).getJetConstituents() );
	      // 	      //cout << "get " << constituents.size() << " constituents" << endl;
	      // 	      for (int iJC(0); iJC<constituents.size(); ++iJC )
	      // 		{
	      // 		  //cout << "[" << iJC << "] constituent pT = " << constituents[iJC]->pt() << endl;
	      // 		  if (constituents[iJC]->et()<0.5)
	      // 		    {
	      // 		      cout << "ERROR!!! [" << iJC << "] constituent pT = " << constituents[iJC]->pt() << endl;
	      // 		    }
	      // 		}
	    }
	  std::stable_sort(TracksJetContainer.begin(),TracksJetContainer.end(),BasicJetSort());
	  
          int iJCall=0;
	  std::vector<reco::TrackJet>::const_iterator it(TracksJetContainer.begin()), itEnd(TracksJetContainer.end());
	  for(int iTracksJet(0); it != itEnd; ++it, ++iTracksJet)
	    {

	      Jet::Constituents constituents( (*it).getJetConstituents() );
	      trackinjet_.tkn[iTracksJet]=constituents.size();
	      for (int iJC(0); iJC<constituents.size(); ++iJC )
		{
		 
		  trackinjet_.tkp[iJCall]=constituents[iJC]->p();
		  trackinjet_.tkpt[iJCall]=constituents[iJC]->pt();
		  trackinjet_.tketa[iJCall]=constituents[iJC]->eta();
		  trackinjet_.tkphi[iJCall]=constituents[iJC]->phi();
		  //  trackinjet_.tknhit[iJCall]=constituents[iJC]->recHitsSize();
		  //  trackinjet_.tkchi2norm[iJCall]=constituents[iJC]->normalizedChi2();
		  //  trackinjet_.tkd0[iJCall]=constituents[iJC]->d0();
		  //  trackinjet_.tkd0Err[iJCall]=constituents[iJC]->d0Err();
		  //  trackinjet_.tkdz[iJCall]=constituents[iJC]->dz();
		  //  trackinjet_.tkdzErr[iJCall]=constituents[iJC]->dzErr();
		  iJCall++;
		}

	      new((*TracksJet)[iTracksJet]) TLorentzVector(it->px(), it->py(), it->pz(), it->energy());
	    }
	}
    }

// edm::Handle< reco::TrackCollection  > trackColl;
// e.getByLabel(tracksCollName,trackColl);


// for (reco::TrackCollection::const_iterator it = trackColl->begin();
//                                           it != trackColl->end();
//                                           it++){
//   m_tkpt[m_ntk]=it->pt();
//   m_tkp[m_ntk]=it->p();
//   m_tketa[m_ntk]=it->eta();
//   m_tkphi[m_ntk]=it->phi();
//   m_tkchi2norm[m_ntk]=it->normalizedChi2();
//   m_tkd0[m_ntk]=it->d0();
//   m_tkd0Err[m_ntk]=it->d0Error();
//   m_tkdz[m_ntk]=it->dz();
//   m_tkdzErr[m_ntk]=it->dzError();
    
//   m_ntk++;    
//   }


 int iTracks=0;
  if ( e.getByLabel( tracksCollName , CandHandleRECO ) )
    {
      if(CandHandleRECO->size())
	{
	  
	  //for(CandidateCollection::const_iterator it(CandHandleRECO->begin()), itEnd(CandHandleRECO->end());
	  for(edm::View<reco::Candidate>::const_iterator it(CandHandleRECO->begin()), itEnd(CandHandleRECO->end());
	      it!=itEnd;++it)
	    {

    	     
	      new ((*Track)[iTracks]) TLorentzVector(it->p4().Px(), it->p4().Py(), it->p4().Pz(), it->p4().E());	
	     new ((*AssVertex)[iTracks]) TLorentzVector(it->vertex().x(),it->vertex().y(),it->vertex().z(),0); 
	     iTracks++; 
	    }
	  // std::stable_sort(Tracks.begin(),Tracks.end(),GreaterPt());
	  
	  //  std::vector<math::XYZTLorentzVector>::const_iterator it( Tracks.begin()), itEnd(Tracks.end());
	  //   for(int iTracks(0); it != itEnd; ++it, ++iTracks)
	  //  {
	  //   new ((*Track)[iTracks]) TLorentzVector(it->Px(), it->Py(), it->Pz(), it->E());
	  
	  //   }
	}
    }
  
  store();
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

