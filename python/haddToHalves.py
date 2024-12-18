#!/usr/bin/python3
# jk III/2020

import os, sys

### STEERING!!!
isDryRun = False
systtag = '_smearedJets_jesSlopeP1p0'


if isDryRun:
    print("OK, just a dry run, should not be doing anything...")
else:
    print("NOT A DRY RUN? ARE YOU SURE? Y/n")
    haha = input()
    if haha != 'Y':
        exit(1)
    
runsdir = 'runs/'
#cmd = 'mkdir -p {} ; mv *run_*.root {}'.format(runsdir, runsdir)
cmd = 'mkdir -p {}'.format(runsdir)
print(cmd)
os.system(cmd)

argv = sys.argv
reqtag = ''
if len(argv) > 1:
    reqtag = argv[1]
    print('OK, will merge samples containing {:}'.format(reqtag))


tags = [  #'2tj_allhad_NLO_ATLAS', # also 14 TeV, do not worry;-) actually same as next sample:)
          #'2tj_allhad_NLO_ptheavy50GeV_14TeV_ATLAS', # not really pT heavy...
          #'2t_allhad_14TeV_LO_ATLAS',
          #'pp_2tj_allhad_NLO_ptj1min60_ptj2min60_14TeV_ATLAS',
          #'pp_2tj_allhad_NLO_ptj1min100_ptj2min100_14TeV_ATLAS',
          #'pp_2tj_allhad_NLO_ptj1min200_ptj2min200_14TeV_ATLAS',
          ###!!!'pp2y02tt_y0_1000GeV_NLO_14TeV_ATLAS', # width 10 GeV
          #'pp2y02tt_y0_1000GeV_width100GeV_NLO_14TeV_ATLAS',
          #'pp2y02tt_y0_1000GeV_width300GeV_NLO_14TeV_ATLAS',
	  #'pp2Wbb_pTj1min50GeV_allhad_14TeV_ATLAS',
	  #'pp2Wj_pTj1min50GeV_allhad_14TeV_ATLAS',
    ###'pp2xdxdtt_y0_1000GeV_xd_10GeV_allhad_14TeV_ATLAS',
    ###!!!'pp2xdxdtt_y0_1000GeV_xd_100GeV_allhad_14TeV_ATLAS',
    ###'pp2xdxdtt_y0_1000GeV_xd_300GeV_allhad_14TeV_ATLAS',

    ###'zp_ttbarj_allhad_1500GeV_14TeV_ATLAS',
          #'zp_ttbarj_allhad_1250GeV_14TeV_ATLAS',
    #'zp_ttbarj_allhad_1000GeV_14TeV_ATLAS',
    ###!!!'zp_ttbarj_allhad_1000GeV_NEW_14TeV_ATLAS',
    ### HACK:
    ###!!!'zp_ttbarj_allhad_1000GeV_14TeV_ATLAS',
    ###'zp_ttbarj_allhad_1250GeV_NEW_14TeV_ATLAS',
       ###   'zp_ttbarj_allhad_900GeV_14TeV_ATLAS',
       ###   'zp_ttbarj_allhad_800GeV_14TeV_ATLAS',
       ###   'zp_ttbarj_allhad_750GeV_14TeV_ATLAS',
    #'zp_ttbarj_allhad_700GeV_14TeV_ATLAS',
    
          #'pp2jjjMatched_pTj1j2min_60GeV_14TeV_ATLAS',
          #'pp2jjjjMatched_pTj1j2min_60GeV_14TeV_ATLAS',
          #'pp2jjjj_pTj1min400GeV_pTj2min60GeV_14TeV_ATLAS',
    ###!!!'pp2wbbjjMatched_allhad_pTj1j2min_60GeV_14TeV_ATLAS',

    ###!!!'pp_2tj_allhad_NLO_ptj1j2min60_ptj1j2max200_14TeV_ATLAS',
    ###!!!'pp_2tj_allhad_NLO_ptj1j2min200_14TeV_ATLAS',
    ###!!!'pp_2tj_allhad_NLO_ptj1min200_ptj2min60max200_14TeV_ATLAS',

    'pp_2tj_allhad_NLO_ptj1j2min60_ptj1j2max200_14TeV_ATLAS_weighted',
    'pp_2tj_allhad_NLO_ptj1j2min200_14TeV_ATLAS_weighted',
    'pp_2tj_allhad_NLO_ptj1min200_ptj2min60max200_14TeV_ATLAS_weighted',

    ###'zp_ttbar_allhad_1000GeV_14TeV_ATLAS',

    ###!!!'pp2wwbb_allhad_pTj1j2min_60GeV_14TeV_ATLAS',

        # 30.6.2021:
    ###'pp_4j_ptj1j2min60_ptj1j2max200_14TeV_ATLAS',
    ###'pp_4j_ptj1j2min200_14TeV_ATLAS',
    ###'pp_4j_ptj1min200_ptj2min60max200_14TeV_ATLAS',

    # 1.7.2021:
    ###!!!
    #'pp_2b2j_LO_matched_ptj1j2min60_ptj1j2max200_14TeV_ATLAS',
    ###!!!
    #'pp_2b2j_LO_matched_ptj1j2min200_14TeV_ATLAS',
    ###!!!
    #'pp_2b2j_LO_matched_ptj1min200_ptj2min60max200_14TeV_ATLAS',

    ###    'pp_2b2j_LO_matched_ptj1j2min60_ptj1j2max200_14TeV_ATLAS_weighted',
    ###    'pp_2b2j_LO_matched_ptj1j2min200_14TeV_ATLAS_weighted',
    ###    'pp_2b2j_LO_matched_ptj1min200_ptj2min60max200_14TeV_ATLAS_weighted',



          ]

