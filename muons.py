#!/usr/bin/env python
from ROOT import TChain
data = TChain("mini")
data.Add("http://opendata.atlas.cern.release/samples/Data/DataMuons.root")
