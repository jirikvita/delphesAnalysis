#!/usr/bin/python3

# jk 25.2.2018, 7.3.2018, 3.4.2018, 11.6.2019, 12.4.2022
# jk 21.6.2022

from Unfold import *

from cUnfSuffixes import *

varname = 'DiTopMass'

topos = ['2B0S',
         '1B1S',
         '0B2S'
]

unfObjs = [ ]
for topo in topos:
    unfObjs.append(    cUnfObjs('toUnfold/stackedToUnfold_y0_1000GeV_' + topo + '_Detector' + varname + '_tot.root',
                                'toUnfold/stackedToUnfold_y0_1000GeV_' + topo + '_Particle' + varname + '_tot.root',
                                'toUnfold/corrsForUnf_ttbar.root',
                                'Detector' + varname + '_ttbarPlusSig',
                                'matrix_' + topo + '_' + varname + '_Particle_Detector',
                                'Particle' + varname + '_ttbarPlusSig', # for closure when unfolding bg+tt+signal - bg
                                'Particle' + varname + '_ttbar', # for bump hunt
    )
                       )

dirname = ''

for unfObj in unfObjs:
    print('Unfolding projections of %s from file %s' % (unfObj.dataRootFileName, unfObj.migraname,))
    Unfold(unfObj)

