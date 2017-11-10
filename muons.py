#!/usr/bin/env python
from ROOT import TChain
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

