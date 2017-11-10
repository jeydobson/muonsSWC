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
        p_leptons = [get_four_momenta(data, i) for i in range(n_leptons)] 
        print("Found {} leptons:".format(len(p_leptons)))
        for p in p_leptons:
            print("  -> Pt {}", p.Pt())
        # TODO: deal with > 2 muon cases
        ppair = p_leptons[0] + p_leptons[1]
        mpair = ppair.M()
        print("Invariant mass of the first two muons = {}".format(mpair))
        h_mpair.Fill(mpair/1E3)

h_mpair.Draw()
raw_input("Exit?") 
