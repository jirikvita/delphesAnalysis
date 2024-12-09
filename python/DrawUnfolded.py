#!/usr/bin/python


# jk 2.2.2018, 26.2.2018, 30th March 2018
# major revision 2.7.2022, 1.8.2022

import ReadTools
from Tools import MakeMultiSubPads
from xSectTools import DrawNiceRatioWithBand
import ROOT
from cUnfSuffixes import *

from Tools import MakeOneWithoutErrors
from Tools import MakeOneWithErrors
from xSectTools import DrawSignificance


#######################################################################
#######################################################################
#######################################################################

class cUnfToDraw:
    
    # ---------------------------------------------------------------------
    
    def __init__(self, fname, varname):
        self.fname = fname
        self.topo = self.fname.split('_')[1]
        self.varname = varname # equivalent, but more fragile: self.fname.split('_')[2].replace('Detector','')
        self.truthlevel = 'Particle'
        self.detlevel = 'Detector'
        self.xlabel = ''
        self.rebin = -1
        self.Normalize = False
        self.migraname = 'matrix_{}_{}_{}_Detector_migra'.format(self.topo, self.varname, self.truthlevel)
        self.PrintNames()
        # marker size:
        self.msz = 2.

    # ---------------------------------------------------------------------

    def PrintNames(self):
        print('varname: {}'.format(self.varname))
        print('topo: {}'.format(self.topo))

    # ---------------------------------------------------------------------
    
    def ReadInputs(self):
        self.unfSuffixes = cUnfSuffixes()
        
        self.rfile = ROOT.TFile(self.fname, 'read')
        # note: varname is gotten from the fname
        # and in my case this is typically unfolded_2B0S_DetectorDiTopMass_ttbarPlusSig.root
        # so the data_bgSub is not really bg subtracted in the sense that the phys. bg unc. would bepropagated
        # but it is really ttabr+BSM signal!
        self.h_data_bgSub = self.rfile.Get('{}{}_{}'.format(self.detlevel, self.varname, self.unfSuffixes.ttbarPlusSig))
        
        self.h_data_bgSub_accApp = self.rfile.Get('{}{}_{}_accApp'.format(self.detlevel, self.varname, self.unfSuffixes.ttbarPlusSig))
        self.xlabel = self.h_data_bgSub.GetXaxis().GetTitle()
        
        tname = '{}{}_{}_effApp'.format(self.truthlevel, self.varname, self.unfSuffixes.ttbarPlusSig)
        print(tname)
        self.h_ptcl_effApp = self.rfile.Get(tname)
        tname = '{}{}_{}'.format(self.truthlevel, self.varname, self.unfSuffixes.ttbarPlusSig)
        print(tname)
        self.h_ptcl = self.rfile.Get(tname)

        tname = '{}{}_{}_effApp'.format(self.truthlevel, self.varname, self.unfSuffixes.ttbar)
        print(tname)
        self.h_ptcl_noSig_effApp = self.rfile.Get(tname)
        tname = '{}{}_{}'.format(self.truthlevel, self.varname, self.unfSuffixes.ttbar)
        print(tname)
        self.h_ptcl_noSig = self.rfile.Get(tname)
 
        self.h_unfolded = self.rfile.Get('h_unfolded')
        self.h_unfolded.SetMarkerStyle(24)
        #self.h_unfolded.SetMarkerColor(ROOT.kGreen+2)
        #self.h_unfolded.SetLineColor(ROOT.kGreen+2)
        self.h_unfolded_effCorr = self.rfile.Get('h_unfolded_effCorr')
        self.h_unfolded_effCorr.SetMarkerStyle(20)
        self.h_unfolded_effCorr.SetMarkerSize(self.msz)
        self.h_unfolded_effCorr.SetMarkerColor(ROOT.kMagenta)
        self.h_unfolded_effCorr.SetLineColor(ROOT.kMagenta)

        # for detector-level significance
        self.h_det_ttbar = self.rfile.Get('{}{}_ttbar'.format(self.detlevel, self.varname))
        
        mname = self.migraname
        print(mname)
        self.h_migra = self.rfile.Get(mname)

        self.eff = self.rfile.Get('eff_{}_{}'.format(self.topo, self.varname))
        self.acc = self.rfile.Get('acc_{}_{}'.format(self.topo, self.varname))

        self.h_data_bgSub_acceffCorr = self.h_data_bgSub.Clone(self.h_data_bgSub.GetName() + '_acceffCorr')
        self.h_data_bgSub_acceffCorr.Multiply(self.acc)
        self.h_data_bgSub_acceffCorr.Divide(self.eff) 
        
        self.canname = self.fname.replace('unfolded_', 'XYZ_').replace('.root', '')
        self.origcanname = self.canname + ''

        self.hxmin = self.h_unfolded_effCorr.GetXaxis().GetXmin()
        self.hxmax = self.h_unfolded_effCorr.GetXaxis().GetXmax()


    # ---------------------------------------------------------------------


    def PlotIngredients(self):

        # add the unfolded data to the first comparison plot

        self.canname = self.origcanname.replace('XYZ', 'Ingredients').replace('.root', '')
        
        self.cantitle = self.canname
        if '/' in self.canname:
            self.cantags = self.canname.split('/')
            self.canname = self.cantags[-1]
            self.cantitle = ''
            for cantag in self.cantags[:-2]:
                self.cantitle = self.cantitle + '_' + cantag

        self.can,self.hists = ReadTools.PlotIngredients(self.h_data_bgSub, self.h_data_bgSub_accApp,
                                                        self.h_ptcl_effApp, self.h_migra,
                                                        self.canname, self.cantitle, self.truthlevel)
        self.can.cd(1)
        unfcol = ROOT.kGreen+2
        self.h_unfolded.SetLineColor(unfcol)
        self.h_unfolded.SetLineStyle(1)
        self.h_unfolded.SetLineWidth(1)
        self.h_unfolded.SetMarkerColor(unfcol)
        self.h_unfolded.SetMarkerStyle(20)
        self.h_unfolded.SetMarkerSize(self.msz)

        leg = ReadTools.Legs[-1]
        leg.AddEntry(self.h_data_bgSub, 'data-Bg', 'PL')
        leg.AddEntry(self.h_data_bgSub_accApp, 'acc*(data-Bg)', 'PL')
        leg.AddEntry(self.h_ptcl_effApp, 'eff*{}'.format(self.truthlevel), 'PL')
        leg.SetBorderSize(0)
        leg.Draw()

        ROOT.gPad.Update()
        
        # better would be a dictionary;)
        self.Hists = [self.h_ptcl, self.h_ptcl_effApp,
                      self.h_unfolded, self.h_unfolded_effCorr,
                      self.h_data_bgSub, self.h_data_bgSub_accApp]
        self.Labels = ['{}'.format(self.truthlevel),
                       'eff*{}'.format(self.truthlevel),
                       'Unfolded',
                       'Unfolded / eff',
                       'Data-Bg', 'acc*(data-Bg)']
        for hist in self.Hists:
            hist.SetLineColor(hist.GetMarkerColor())
            hist.SetStats(0)
            
    # ----------------------------------------------------------------
    
    def PlotPosteriorsUncCmp(self):
        # get posteriors
        posteriors = []
        nbins = self.h_data_bgSub.GetNbinsX()
        for ibin in range(0, nbins):
            posteriors.append(self.rfile.Get('trace_{}'.format(ibin)))

        self.statUncRatioUnfOverDet = self.h_data_bgSub.Clone(self.h_data_bgSub.GetName() + '_statUncRatioUnfOverDet' )
        self.statUncRatioUnfOverDet.Reset()
        self.statUncRatioUnfOverPtcl = self.h_data_bgSub.Clone(self.h_data_bgSub.GetName() + '_statUncRatioUnfOverPtcl' )
        self.statUncRatioUnfOverPtcl.Reset()

        # get their std dev and compute the relative stat unc.
        # compare to the relative stat. unc of the
        #   i) detector spectrum of ttbar+BSM signal
        #   ii) particle spectrum of ttbar+BSM signal

        for ibin in range(0, len(posteriors)):
            #statUncUnf = posteriors[ibin].GetStdDev()
            
            detVal = self.h_data_bgSub_accApp.GetBinContent(ibin + 1)
            unfVal = self.h_unfolded.GetBinContent(ibin + 1)
            if unfVal > 0. and detVal > 0:
                detUnc = self.h_data_bgSub_accApp.GetBinError(ibin + 1)
                unfUnc = self.h_unfolded.GetBinError(ibin + 1)
                # can compute the ratio of stat. unc.'s
                detUncRel = detUnc / detVal
                unfUncRel = unfUnc / unfVal
                if detUncRel > 0.:
                    self.statUncRatioUnfOverDet.SetBinContent(ibin+1, unfUncRel / detUncRel)
                    
            # and now similar, but after eff correction and between unfolded and particle level:
            ptclVal = self.h_ptcl_effApp.GetBinContent(ibin + 1)
            unfVal_effApp = self.h_unfolded_effCorr.GetBinContent(ibin + 1)
            if unfVal_effApp > 0. and ptclVal > 0:
                ptclUnc = self.h_ptcl_effApp.GetBinError(ibin + 1)
                unfUnc_effApp = self.h_unfolded_effCorr.GetBinError(ibin + 1)
                # can compute the ratio of stat. unc.'s
                ptclUncRel = ptclUnc / ptclVal
                unfUncRel_effApp = unfUnc_effApp / unfVal_effApp
                if ptclUncRel > 0.:
                    self.statUncRatioUnfOverPtcl.SetBinContent(ibin+1, unfUncRel_effApp / ptclUncRel)

                    
        self.statUncRatioUnfOverDet.Scale(1.)
        self.statUncRatioUnfOverPtcl.Scale(1.)

        self.canname = self.origcanname.replace('XYZ', 'UncCmp')
        self.can_uncCmp = ROOT.TCanvas(self.canname, self.canname, 300, 300, 800, 800)
        self.can_uncCmp.cd()

        self.statUncRatioUnfOverDet.SetLineColor(ROOT.kBlue)
        self.statUncRatioUnfOverPtcl.SetLineColor(ROOT.kRed)
        self.statUncRatioUnfOverDet.SetLineWidth(2)
        self.statUncRatioUnfOverPtcl.SetLineWidth(2)
        self.statUncRatioUnfOverDet.SetLineStyle(1)
        self.statUncRatioUnfOverPtcl.SetLineStyle(1)
        self.statUncRatioUnfOverDet.SetFillStyle(0)
        self.statUncRatioUnfOverPtcl.SetFillStyle(0)

        h2name = 'h2UncTmp' + self.topo
        y1 = 0
        y2 = 10.
        self.h2UncTmp = ROOT.TH2D(h2name, h2name + ';' + self.h_unfolded_effCorr.GetXaxis().GetTitle(), 100, self.hxmin, self.hxmax, 100, y1, y2 )
        self.h2UncTmp.SetStats(0)
        self.h2UncTmp.Draw()
        self.statUncRatioUnfOverDet.Draw('hist same')
        self.statUncRatioUnfOverPtcl.Draw('hist same')

        #self.uncleg = ROOT.TLegend(0.65, 0.15, 0.88, 0.35)
        self.uncleg = ROOT.TLegend(0.15, 0.75, 0.50, 0.88)
        self.uncleg.SetBorderSize(0)
        self.uncleg.SetHeader(self.topo)
        self.uncleg.AddEntry(self.statUncRatioUnfOverDet,  '#varepsilon_{unf} / #varepsilon_{det}', 'L')
        self.uncleg.AddEntry(self.statUncRatioUnfOverPtcl, '#varepsilon_{unf} / #varepsilon_{ptcl}', 'L')
        self.uncleg.Draw()

        


        return

    # ----------------------------------------------------------------
    
    def PlotClosure(self):

        idiv = 0

       
        # plot the closure ratio
        self.canname = self.origcanname.replace('XYZ', 'Closure')
        self.can_div, self.ratios, self.lstuff = ReadTools.DrawRatios(self.Hists, self.Labels, idiv, self.Normalize, self.canname, self.xlabel, '', '', 1., 1.)
        for ratio in self.ratios:
            ratio.SetLineColor(ratio.GetMarkerColor())
        ROOT.gPad.Update()
        
        # plot the efficiency
        self.canname = self.origcanname.replace('XYZ', 'eff')
        self.can_eff = ROOT.TCanvas(self.canname, self.canname)
        self.eff.SetMinimum(0.)
        self.eff.SetMaximum(1.05)
        self.eff.SetMarkerColor(self.eff.GetLineColor())
        self.eff.SetMarkerSize(self.msz)
        self.eff.SetMarkerStyle(29)
        self.eff.SetStats(0)
        titx = self.eff.GetXaxis().GetTitle()
        self.eff.GetXaxis().SetTitle(titx.replace('_',' ').replace('ttbar','-t#bar{t} ').replace('det','').replace('Parton',''))
        self.eff.Draw('e1')        
        ROOT.gPad.Update()
        #ReadTools.PrintCan(self.can_eff)
        print('*** Efficiency:')
        ReadTools.PrintBinContent(self.eff)

        # ...?
        # TODO: add here one more closure before the eff correction?
        # ...?


        
        # plot the particle and unfolded spectra as closure
        self.canname = self.origcanname.replace('XYZ', 'SpectraClosure')
        self.can_spect = ROOT.TCanvas(self.canname, self.canname, 700, 400, 900, 800)
        opt = 'e1'
        self.h_ptcl_copy = self.h_ptcl.DrawCopy(opt)
        ROOT.gPad.SetLeftMargin(0.15)
        self.h_ptcl_copy.GetYaxis().SetTitleOffset(2.)
        self.h_ptcl_copy.GetYaxis().SetTitle("events / GeV")

        self.h_ptcl_copy.GetYaxis().SetMoreLogLabels()
        self.h_ptcl_copy.SetLineStyle(1)
        self.h_ptcl_copy.SetLineWidth(1)
        self.h_ptcl_copy.SetLineColor(ROOT.kRed)
        self.h_ptcl_copy.SetMarkerColor(ROOT.kRed)
        self.h_ptcl_copy.SetMarkerStyle(25)
        self.h_ptcl_copy.SetMarkerSize(2)
        self.h_ptcl_copy.SetFillStyle(0)
        self.h_ptcl_copy.SetMaximum(1.5*self.h_ptcl_copy.GetMaximum())

        self.h_ptcl_noSig.SetLineStyle(1)
        self.h_ptcl_noSig.SetLineWidth(1)
        self.h_ptcl_noSig.SetLineColor(ROOT.kMagenta-9)
        self.h_ptcl_noSig.SetFillColor(ROOT.kRed-9)
        #elf.h_ptcl_noSig.SetMarkerColor(ROOT.kRed)
        #elf.h_ptcl_noSig.SetMarkerStyle(27)
        #elf.h_ptcl_noSig.SetMarkerSize(2)
        self.h_ptcl_noSig.SetFillStyle(1111)
        self.h_ptcl_noSig.Draw('hist same')
        
        self.h_unfolded_effCorr_copy = self.h_unfolded_effCorr.DrawCopy(opt + 'same')
        self.h_unfolded_effCorr_copy.SetLineStyle(1)
        self.h_unfolded_effCorr_copy.SetLineWidth(1)
        self.h_unfolded_effCorr_copy.SetLineColor(ROOT.kBlack)
        self.h_unfolded_effCorr_copy.SetMarkerColor(ROOT.kBlack)
        self.h_unfolded_effCorr_copy.SetMarkerStyle(8)
        self.h_unfolded_effCorr_copy.SetMarkerSize(2)
        self.h_unfolded_effCorr_copy.SetFillStyle(0)

        self.h_data_bgSub_acceffCorr.SetMarkerSize(2)
        self.h_data_bgSub_acceffCorr.SetMarkerStyle(32)
        self.h_data_bgSub_acceffCorr.SetMarkerColor(ROOT.kBlue)
        self.h_data_bgSub_acceffCorr.SetLineStyle(1)
        self.h_data_bgSub_acceffCorr.SetLineWidth(1)
        self.h_data_bgSub_acceffCorr.SetLineColor(ROOT.kBlue)
        self.h_data_bgSub_acceffCorr.Draw(opt + 'same')

        # LEG
        self.leg_spect = ROOT.TLegend(0.55, 0.75, 0.88, 0.88)
        leg = self.leg_spect
        leg.AddEntry(self.h_data_bgSub_acceffCorr, '1/eff*acc*(data-Bg)', 'PL')
        leg.AddEntry(self.h_ptcl_copy, '{}'.format(self.truthlevel), 'PL')
        leg.AddEntry(self.h_unfolded_effCorr_copy, 'Unfolded', 'PL')
        leg.AddEntry(self.h_ptcl_noSig, '{}, no signal'.format(self.truthlevel), 'F')
        leg.SetBorderSize(0)
        leg.Draw()
        #self.spect_stuff = []
        #print('*** Closure integrals: {}, {}'.format(self.h_ptcl_copy.Integral(), self.h_unfolded_effCorr_copy.Integral()))
        ROOT.gPad.Update()
        ROOT.gPad.RedrawAxis()
        ReadTools.PrintCan(self.can_spect, '', '_liny')
        ROOT.gPad.SetLogy(1)
        ROOT.gPad.Update()
        ROOT.gPad.RedrawAxis()
        ReadTools.PrintCan(self.can_spect, '', '_logy')
        
        
        # closure w.r.t. the full particle level distribution = ttbar + Sig, i.e. including the BSM bump;
        self.FullClosureHists = [self.h_ptcl, self.h_unfolded_effCorr] #,  h_data]
        self.FullClosureLabels = [self.truthlevel, 'Unfolded/eff', 'Detector level']
        idiv = 0
        self.canname = self.origcanname.replace('XYZ', 'ClosureInclEff')
        self.can_div_eff, self.ratios_eff, self.llstuff = ReadTools.DrawRatios(self.FullClosureHists, self.FullClosureLabels, idiv, self.Normalize, self.canname, self.xlabel, '')
        for ratio in self.ratios_eff:
            ratio.SetFillStyle(0)
            #ratio.SetMarkerColor(self.h_unfolded_effCorr.GetMarkerColor())
            #ratio.SetLineColor(self.h_unfolded_effCorr.GetLineColor())
            ratio.SetLineStyle(1)
            ratio.SetLineWidth(1)
            ratio.SetMarkerStyle(20)
            ratio.SetMarkerSize(self.msz)
            ratio.Draw('e1 same')
        ROOT.gPad.Update()
        #ReadTools.PrintCan(self.can_div_eff)

        # ratio to ttbar only, to see the BSM bump after unfolding
        self.FullBumpHists = [self.h_ptcl_noSig, self.h_unfolded_effCorr] #,  h_data]
        self.FullBumpLabels = [self.truthlevel + ' t#bar{t}', 'Unfolded/eff', 'Detector level']
        idiv = 0
        self.canname = self.origcanname.replace('XYZ', 'UnfBump')
        self.can_div_bump, self.ratios_bump, self.llstuff = ReadTools.DrawRatios(self.FullBumpHists, self.FullBumpLabels, idiv, self.Normalize, self.canname, self.xlabel, '')
        for ratio in self.ratios_bump:
            ratio.SetFillStyle(0)
            ratio.SetMarkerColor(self.h_unfolded_effCorr.GetMarkerColor())
            ratio.SetLineColor(self.h_unfolded_effCorr.GetLineColor())
            ratio.SetLineStyle(1)
            ratio.SetLineWidth(1)
            ratio.SetMarkerStyle(20)
            ratio.SetMarkerSize(self.msz)
            ratio.Draw('e1 same')
        ReadTools.PrintCan(self.can_div_bump)
        
        # now draw the significance
        # h_unity = MakeOneWithoutErrors(self.h_data_bgSub_accApp)
        # copy the unfolded error bars to the unity which is then as a 'background; subtracted
        # and its errors are used to compute the sinif.:
        # WE SHOULD NOT PUT ON THE ERRORS OF UNFOLED_EFFCORR, AS THESE UNC. ARE ALEADY PART OF THE RATIOS_BUMP[0]!
        ### THEREFORE NOT:
        ### h_unity = MakeOneWithErrors(self.h_unfolded_effCorr)
        # BUT:
        h_unity = MakeOneWithoutErrors(self.h_unfolded_effCorr)
        stuff = []
        yMin = -1.
        yMax = 42.
        iplot = 0
        
        self.canname = self.origcanname.replace('XYZ', 'Significance')
        self.can_signif = ROOT.TCanvas(self.canname, self.canname, 400, 400, 800, 800)
        # see Tools' MakeMultiSubPads(can, ratios, PadSeparation = 0.0, UpperPadTopMargin = 0.07, LowestPadBottomMargin = 0.40)
        rspads,rspad_inset = MakeMultiSubPads(self.can_signif, [0.70, 0.28], 0.0)

        rspads[0].cd()
        
        self.signifh_unf, self.ratioScaleHisto = DrawSignificance(h_unity, self.ratios_bump[0], self.hxmin, self.hxmax, yMin, yMax, stuff, iplot, 'Signal signif.', False, 'e1 hist same', True)
        stuff.append(self.signifh_unf)
        stuff.append(self.ratioScaleHisto)

        
        # compute the detector-level significance:
        # note: this excludes any physics bg unc., only the ttbar and BSM signal uncertainties!
        # this is b/c bgSub here actually means ttbar+BSM signal
        self.signifh_det, ratioScaleHisto_det = DrawSignificance(self.h_det_ttbar, self.h_data_bgSub, self.hxmin, self.hxmax, yMin, yMax, stuff, iplot+1, 'Signal signif.', False, 'e1 hist same')
        stuff.append(self.signifh_det)
        #stuff.append(ratioScaleHisto_det)

        # 4.7.2022, Higgs @ 10y!;)
        # TODO IDEA: compute the significance as in stack plots: "bg" incl. ttbar and total data?
        # 1.8.2022 not sure I want this after all...

        self.signifh_unf.SetLineColor(ROOT.kMagenta)
        self.signifh_det.SetLineColor(ROOT.kBlack)
        #self.signifh_unf.SetFillColor(ROOT.kMagenta, 0.3)
        #self.signifh_det.SetFillColor(ROOT.kBlack, 0.3)
        self.signifh_unf.SetFillColorAlpha(ROOT.kMagenta, 0.3)
        self.signifh_det.SetFillColorAlpha(ROOT.kBlack, 0.2)
        #self.signifh_unf.SetFillStyle(3445)
        #self.signifh_det.SetFillStyle(3554)
        self.signifh_unf.SetFillStyle(1111)
        self.signifh_det.SetFillStyle(1111)
        self.signifh_unf.SetLineWidth(2)
        self.signifh_det.SetLineWidth(2)
        self.signifh_unf.SetLineStyle(1)
        self.signifh_det.SetLineStyle(1)
        self.signifh_unf.Draw('hist same')
        self.signifh_det.Draw('hist same')

        self.sleg = ROOT.TLegend(0.55, 0.65, 0.88, 0.92)
        self.sleg.SetBorderSize(0)
        self.sleg.SetHeader(self.topo)
        self.sleg.AddEntry(self.signifh_det, 'Det. level signal signif.', 'F')
        self.sleg.AddEntry(self.signifh_unf, 'Unf. level signal signif.', 'F')
        self.sleg.Draw()
        
        # plot also the ratio of significances
        # remove the yellow band
        rspads[1].cd()

        gyratioMin, gyratioMax = -1., 2.2
        ratio,band,hratio = DrawNiceRatioWithBand(self.signifh_det, self.signifh_unf, self.hxmin, self.hxmax, gyratioMin, gyratioMax, stuff, 0, 'unf/det signif.', False)
        ratio.SetFillStyle(0)
        print('Signifs and their ratio bin contents:')
        ReadTools.PrintBinContent(self.signifh_unf)
        ReadTools.PrintBinContent(self.signifh_det)
        ReadTools.PrintBinContent(ratio)
        ratio.SetLineColor(self.signifh_unf.GetLineColor())
        ratio.SetLineWidth(2)
        ratio.SetLineStyle(1)
        ratio.Draw('hist same')

        stuff.append([ratio, band, hratio, self.sleg])
        
        self.can_signif.Update()
        
        self.stuff = stuff
        
        
    # ---------------------------------------------------------------------

    def PrintCanvases(self):
        ReadTools.PrintCan(self.can)
        ReadTools.PrintCan(self.can_div)
        ReadTools.PrintCan(self.can_div_eff)
        ReadTools.PrintCan(self.can_signif)
        ReadTools.PrintCan(self.can_uncCmp)

        
#######################################################################
#######################################################################
#######################################################################


def DrawUnfolded(unfToDraw):

    localstuff = []
    ROOT.gStyle.SetOptTitle(0)

    unfToDraw.ReadInputs()

    # compare posteriors stat. unc.
    unfToDraw.PlotPosteriorsUncCmp()
    
    # plot ingredients
    unfToDraw.PlotIngredients()

    # plot closure
    # and also a possible bump over ttbar and its significance
    unfToDraw.PlotClosure()

    # print png/pdf
    unfToDraw.PrintCanvases()
    
    #ROOT.gApplication.Run()

    return
