#!/snap/bin/pyroot

# jk 23.11.2023 -- 25.11.2023, 10.12.2023
# plotting JES-like systs

import ROOT

from Tools import *

ROOT.gStyle.SetOptTitle(0)

sel = "AnySel/"
#sel = "2B0S"

fnames = [ "root_2021/analyzed_histos_pp_2tj_allhad_NLO_ALL_14TeV_ATLAS_weighted_all.root",
           "root_2023_SYST_smearedJets_jesSlopeP1p0/analyzed_histos_pp_2tj_allhad_NLO_ALL_14TeV_ATLAS_weighted_all.root" ]

cols = [ROOT.kBlack, ROOT.kRed]

hnames = ["DetectorLJetPt", "DetectorLJetMass", "DetectorHTj", "DetectorDiTopMass_denser"]

rfiles = []
for fname in fnames:
    rfile = ROOT.TFile(fname, 'read')
    print(rfile)
    rfiles.append(rfile)

rb = 5
Hs = []
ifile = -1
for rfile in rfiles:
    ifile = ifile + 1
    hs = []
    for hname in hnames:
        h = rfile.Get(sel + hname)
        print(h)
        print(h.GetStdDev())
        print(h.Integral())
        
        h.SetLineColor(cols[ifile])
        if not ('HT' in hname or 'DiTop' in hname):
            h.Rebin(rb)
        DivideByBinWidth(h)
        h.SetStats(0)
        hs.append(h)

    Hs.append(hs)
    
#cans = []
canname = ''
#canname = "cmpCan" + "_" + sel + "_" + hname
can = ROOT.TCanvas(canname, canname, 1, 1, 1000, 1000)
can.Divide(2,2)


for ih in range(0,len(Hs[0])):
    opt = ''
    for ifile in range(0,len(Hs)):
        can.cd(ih+1)        
        Hs[ifile][ih].Draw('hist' + opt)
        opt = 'same'
  
  #can.Update()
  #can.Print(TString(can.GetName()) + ".png")
  #can.Print(TString(can.GetName()) + ".pdf")
  

can.cd()
ROOT.gPad.Update()
ROOT.gApplication.Run()
