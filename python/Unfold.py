#!/usr/bin/python3

# jk 25.2.2018, 7.3.2018, 3.4.2018, 11.6.2019, 12.4.2022
# reworked to a class VI-VII/2022

import ReadTools
import ROOT

# following:
# http://nbviewer.jupyter.org/github/gerbaudo/fbu/blob/v0.0.2/tutorial.ipynb
# modified by jk 30.11.2017, 1.2.2018, 26.2.2018, 28.2.2018, 15.4.2022

import fbu
myfbu = fbu.PyFBU()
ReadTools.stuff.append(myfbu)

#######################################################################
#######################################################################
#######################################################################

# some nasty globals:)
#from matplotlib import pyplot as plt
PlotByPyPlot = False

# increase defaults:
# Petr:
#myfbu.nMCMC = 300000 # 100000
# jk:
#myfbu.nMCMC = 200000
###myfbu.nMCMC = 100000
myfbu.nMCMC = 50000
#myfbu.nwalkers = 1000
#myfbu.nBurn = 100000
#myfbu.nThin = 20
#myfbu.verbose = False
myfbu.verbose = True

# The Regularization class allows to impose an additional prior on the unfolded parameters
from fbu import Regularization
#myfbu.regularization = Regularization('Tikhonov',parameters=[{'refcurv':0.,'alpha':0.01}])
#myfbu.regularization = Regularization('Tikhonov',parameters=[{'refcurv':0.,'alpha':0.1},{'refcurv':0.2,'alpha':0.1}])

# Supply the input distribution to be unfolded as a 1-dimensional list for N bins, with each entry corresponding to the bin content.


#######################################################################
#######################################################################
#######################################################################

class cUnfObjs:
    def __init__(self,
                 dataRootFileName,
                 ptclRootFileName,
                 corrsFileName,
                 hname,
                 migraname,
                 ptclhname,
                 ptclhname_noSig):
        self.hname = hname
        self.ptclhname = ptclhname
        self.ptclhname_noSig = ptclhname_noSig
        self.dataRootFileName = dataRootFileName
        self.ptclRootFileName = ptclRootFileName
        self.migraname = migraname
        self.corrsFilename = corrsFileName
        
        self.topo = migraname.split('_')[1]
        self.varname = migraname.split('_')[2]
        self.nrebin = -1

        self.outtag = dataRootFileName.split('/')[-1].replace('.root', '')
        self.outFileName = 'unfolded_{}_{}.root'.format( self.topo, self.hname, self.outtag)

        self.ReadHistos()
        
    def ReadHistos(self):

        print('Opening ROOT file {}'.format(self.dataRootFileName))
        self.rfile_pseudodata = ROOT.TFile(self.dataRootFileName, 'read')
        print('Opening ROOT file {}'.format(self.ptclRootFileName))
        self.rfile_ptcl = ROOT.TFile(self.ptclRootFileName, 'read')

        # take the detector level and the truth level for closure from the data-like MC file:
        print('Getting data and particle histograms...')
        self.h_data = self.rfile_pseudodata.Get(self.hname)
        self.h_ptcl = self.rfile_ptcl.Get(self.ptclhname)
        # this one is typically just ttbar, w/o new physics
        self.h_ptcl_noSig = self.rfile_ptcl.Get(self.ptclhname_noSig)

        self.h_det_ttbar = self.rfile_pseudodata.Get('Detector{}_ttbar'.format(self.varname))
        
        print('Getting eff and acc...')
        self.corrsFile = ROOT.TFile(self.corrsFilename, 'read')
        self.acc = self.corrsFile.Get('acc_{}_{}'.format(self.topo, self.varname))
        self.eff = self.corrsFile.Get('eff_{}_{}'.format(self.topo, self.varname))

        print('Getting response matrix {}'.format(self.corrsFilename))
        self.h_response_mc = self.corrsFile.Get(self.migraname)
        print('Making migratin matrix')
        self.h_migra = ReadTools.NormalizeResponse(self.h_response_mc)

        # Obsolete:
        # rebin
        #if self.nrebin > 1:
        #    h_response_pseudodata.Rebin2D(self.nrebin,self.nrebin)
        #    h_response_mc.Rebin2D(nrebin,self.nrebin)

    def PrintInfo(self):
        print('Number of bins: data {}, ptcl {}, migra {}x{}'.format(self.h_data.GetXaxis().GetNbins(),
                                                                     self.h_ptcl.GetXaxis().GetNbins(),
                                                                     self.h_migra.GetXaxis().GetNbins(),
                                                                     self.h_migra.GetYaxis().GetNbins()))        
        print (self.h_data)
        print ('h_ptcl:')
        print (self.h_ptcl)
        print ('Migra:')
        print (self.h_migra)
        print('*** data I={}'.format(self.h_data.Integral()))
        ReadTools.PrintBinContent(self.h_data)
        print('*** ptcl I={}'.format(self.h_ptcl.Integral()))
        ReadTools.PrintBinContent(self.h_ptcl)

    def ApplyAccToData(self):
        # apply the acceptance
        print('Applying the acc factor to the detector level...')
        self.h_data_accApp = self.h_data.Clone(self.h_data.GetName() + '_accApp')
        self.h_data_accApp.Multiply(self.acc)
        
    def ApplyEffToPtcl(self):
        # Aply eff factor to h_ptcl to be able to compare to eff-non-corrected unfolded
        self.h_ptcl_effApp = self.h_ptcl.Clone(self.h_ptcl.GetName() + '_effApp')
        self.h_ptcl_effApp.Multiply(self.eff)
        self.h_ptcl_noSig_effApp = self.h_ptcl_noSig.Clone(self.h_ptcl_noSig.GetName() + '_effApp')
        self.h_ptcl_noSig_effApp.Multiply(self.eff)

    def CorrectUnfoldedForEff(self):
        # apply the efficiency correction as 1/eff
        print('Applying the 1/eff factor to the unfolded result...')
        self.h_unfolded_effCorr = self.h_unfolded.Clone(self.h_unfolded.GetName() + '_effCorr')
        self.h_unfolded_effCorr.Divide(self.eff)

    def OpenOutFile(self):
        self.outfile = ROOT.TFile(self.outFileName, "recreate")
        self.outfile.cd()

    def MakePosteriorsDiagonal(self, trace):
        self.posteriors_diag = ReadTools.MakeTH1Ds(trace)
        print ('Length of the diag: {:}'.format(len(self.posteriors_diag)) )

    def PlotPosteriors(self):
        ftag = ''
        canp = ReadTools.PlotPosteriors(self.posteriors_diag, self.h_ptcl_effApp, 'PosteriorsDiag_' + self.migraname + ftag)

    def MakeUnfoldedHisto(self):
        self.h_unfolded = ReadTools.MakeUnfoldedHisto(self.h_data, self.posteriors_diag)

    def Write(self):
        self.h_data.Write()
        self.h_data_accApp.Write()

        self.h_ptcl.Write()
        self.h_ptcl_effApp.Write()

        self.h_ptcl_noSig.Write()
        self.h_ptcl_noSig_effApp.Write()

        # save also detector-level ttbar distr., to compute BSM signif. above ttbar 
        self.h_det_ttbar.Write()
        
        self.h_response_mc.Write()
        self.h_migra.Write()

        self.h_unfolded.Write()
        self.h_unfolded_effCorr.Write()

        self.eff.Write()
        self.acc.Write()
        
        # TODO:
        # read and write also the ttbar only and signal only! (for closure and signal significance)
        
        self.outfile.Write()