for tag in tags:
    # HACK!!!
    #if tag != 'zp_ttbarj_allhad_1000GeV_14TeV_ATLAS' and  tag != 'zp_ttbarj_allhad_1250GeV_14TeV_ATLAS' and tag != 'pp_2tj_allhad_NLO_ptj1min60_ptj2min60_14TeV_ATLAS':
    #if tag != 'pp_2tj_allhad_NLO_ptj1min60_ptj2min60_14TeV_ATLAS':
    #if tag != 'zp_ttbarj_allhad_1000GeV_NEW_14TeV_ATLAS':
    #    #'pp2wbbjjMatched_allhad_pTj1j2min_60GeV_14TeV_ATLAS':
    #if tag != 'pp_2tj_allhad_NLO_ptj1min100_ptj2min100_14TeV_ATLAS':
    #if not 'pp_2tj_allhad_NLO_ptj1min200' in tag:
    #    continue
    #if not 'xd_100' in tag:
    #    continue
    #if not '2tj' in tag:
    #    continue
    #if not 'ptj1min200_ptj2min60max200' in tag:
    #    continue


    if reqtag != '' and not reqtag in tag:
        continue
        
    print('***processing {}'.format(tag))

    cmd = 'mv analyzed_histos_run_*{}*{}*.root {}/'.format(tag, systtag, runsdir)
    print(cmd)
    if not isDryRun:
        os.system(cmd)

    files = []
    #addGrepCmd = ''
    #if 'xdxd' in tag:
    #    # early xdxd samples have bugged particle jets as xd were included in the ptcl jets clustering
    #    addGrepCmd = ' | egrep "run_3|run_4" | egrep -v "run_30|run_31"'
    addGrepCmd = ''
    if not 'weighted' in tag:
        addGrepCmd = ' | grep -v weighted'
    for line in os.popen('cd {} ; ls *{}*{}*.root | grep run_ {}'.format(runsdir, tag, systtag, addGrepCmd)).readlines():
        #print(line)
        files.append(line[:-1])
        #print(files)
    print('Files: {}'.format(len(files)))


    flists = [ [], [] ]
    iif = 0
    ihalf = 0
    for fname in files:
        if iif == int(len(files)/2.):
            ihalf += 1
        flists[ihalf].append(fname)
        iif += 1
    print(flists)
    if len(flists[0]) != len(flists[1]):
        print('ERROR, GOT NON EQUAL NUMBER OF FILES IN HALF0 AND HALF1 SAMPLES! {} vs {}'.format(len(flists[0]), len(flists[1])))
    
    ihalf=0
    for flist in flists:
        fline = ''
        for item in flist:
            print(item)
            fline += ' {}{}'.format(runsdir,item)
        cmd = 'hadd -f analyzed_histos_{}{}_half{}.root {}'.format(tag, systtag, ihalf, fline)
        print(cmd)
        if not isDryRun:
            ###!!!
            os.system(cmd)
        ihalf += 1
    cmd = 'hadd -f analyzed_histos_{}{}_all.root analyzed_histos_{}{}_half0.root analyzed_histos_{}{}_half1.root'.format(tag, systtag, tag, systtag, tag, systtag)
    if not isDryRun:
        os.system(cmd)

