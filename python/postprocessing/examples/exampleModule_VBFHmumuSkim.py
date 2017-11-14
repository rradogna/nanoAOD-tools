import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class exampleProducer(Module):
    def __init__(self, jetSelection, muSelection):
        self.jetSel = jetSelection
        self.muSel = muSelection
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("EventMass",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        selectEvent = True
        mu1 = ROOT.TLorentzVector()
        mu2 = ROOT.TLorentzVector()
        jet1 = ROOT.TLorentzVector()
        jet2 = ROOT.TLorentzVector()
        mu1_charge = 0
        count_mu = 0
        count_jet = 0
        dimuonSelection = False
        dimuonSelectionH = False
        dijetSelection = False
        dijetSelectionVBF = False
        dimuon = ROOT.TLorentzVector()
        dijet = ROOT.TLorentzVector()
        eventSum = ROOT.TLorentzVector()
        if len(filter(self.muSel,muons)) < 2:
            return False
        for lep in muons :
            eventSum += lep.p4()
            #print 'lep pt='+repr(lep.pt)+' lep charge='+repr(lep.charge)+' lep pfRelIso04_all='+repr(lep.pfRelIso04_all)+' lep pdgId='+repr(lep.pdgId)
            if lep.pfRelIso04_all<0.25 and abs(lep.pdgId)==13:
                #print 'here'
                if count_mu == 1 and (lep.charge*mu1_charge)<0:
                    mu2 = lep.p4()
                    dimuonSelection = True
                #print 'dimuonSel'
                if count_mu == 0:
                    #mu1.SetPtEtaPhiM(lep.pt,lep.eta, lep.phi, 0.105)
                    mu1 = lep.p4()
                    mu1_charge = lep.charge
                    count_mu +=1
        if dimuonSelection and (mu1.Pt()>30 or mu2.Pt()>30):
            dimuon = mu1 + mu2
            if dimuon.M()>90:
                dimuonSelectionH = True
        #print 'dimuonSelH'
        #for lep in electrons :
        #    eventSum += lep.p4()
        if len(filter(self.jetSel,jets)) < 2:
            return False
        for j in filter(self.jetSel,jets):
            eventSum += j.p4()
            if j.jetId>2 and j.puId>0:
                if count_jet ==1:
                    jet2=j.p4()
                    dijetSelection = True
                if count_jet == 0:
                    jet1=j.p4()
                    count_jet +=1
        if dijetSelection and (jet1.Pt()>32 or jet2.Pt()>32):
            dijet = jet1 + jet2
            if dijet.M()>150:
                dijetSelectionVBF = True
        
        self.out.fillBranch("EventMass",eventSum.M())
        return dimuonSelection*dimuonSelectionH and dijetSelection and dijetSelectionVBF


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

exampleModule_VBFHmumuSkim = lambda : exampleProducer(jetSelection= lambda j : j.pt > 20, muSelection= lambda mu : mu.pt > 10)
 