#######################################################################
#######################################################################
#######################################################################

def Unfold(unfObjs):

    ROOT.gStyle.SetOptTitle(0)
    
    unfObjs.PrintInfo()

    unfObjs.ApplyAccToData()
    
    myfbu.data = ReadTools.MakeListFromHisto(unfObjs.h_data_accApp)
    print ('FBU data:')
    print (myfbu.data)
 
    myfbu.response = ReadTools.MakeListResponse(unfObjs.h_migra)
    print (myfbu.response)

    # Define the boundaries of the hyperbox to be sampled for each bin.

    myfbu.lower = []
    myfbu.upper = []
    # sf to restrict the range of truth to be sampled around reco
    nbins = unfObjs.h_data_accApp.GetXaxis().GetNbins()
    for i in range(1, nbins+1):
        rval = unfObjs.h_data_accApp.GetBinContent(i)
        tval = unfObjs.h_ptcl.GetBinContent(i)
        print('*** bin {} reco: {} truth: {}'.format(i, rval, tval))
        myfbu.lower.append(0.)
        myfbu.upper.append(rval * 5.)
        print('  limits in bin {} set to: {:.0f} -- {:.0f}'.format(i, myfbu.lower[-1], myfbu.upper[-1]))
    
    print('The limits are:')
    i = 1
    for low,up in zip(myfbu.lower, myfbu.upper):
        val = unfObjs.h_ptcl.GetBinContent(i)
        i = i + 1
        print('{:.0f} -- {:.0f}   truth: {:.0f}. Contained? {}'.format(low, up, val, val > low and val < up))

    ###############################################################################
    # Run the MCMC sampling                                                       #
    # (this step might take up to several minutes for a large number of bins).    #
    ###############################################################################
    myfbu.run()
    ###############################################################################
    # Retrieve the N-dimensional posterior distribution in the form of a list of N arrays.
    trace = myfbu.trace
    print (trace)
    print ('Length of the trace: {:}'.format(len(trace)) )

    unfObjs.OpenOutFile()
    unfObjs.MakePosteriorsDiagonal(trace)
    unfObjs.ApplyEffToPtcl()
    unfObjs.PlotPosteriors()
    unfObjs.MakeUnfoldedHisto()
    unfObjs.CorrectUnfoldedForEff()
    
    #if PlotByPyPlot:
    #    for ibin in range(0,h_data.GetNbinsX()):
    #        plt.hist(trace[ibin],
    #                 bins=20,alpha=0.85,
    #                 normed=True)
    #        plt.ylabel('probability')
    #        plt.show()
    # more on plotting:
    # https://matplotlib.org/users/pyplot_tutorial.html

    unfObjs.Write()

    #ROOT.gApplication.Run()

    return