# SPECIAL: 29.10.2020
# hadd the full weighted ttbar sample!
if reqtag == '' or '2tj' in reqtag or 'weigh' in reqtag:
    if not isDryRun:
        os.system('hadd -f analyzed_histos_pp_2tj_allhad_NLO_ALL_14TeV_ATLAS_weighted_all.root analyzed_histos_pp_2tj_allhad_NLO_ptj1j2min60_ptj1j2max200_14TeV_ATLAS_weighted_all.root analyzed_histos_pp_2tj_allhad_NLO_ptj1j2min200_14TeV_ATLAS_weighted_all.root analyzed_histos_pp_2tj_allhad_NLO_ptj1min200_ptj2min60max200_14TeV_ATLAS_weighted_all.root')
    if not isDryRun:
        os.system('hadd -f analyzed_histos_pp_2tj_allhad_NLO_ALL_14TeV_ATLAS_unweighted_all.root analyzed_histos_pp_2tj_allhad_NLO_ptj1j2min60_ptj1j2max200_14TeV_ATLAS_all.root analyzed_histos_pp_2tj_allhad_NLO_ptj1j2min200_14TeV_ATLAS_all.root analyzed_histos_pp_2tj_allhad_NLO_ptj1min200_ptj2min60max200_14TeV_ATLAS_all.root')

# SPECIAL: 13.7.2021
# hadd the full weighted 2b2j sample!
if reqtag == '' or '2b2j' in reqtag or 'weigh' in reqtag:
    if not isDryRun:
        os.system('hadd -f analyzed_histos_pp_2b2j_LO_matched_ALL_14TeV_ATLAS_weighted_all.root analyzed_histos_pp_2b2j_LO_matched_ptj1min200_ptj2min60max200_14TeV_ATLAS_weighted_all.root analyzed_histos_pp_2b2j_LO_matched_ptj1j2min200_14TeV_ATLAS_weighted_all.root analyzed_histos_pp_2b2j_LO_matched_ptj1min200_ptj2min60max200_14TeV_ATLAS_weighted_all.root')
    if not isDryRun:
        os.system('hadd -f analyzed_histos_pp_2b2j_LO_matched_ALL_14TeV_ATLAS_unweighted_all.root analyzed_histos_pp_2b2j_LO_matched_ptj1min200_ptj2min60max200_14TeV_ATLAS_all.root analyzed_histos_pp_2b2j_LO_matched_ptj1j2min200_14TeV_ATLAS_all.root analyzed_histos_pp_2b2j_LO_matched_ptj1min200_ptj2min60max200_14TeV_ATLAS_all.root')

print('DONE!')

# remove NEW from file names:
print('Calling ./scripts/renameNEW.sh')
if not isDryRun:
    os.system('./scripts/renameNEW.sh')

