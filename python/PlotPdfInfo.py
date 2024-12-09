#!/snap/bin/pyroot

#/usr/bin/python
# Sat 29 May 10:16:43 CEST 2021

from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

from Tools import DivideByBinWidth

pdgidDict = { 21 : 'g',
           1 : 'd',
           2 : 'u',
           3 : 's',
           4 : 'c',
          -1 : '#bar{d}',
          -2 : '#bar{u}',
          -3 : '#bar{s}',
          -4 : '#bar{c}',
         }

cans = []
stuff = []

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]

    ### https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    ### https://pymotw.com/2/getopt/
    ### https://docs.python.org/3.1/library/getopt.html
    gBatch = False
    gTag=''
    print(argv[1:])
    try:
        # options that require an argument should be followed by a colon (:).
        opts, args = getopt.getopt(argv[2:], 'hbt:', ['help','batch','tag='])

        print('Got options:')
        print(opts)
        print(args)
    except getopt.GetoptError:
        print('Parsing...')
        print ('Command line argument error!')
        print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]]'.format(argv[0]))
        sys.exit(2)
    for opt,arg in opts:
        print('Processing command line option {} {}'.format(opt,arg))
        if opt == '-h':
            print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]'.format(argv[0]))
            sys.exit()
        elif opt in ("-b", "--batch"):
            gBatch = True
        elif opt in ("-t", "--tag"):
            gTag = arg
            print('OK, using user-defined histograms tag for output pngs {:}'.format(gTag,) )

    if gBatch:
        ROOT.gROOT.SetBatch(1)

    ROOT.gStyle.SetPalette(ROOT.kSolar)
    
    print('*** Settings:')
    print('tag={:}, batch={:}'.format(gTag, gBatch))

    cw = 800
    ch = 600

    ROOT.gStyle.SetOptTitle(0)

     
    scanname = 'shat'
    scan = ROOT.TCanvas(scanname, scanname, 0, 0, cw, ch)
    cans.append(scan)

    canname = 'flavour_fractions'
    fcan = ROOT.TCanvas(canname, canname, 150, 150, cw, ch)
    cans.append(fcan)

    filename = 'foo.root'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    rfile = ROOT.TFile(filename, 'read')

    collider = ''
    if 'pbar' in filename:
        collider = 'Tevatron p#bar{p} #sqrt{S}=1.96 TeV'
    else:
        collider = 'LHC pp #sqrt{S}=14 TeV'
    maintxt = ROOT.TLatex(0.12, 0.92, collider)
    maintxt.SetNDC()
    stuff.append(maintxt)
    
    pbartag = ''
    if 'pbar' in filename:
        pbartag = '_ppbar'
    
    dirname='pdfinfo/'
    hname = 'InitPartonsFracs'
    hInitPartonsFracs = rfile.Get(dirname + hname)
    hInitPartonsFracs.Scale(1./hInitPartonsFracs.Integral())

    canname = 'ffractions'
    gcan = ROOT.TCanvas(canname, canname, 250, 250, cw, ch)
    cans.append(gcan)
    gcan.cd()
    hInitPartonsFracs.SetMarkerSize(1.5)
    hInitPartonsFracs.SetLineColor(ROOT.kBlack)
    hInitPartonsFracs.SetMarkerStyle(20)
    hInitPartonsFracs.SetMinimum(0.)
    hInitPartonsFracs.SetMaximum(1.)
    hInitPartonsFracs.GetXaxis().SetLabelSize(0.08)
    hInitPartonsFracs.SetStats(0)
    hInitPartonsFracs.Draw('e1')
    maintxt.Draw()
    gcan.Update()
 
    
    qgs = ['gg', 'qg', 'qq']
    dcols = {'gg' : ROOT.kPink, 'qq' : ROOT.kSpring, 'qg' : ROOT.kCyan+2} 
    hshat = {}
    ints = {}

    s1 = 0.25
    s2 = 2. # TeV in range of sqrt(shat)
    
    htot = ROOT.TH1D('dum', 'dum', 10, s1, s2)
    for qg in qgs:
        basename = 'InitPartonsFracsSqrtshat_'
        h = rfile.Get(dirname + basename + qg)
        DivideByBinWidth(h)
        #h.Rebin(2)
        h.SetStats(0)
        h.GetXaxis().SetTitle('#hat{s} [TeV]')
        h.GetYaxis().SetTitle('normalized events')
        h.SetLineColor(dcols[qg])
        hshat[qg] = h
        ints[qg] = h.Integral(0, h.GetNbinsX(), 'width')
        if htot.GetEntries() <= 1e-4:
            htot = h.Clone('shat_tot')
        else:
            htot.Add(h)

    scan.cd()
    opt = ''
    ROOT.gPad.SetLogy(1)
    for qg in qgs:
        h = hshat[qg]
        h.SetLineWidth(2)
        h.GetXaxis().SetRangeUser(s1,s2)
        h.Draw('hist' + opt)
        opt = 'same'
    
            
    sname = 'shat_stack'
    hstack = ROOT.THStack(sname, sname)
    hfrac = {}
    delta = 0.07
    #fleg = ROOT.TLegend(0.80, 0.65, 0.88, 0.82)
    fleg = ROOT.TLegend(0.91, 0.50 - delta, 1., 0.50 + delta)
    fleg.SetBorderSize(0)
    lqg = []
    for qg in qgs:
        lqg.append(qg)
        ratio = hshat[qg].Clone(hshat[qg].GetName() + '_ratio')
        ratio.Divide(htot)
        ratio.SetFillColor(dcols[qg])
        ratio.SetFillStyle(1001)
        ratio.SetLineWidth(1)
        hfrac[qg] = ratio
        hstack.Add(hfrac[qg], 'hist')
    lqg.reverse()
    for qg in lqg:
        fleg.AddEntry(hfrac[qg], qg, 'F')

    fcan.cd()
    #s2 = 2. # TeV!
    eps = 0.004
    h2 = ROOT.TH2D('dum2', 'dum2;#hat{s} [TeV];fraction', 100, s1, s2, 100, 0. - eps, 1. + eps)
    h2.SetStats(0)
    h2.Draw()
    hstack.Draw('hist same')
    #hstack.GetXaxis().SetRangeUser(s1,s2)
    #hstack.GetYaxis().SetRangeUser(0.,1.)
    fleg.Draw()
    maintxt.Draw()
    ROOT.gPad.Update()

    scan.cd()
    fleg.Draw()
    
    
    pdgid = [21, -4, -3, -2, -1, 1, 2, 3, 4]
    hx = {}
    for pdg in pdgid:
        hx[pdg] = rfile.Get(dirname + 'h_xPdfHisto_' + str(pdg))
        DivideByBinWidth(hx[pdg])

    canname = 'pdfx'
    canx = ROOT.TCanvas(canname, canname, 300, 100, cw, ch)
    cans.append(canx)
    ROOT.gPad.SetLogy(1)
    cols = [ROOT.kRed, ROOT.kBlack, ROOT.kGreen + 2, ROOT.kBlue, ROOT.kViolet]
    opt = ''
    ymax = -1
    for pdg in hx:
        hmax = hx[pdg].GetMaximum()
        #hx[pdg].Rebin(10)
        hx[pdg].SetStats(0)
        hx[pdg].GetXaxis().SetTitle('x')
        #hx[pdg].Scale(1./hx[pdg].Integral(0, hx[pdg].GetNbinsX(), 'width'))
        if ymax < hmax:
            ymax = 15*hmax
    xleg = ROOT.TLegend(0.69, 0.55, 0.89, 0.89)
    xleg.SetBorderSize(0)
    for pdg in hx:
        i = abs(pdg)
        if i > 20:
            i = 0
        h = hx[pdg]
        h.SetMaximum(ymax)
        h.SetLineColor(cols[i])
        h.SetLineWidth(2)
        if pdg < 0:
            h.SetLineStyle(2)
        h.Draw('hist' + opt)
        #xleg.AddEntry(h, 'PDGID ' + str(pdg) + ',  <x>' + '={:1.3f}'.format(h.GetMean()), 'L')
        xleg.AddEntry(h, '{}'.format(pdgidDict[pdg]) + ' <x>' + '={:1.3f}'.format(h.GetMean()), 'L')
        opt = 'same'
    xleg.Draw()
    maintxt.Draw()
    ROOT.gPad.Update()

    canname = 'pdfx1vsx2'
    canx1vsx2 = ROOT.TCanvas(canname, canname, 300, 300, cw, ch)
    cans.append(canx1vsx2)
    canx1vsx2.cd()
    hname = 'PdfIfo_x1vsx2'
    h2x1vsx2 = rfile.Get(dirname + hname)
    h2x1vsx2.SetStats(0)
    h2x1vsx2.Draw('colz')
    maintxt.Draw()
    ROOT.gPad.Update()

    canname = 'pdfsqrtx1x2'
    cansqrtx1x2 = ROOT.TCanvas(canname, canname, 500, 500, cw, ch)
    cans.append(cansqrtx1x2)
    cansqrtx1x2.cd()
    ROOT.gPad.SetLogy(1)
    hname = 'PdfIfo_sqrtx1x2'
    h2sqrtx1x2 = rfile.Get(dirname + hname)
    h2sqrtx1x2.SetFillColor(ROOT.kCyan)
    h2sqrtx1x2.SetStats(0)
    #txt = ROOT.TLatex(0.62, 0.84, r'\langle\sqrt{x_{1}x_{2}}\,\rangle=' + '{:1.3f}'.format(h2sqrtx1x2.GetMean()))
    txt = ROOT.TLatex(0.62, 0.84, r'<#sqrt{x_{1}x_{2}}>=' + '{:1.3f}'.format(h2sqrtx1x2.GetMean()))
    txt.SetNDC()
    stuff.append(txt)
    h2sqrtx1x2.Draw('hist')
    txt.Draw()
    maintxt.Draw()
    ROOT.gPad.Update()

    for can in cans:
        can.Print('pdf/' + can.GetName() + pbartag + '.pdf')
        can.Print('png/' + can.GetName() + pbartag + '.png')
        
    ROOT.gApplication.Run()
    return

###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

