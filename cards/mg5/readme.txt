

###################################
Higgs -> l nu b l nu b:
p p > h  > l+ vl b l- vl~ b~ 

###################################
4tops allhad
generate p p > t t t~ t~, t > b j j, t~ > b~ j j
output 4t_allhad_14TeV

###################################
Zprime -> ttbar -> allhad
LO:
import model Abelian_Higgs_Model_UFO
generate p p > zp > t t~, t > j j b, t~ > j j b~
output pp_zp_ttbar_allhad_1000GeV_14TeV

NLO: (allow Zp+j)
import model Abelian_Higgs_Model_UFO
generate p p > zp > t t~, t > j j b, t~ > j j b~ @0
add process p p > zp > t t~ j, t > j j b, t~ > j j b~ @1
output pp_zp_ttbarj_allhad_1000GeV_14TeV

or also ljets:
generate p p > zp > t t~, t > l+ vl b, t~ > j j b~ @0
add process p p > zp > t t~ j, t > l+ vl b, t~ > j j b~ @1
add process p p > zp > t t~, t > j j b, t~ > l- vl~ b~ @0
add process p p > zp > t t~ j, t > j j b, t~ > l- vl~ b~ @1
output pp_zp_ttbarj_ljets_1000GeV_14TeV

###################################
W+ + Jet:
generate p p > W+, W+ > j j @0
addprocess p p > W+ j, W+ > j j @1
!! zapnout si ckkw matching na 1 !!


###################################
ttbar:

alljets:
generate p p > t t~, t > j j b, t~ > j j b~ @0
add process p p > t t~ j, t > j j b, t~ > j j b~ @1

output pp_2tj_allhad_NLO
output pp_2tj_allhad_NLO_ptj1j2min60_ptj1j2max200
output pp_2tj_allhad_NLO_ptj1j2min200
output pp_2tj_allhad_NLO_ptj1min200_ptj2min60max200


just pp->tt:
generate p p > t t~, t > j j b, t~ > j j b~
output pp2ttbar_allhad_LO

try also?
generate p p > t t~, t > j j b, t~ > j j b~ @0
output pp2ttbar_allhad_LO_0


ljets: NLO in tt, LO in ttj:
dohromady:
generate p p > t t~, t > l+ vl b, t~ > j j b~ @0
add process p p > t t~ j, t > l+ vl b, t~ > j j b~ @1
add process p p > t t~, t > j j b, t~ > l- vl~ b~ @0
add process p p > t t~ j, t > j j b, t~ > l- vl~ b~ @1
output pp2ttbarj_ljets_both_NLO

LO in ttbar:
dohromady:
generate p p > t t~, t > l+ vl b, t~ > j j b~ @0
add process p p > t t~, t > j j b, t~ > l- vl~ b~ @0
output pp2ttbar_ljets_both_LO


popr. separatne:
1)
generate p p > t t~, t > j j b, t~ > l- vl~ b~ @0
add process p p > t t~ j, t > j j b, t~ > l- vl~ b~ @1
output pp2ttbarj_ljets_LO
2)
generate p p > t t~, t > l+ vl b, t~ > j j b~ @0
add process p p > t t~ j, t > l+ vl b, t~ > j j b~ @1
output pp2ttbarj_ljets2_LO


###################################
ttbar allhad, special initial parton combinations:
jk 24.5.2021

# gg -- OK, 421 pb
generate g g > t t~, t > j j b, t~ > j j b~ @0
add process g g > t t~ j, t > j j b, t~ > j j b~ @1
output gg2ttbarj_allhad_NLO

# qq -- OK, 38 pb
define q = u c d s u~ c~ d~ s~
generate q q > t t~, t > j j b, t~ > j j b~ @0
add process q q > t t~ j, t > j j b, t~ > j j b~ @1
output qq2ttbarj_allhad_NLO

# qg -- OK, 69 pb
generate q g > t t~ j, t > j j b, t~ > j j b~ @0
add process q g > t t~ j, t > j j b, t~ > j j b~ @1
output qg2ttbarj_allhad_NLO



###################################
SINGLE TOP BACKGROUND - PETR BARON

T channel top:

generate p p > t j b~, t > b l+ vl
add process p p > t j, t > b l+ vl

T channel anti-top

generate p p > t~ j b, t~ > b~ l- vl~
add process p p > t~ j, t~ > b~ l- vl~

S channel top: 

generate p p > t b~, t > b l+ vl

S channel anti-top: 

