#!/usr/bin/env python
from ROOT import TChain, TLorentzVector, TH1F, gPad

class Particle:
    def __init__(self, p, q):
        self.p = p
        self.q = q

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

def get_leptons_from_event(data):
    leptons = []
    for ilepton in range(data.lep_n):
        particle = Particle(get_four_momenta(data, ilepton), data.lep_charge[ilepton])
        leptons.append(particle) 
    return leptons

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
            pair = [leptons[p_i], leptons[p_j]]
            pairs.append(pair)
    return pairs

def get_opposite_charge_pairs(pairs):
    """
    Take a set of pairs of Particle objects and return a 
    list of those whose individual particles have opposite 
    sign.
    """
    opposite_pairs = []
    for pair in pairs:
        if pair[0].q != pair[1].q: 
            opposite_pairs.append(pair)
    return opposite_pairs

def get_mass_of_pair(pair):
    """
    Get invariant mass of pair (list size 2) of Particle objects.
    """
    p_pair = pair[0].p+pair[1].p
    return p_pair.M() 

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
        leptons = get_leptons_from_event(data)
        print("Found {} leptons:".format(len(leptons)))
        for p in sorted(leptons, key=lambda x: x.p.Pt()): # print based on decreasing mass
            print("  -> Pt {}", p.p.Pt())
        pairs = get_lepton_pairs(leptons)
        opposite_sign_pairs = get_opposite_charge_pairs(pairs)
        for pair in opposite_sign_pairs: 
            m_pair = get_mass_of_pair(pair) 
            print("   -> Invariant mass of pair = {}".format(m_pair))
            h_mpair.Fill(m_pair/1E3) # convert from MeV to GeV

h_mpair.Draw()
raw_input("Exit?") 
