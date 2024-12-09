#!/snap/bin/pyroot
#!/usr/bin/python
# jk 26.2.2018, 30.3.2018, 2.12.2019, 11.6.2020

from __future__ import print_function

from DrawUnfolded import *
from Tools import MakePrettyTitle

import os, sys

stuff = []

rebin = -1 # !!!

UnfToDraw = [
    cUnfToDraw('unfolded_2B0S_DetectorDiTopMass_ttbarPlusSig.root', 'DiTopMass'),
    cUnfToDraw('unfolded_1B1S_DetectorDiTopMass_ttbarPlusSig.root', 'DiTopMass'),
    cUnfToDraw('unfolded_0B2S_DetectorDiTopMass_ttbarPlusSig.root', 'DiTopMass')
]

ROOT.gStyle.SetPaintTextFormat("1.2f")
ROOT.gStyle.SetPalette(1)

os.system('mkdir -p png/unfolded/')
os.system('mkdir -p pdf/unfolded/')

for unfToDraw in UnfToDraw:
    print('Processing {}'.format(unfToDraw.fname) )
    print('Drawing unfolded results for {} from file {}'.format(unfToDraw.fname, unfToDraw.varname,))
    DrawUnfolded(unfToDraw)

ROOT.gApplication.Run()
