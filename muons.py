#!/usr/bin/env python
from ROOT import TChain, TLorentzVector
data = TChain("mini")
data.Add("/home/jdobson/SoftwareCarpentry/DataMuons.root")

num_events = data.GetEntries()
print("Number of events = "+str(num_events))

num_events_to_process = 1000 # for testing
for i_event in range(num_events_to_process):
    data.GetEntry(i_event)
    n_leptons = data.lep_n
    if n_leptons >= 2:
        print("Number of leptons = "+str(n_leptons))
        assert n_leptons==2
        pt1 = data.lep_pt[0]
        pt2 = data.lep_pt[1]
        print("Lepton Pts are: {} and {}".format(pt1, pt2))
        p1 = TLorentzVector()
        p1.SetPtEtaPhiE(data.lep_pt[0], data.lep_eta[0], data.lep_phi[0], data.lep_E[0])        
        p2 = TLorentzVector()
        p2.SetPtEtaPhiE(data.lep_pt[1], data.lep_eta[1], data.lep_phi[1], data.lep_E[1])
        print("Pts from TLorentzVector are {} and {}".format(p1.Pt(), p2.Pt())) 
