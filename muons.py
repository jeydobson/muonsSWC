#!/usr/bin/env python
from ROOT import TChain, TLorentzVector, TH1F, gPad

def get_four_momenta(data, ilepton):
    """
    Get the four-momentum of a given lepton from TTree data and
    return the result as a TLorentzVector. ilepton starts from 0
    and the function assumes GetEntry has been called and number
    of leptons has been checked.
    """
    pt = TLorentzVector()
    pt.SetPtEtaPhiE(data.lep_pt[ilepton] , \
                    data.lep_eta[ilepton], \
                    data.lep_phi[ilepton], \
                    data.lep_E[ilepton]) 
    return pt

data = TChain("mini")
data.Add("/home/jdobson/SoftwareCarpentry/DataMuons.root")

num_events = data.GetEntries()
print("Number of events = "+str(num_events))

h_mpair = TH1F("h_mpair", "#mu pair invariant mass; GeV/c^{2}; Events/bin", 200, 50.0, 150.0)

num_events_to_process = 1000 # for testing
for i_event in range(num_events_to_process):
    data.GetEntry(i_event)
    n_leptons = data.lep_n
    if n_leptons >= 2: # looking for pairs of leptons
        print("Number of leptons = "+str(n_leptons))
        assert n_leptons==2
        pt1 = data.lep_pt[0]
        pt2 = data.lep_pt[1]
        print("Lepton Pts are: {} and {}".format(pt1, pt2))
        p1 = get_four_momenta(data, 0)
        p2 = get_four_momenta(data, 1)
        print("Pts from TLorentzVector are {} and {}".format(p1.Pt(), p2.Pt()))
        ppair = p1 + p2
        mpair = ppair.M()
        print("Invariant mass of the two muons = {}".format(mpair))
        h_mpair.Fill(mpair/1E3)

h_mpair.Draw()
gPad.Update()
raw_input("Exit?") 
