#!/snap/bin/pyroot

import ROOT
from math import cosh

# just for a test
class LJet:
    def __init__(self, PT, Eta, Phi, M):
        self.PT = PT
        self.Eta = Eta
        self.Phi = 0.
        self.M = M

calib_file = ROOT.TFile("data/JESfits.root")


# BEFORE THE EVENT LOOP
# get the TF2, function of eta and E
# which is the jet response, i.e. E_det / E_ptcl of angularly matched jets
jesfun = calib_file.Get("fit2d_JESRPtLJetsEtaE")

# TO APPLY IN THE EVENT LOOP
# derive the correction for each jet used in the loop:

# created just some random dummy "jet"
myLJet = LJet(240., 1., 0., 172.)

jesc = 1./ jesfun.Eval(myLJet.PT * cosh(myLJet.Eta), myLJet.Eta);
print(jesc)



