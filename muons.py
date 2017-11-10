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

def get_lepton_pairs(leptons):
    """
    Return all possible combinations of pairs except those
    where the pair is made of the same lepton. Returns the 
    combined four-momentum as a list of TLorentzVectors.
    """
    pairs = []
    n_leptons = len(leptons)
    for p_i in range(n_leptons-1):
        for p_j in range(p_i+1, n_leptons):
            pair = leptons[p_i] + leptons[p_j]
            pairs.append(pair)
    return pairs

data = TChain("mini")
data.Add("/home/jdobson/SoftwareCarpentry/DataMuons.root")

num_events = data.GetEntries()
print("Number of events = "+str(num_events))

h_mpair = TH1F("h_mpair", "#mu pair invariant mass; GeV/c^{2}; Events/bin", 200, 50.0, 150.0)

num_events_to_process = 100000 # for testing
for i_event in range(num_events_to_process):
    data.GetEntry(i_event)
    n_leptons = data.lep_n
    if n_leptons >= 2: # looking for pairs of leptons
        p_leptons = [get_four_momenta(data, i) for i in range(n_leptons)] 
        print("Found {} leptons:".format(len(p_leptons)))
        for p in sorted(p_leptons, key=lambda x: x.Pt()): # print based on decreasing mass
            print("  -> Pt {}", p.Pt())
        pairs = get_lepton_pairs(p_leptons)
        for pair in pairs:
            print("   -> Invariant mass of pair = {}".format(pair.M()))
            h_mpair.Fill(pair.M()/1E3)

h_mpair.Draw()
raw_input("Exit?") 