generate p p > t~ b, t~ > b~ l- vl~     

Wt channel top:

generate p p > t w-, w- > j j, t > b l+ vl 
add process p p > t w-, w- > l- vl~, t > b j j

Wt channel anti-top:

generate p p > t~ w+, w+ > j j, t~ > b~ l- vl~ 
add process p p > t~ w+, w+ > l+ vl, t~ > b~ j j

###################################
# DM xd model with a portal y0

https://arxiv.org/abs/1607.06680
 => "Monojet, tt¯ + E/ T and SM Higgs boson events are
generated with MadGraph5 aMC@NLO [41] using the SMM UFO model [42] for the SMM case and the DMSIMP UFO model [43] for the LHC DMF and SM Higgs boson cases"
[43] => https://arxiv.org/pdf/108.05327.pdf
"Our simplified DM model files are publicly available at the FeynRules repository [28]"
http://feynrules.irmp.ucl.ac.be/wiki/DMsimp

import model DMsimp_s_spin0
generate p p > xd xd~ t t~ / a z w+ w- [QCD]

with decay, can't use NLO QCD:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/MadgraphTutorial
=>

ljets ttbar final state::
generate    p p > xd xd~ t t~ / a z w+ w-, t > l+ vl b, t~ > j j b~
add process p p > xd xd~ t t~ / a z w+ w-, t > j j b, t~ > l- vl~ b~  
output pp2ttchichi_LO_ljets_14TeV

allhad final state:
generate    p p > xd xd~ t t~ / a z w+ w-, t > j j b, t~ > j j b~
output pp2ttchichi_LO_allhad_14TeV

NEW: scalar y0->tt, via triangle loop, cannot specify decay mode of tt, but works!;)
cca 20.3.2020
p p > y0 > t t~
see JIRA
https://its.cern.ch/jira/projects/BSTOP/issues/BSTOP-13
Works:
import model sm
import model DMsimp_s_spin0
generate p p > y0 > t t~  [QCD]


29.3.2020
generate p p > w+ b b~, w+ > j j
add process p p > w- b b~, w- > j j
output pp2Wbb_pTj1min50GeV_allhad

24.4.2020 works!
import model sm-full
generate p p > w+ b @0
generate p p > w+ b j @1

# ljets need:
# Wbb + jets, W->lnu
generate p p > w+ b b~ @0, w+ > l+ vl
add process p p > w+ b b~ j @1, w+ > l+ vl
add process p p > w+ b b~ j j @2, w+ > l+ vl
add process p p > w- b b~ @0, w- > l- vl~
add process p p > w- b b~ j @1, w- > l- vl~
add process p p > w- b b~ j j @2, w- > l+ vl~

# jk 23.3.2021
# not that great idea;-)
generate p p > w+ w-, w+ > j j, w- > l- vl~ @0
add process p p > w+ w- b, w+ > j j, w- > l- vl~ @1
add process p p > w+ w- b b~, w+ > j j, w- > l- vl~ @2
add process p p > w+ w-, w- > j j, w+ > l+ vl @0
add process p p > w+ w- b, w- > j j, w+ > l+ vl @1
add process p p > w+ w- b b~, w- > j j, w+ > l+ vl @2

# jk 31.3.2021
# dibosons for l+jets:
generate p p > w+ w- b b~, w+ > j j, w- > l- vl∼
add process p p > w+ w- b b~, w- > j j, w+ > l- vl∼

# jk 31.3.2021
# possible allhad bg
generate p p > w+ w- b b~ @0, w+ > j j, w- > j j
# or incl. more jets:
generate p p > w+ w- b b~ @0, w+ > j j, w- > j j @0
add process p p > w+ w- b b~ j @0, w+ > j j, w- > j j @1
add process p p > w+ w- b b~ j j @0, w+ > j j, w- > j j @2
# ...but takes very long;)

# bg for allhad, generated
generate p p > w+ b b~ @0, w+ > j j 
add process p p > w+ b b~ j @1, w+ > j j
add process p p > w+ b b~ j j @2, w+ > j j
add process p p > w- b b~ @0, w- >  j 
add process p p > w- b b~ j @1, w- > j j
add process p p > w- b b~ j j @2, w- > j j

test 21.3.2021
generate p p > y0 > t t~ j [QCD]
0.01855 ± 4.9e-05 pb

# Higgs?
import model loop_qcd_qed_sm
generate p p > h [QCD]
# or even:
generate p p > h > z z [QCD]
generate p p > h > l+ l- l+ l- [QCD]
