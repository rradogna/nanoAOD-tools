#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  exampleModule_VBFHmumuSkim import *
p=PostProcessor(".",["root://cmsxrootd.fnal.gov//store/user/arizzi/NanoTest3/VBF_HToMuMu_M125_13TeV_powheg_pythia8/NanoTest3/171103_143903/0000/nanoaod_1.root"],"Jet_pt>20 && Muon_pt > 10","keep_and_drop_VBFHmumuSkim.txt",[exampleModule_VBFHmumuSkim()],provenance=True)
p.run()
