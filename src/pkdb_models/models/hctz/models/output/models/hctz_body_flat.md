# Hydrochlorothiazide (HCTZ) body model

Model `hctz_body`, SBML Level 3 Version 2, read from hctz\_body\_flat.xml, written by sbmlode 0.3.2.

Hydrochlorothiazide (HCTZ) body model

Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of hydrochlorothiazide, built with the PBPK library pkpdsim.pbpk: the whole body with the absorption of HCTZ in the intestine, its distribution into the tissues and its renal excretion by filtration and tubular secretion, and the fluid and electrolyte model of the PD (FLUID) with the effect of HCTZ on the excretion of sodium and chloride and the blood pressure.

The content of this model has been carefully created in a manual research effort.

Terms of use

Copyright © 2026 Matthias König.

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

Redistribution and use of any part of this model, with or without modification, are permitted provided that the following conditions are met:

Redistributions of this SBML file must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in a different form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Units

| Time | Substance | Extent | Volume | Area | Length |
| --- | --- | --- | --- | --- | --- |
| min | mmol | mmol | l | m<sup>2</sup> | m |

## Compartments

| Symbol | Id | Name | Size | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Var}_{\mathrm{pl}}$ | `Var_pl` | arterial plasma | $1$ | l | ✓ |
| $\mathrm{Var}_{\mathrm{bc}}$ | `Var_bc` | arterial blood cells | $1$ | l | ✓ |
| $\mathrm{Var}_{\mathrm{pl\_hctz}}$ | `Var_pl_hctz` | plasma-equivalent capacity V\*BP of hctz, arterial pool | $1$ | l | ✓ |
| $\mathrm{Vve}_{\mathrm{pl}}$ | `Vve_pl` | venous plasma | $1$ | l | ✓ |
| $\mathrm{Vve}_{\mathrm{bc}}$ | `Vve_bc` | venous blood cells | $1$ | l | ✓ |
| $\mathrm{Vve}_{\mathrm{pl\_hctz}}$ | `Vve_pl_hctz` | plasma-equivalent capacity V\*BP of hctz, venous pool | $1$ | l | ✓ |
| $\mathrm{Vpo}_{\mathrm{pl}}$ | `Vpo_pl` | portal plasma | $1$ | l | ✓ |
| $\mathrm{Vpo}_{\mathrm{bc}}$ | `Vpo_bc` | portal blood cells | $1$ | l | ✓ |
| $\mathrm{Vpo}_{\mathrm{pl\_hctz}}$ | `Vpo_pl_hctz` | plasma-equivalent capacity V\*BP of hctz, portal pool | $1$ | l | ✓ |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vbile}$ | `Vbile` | bile | $0.058$ | l | ✓ |
| $\mathrm{LU}_{\mathrm{\_Vpl}}$ | `LU__Vpl` | plasma lung | $1$ | l | ✓ |
| $\mathrm{LU}_{\mathrm{\_Vti}}$ | `LU__Vti` | tissue lung | $1$ | l | ✓ |
| $\mathrm{LU}_{\mathrm{\_Vpl\_hctz}}$ | `LU__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, lung | $1$ | l | ✓ |
| $\mathrm{HE}_{\mathrm{\_Vpl}}$ | `HE__Vpl` | plasma heart | $1$ | l | ✓ |
| $\mathrm{HE}_{\mathrm{\_Vti}}$ | `HE__Vti` | tissue heart | $1$ | l | ✓ |
| $\mathrm{HE}_{\mathrm{\_Vpl\_hctz}}$ | `HE__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, heart | $1$ | l | ✓ |
| $\mathrm{BR}_{\mathrm{\_Vpl}}$ | `BR__Vpl` | plasma brain | $1$ | l | ✓ |
| $\mathrm{BR}_{\mathrm{\_Vti}}$ | `BR__Vti` | tissue brain | $1$ | l | ✓ |
| $\mathrm{BR}_{\mathrm{\_Vpl\_hctz}}$ | `BR__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, brain | $1$ | l | ✓ |
| $\mathrm{LI}_{\mathrm{\_Vpl}}$ | `LI__Vpl` | plasma liver | $1$ | l | ✓ |
| $\mathrm{LI}_{\mathrm{\_Vti}}$ | `LI__Vti` | tissue liver | $1$ | l | ✓ |
| $\mathrm{LI}_{\mathrm{\_Vpl\_hctz}}$ | `LI__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, liver | $1$ | l | ✓ |
| $\mathrm{KI}_{\mathrm{\_Vpl}}$ | `KI__Vpl` | plasma kidney | $1$ | l | ✓ |
| $\mathrm{KI}_{\mathrm{\_Vis}}$ | `KI__Vis` | interstitium kidney | $1$ | l | ✓ |
| $\mathrm{KI}_{\mathrm{\_Vic}}$ | `KI__Vic` | intracellular space kidney | $1$ | l | ✓ |
| $\mathrm{KI}_{\mathrm{\_Vpl\_hctz}}$ | `KI__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, kidney | $1$ | l | ✓ |
| $\mathrm{ST}_{\mathrm{\_Vpl}}$ | `ST__Vpl` | plasma stomach | $1$ | l | ✓ |
| $\mathrm{ST}_{\mathrm{\_Vti}}$ | `ST__Vti` | tissue stomach | $1$ | l | ✓ |
| $\mathrm{ST}_{\mathrm{\_Vpl\_hctz}}$ | `ST__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, stomach | $1$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vpl}}$ | `GU__Vpl` | plasma small intestine | $1$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vti}}$ | `GU__Vti` | tissue small intestine | $1$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_st}}$ | `GU__Vlumen_st` | lumen stomach | $0.028$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_du}}$ | `GU__Vlumen_du` | lumen duodenum | $0.007819$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_jej1}}$ | `GU__Vlumen_jej1` | lumen upper jejunum | $0.01955$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_jej2}}$ | `GU__Vlumen_jej2` | lumen lower jejunum | $0.01955$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_ile1}}$ | `GU__Vlumen_ile1` | lumen upper ileum | $0.02904$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_ile2}}$ | `GU__Vlumen_ile2` | lumen lower ileum | $0.02904$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_cae}}$ | `GU__Vlumen_cae` | lumen caecum | $0.002093$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_asc}}$ | `GU__Vlumen_asc` | lumen colon ascendens | $0.002093$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_tra}}$ | `GU__Vlumen_tra` | lumen colon transversum | $0.002111$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_des}}$ | `GU__Vlumen_des` | lumen colon descendens | $0.002111$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_sig}}$ | `GU__Vlumen_sig` | lumen colon sigmoid | $0.002296$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vlumen\_rec}}$ | `GU__Vlumen_rec` | lumen rectum | $0.002296$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vpl\_hctz}}$ | `GU__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, small intestine | $1$ | l | ✓ |
| $\mathrm{SP}_{\mathrm{\_Vpl}}$ | `SP__Vpl` | plasma spleen | $1$ | l | ✓ |
| $\mathrm{SP}_{\mathrm{\_Vti}}$ | `SP__Vti` | tissue spleen | $1$ | l | ✓ |
| $\mathrm{SP}_{\mathrm{\_Vpl\_hctz}}$ | `SP__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, spleen | $1$ | l | ✓ |
| $\mathrm{PA}_{\mathrm{\_Vpl}}$ | `PA__Vpl` | plasma pancreas | $1$ | l | ✓ |
| $\mathrm{PA}_{\mathrm{\_Vti}}$ | `PA__Vti` | tissue pancreas | $1$ | l | ✓ |
| $\mathrm{PA}_{\mathrm{\_Vpl\_hctz}}$ | `PA__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, pancreas | $1$ | l | ✓ |
| $\mathrm{MU}_{\mathrm{\_Vpl}}$ | `MU__Vpl` | plasma muscle | $1$ | l | ✓ |
| $\mathrm{MU}_{\mathrm{\_Vti}}$ | `MU__Vti` | tissue muscle | $1$ | l | ✓ |
| $\mathrm{MU}_{\mathrm{\_Vpl\_hctz}}$ | `MU__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, muscle | $1$ | l | ✓ |
| $\mathrm{SK}_{\mathrm{\_Vpl}}$ | `SK__Vpl` | plasma skin | $1$ | l | ✓ |
| $\mathrm{SK}_{\mathrm{\_Vti}}$ | `SK__Vti` | tissue skin | $1$ | l | ✓ |
| $\mathrm{SK}_{\mathrm{\_Vpl\_hctz}}$ | `SK__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, skin | $1$ | l | ✓ |
| $\mathrm{AD}_{\mathrm{\_Vpl}}$ | `AD__Vpl` | plasma adipose | $1$ | l | ✓ |
| $\mathrm{AD}_{\mathrm{\_Vti}}$ | `AD__Vti` | tissue adipose | $1$ | l | ✓ |
| $\mathrm{AD}_{\mathrm{\_Vpl\_hctz}}$ | `AD__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, adipose | $1$ | l | ✓ |
| $\mathrm{BO}_{\mathrm{\_Vpl}}$ | `BO__Vpl` | plasma bone | $1$ | l | ✓ |
| $\mathrm{BO}_{\mathrm{\_Vti}}$ | `BO__Vti` | tissue bone | $1$ | l | ✓ |
| $\mathrm{BO}_{\mathrm{\_Vpl\_hctz}}$ | `BO__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, bone | $1$ | l | ✓ |
| $\mathrm{GO}_{\mathrm{\_Vpl}}$ | `GO__Vpl` | plasma gonads | $1$ | l | ✓ |
| $\mathrm{GO}_{\mathrm{\_Vti}}$ | `GO__Vti` | tissue gonads | $1$ | l | ✓ |
| $\mathrm{GO}_{\mathrm{\_Vpl\_hctz}}$ | `GO__Vpl_hctz` | plasma-equivalent capacity V\*f\_vas\*BP of hctz, gonads | $1$ | l | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_ECF}}$ | `FLUID__ECF` | extracellular fluid (ECF) | $\mathrm{NaN}$ | l |  |
| $\mathrm{FLUID}_{\mathrm{\_Vloop}}$ | `FLUID__Vloop` | renal tubule | $0.5$ | l |  |
| $\mathrm{FLUID}_{\mathrm{\_Vurine}}$ | `FLUID__Vurine` | urine | $10^{-6}$ | l |  |
| $\mathrm{FLUID}_{\mathrm{\_Vki}}$ | `FLUID__Vki` | kidney | $\mathrm{NaN}$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{Car}_{\mathrm{hctz}}$ | `Car_hctz` | hydrochlorothiazide (arterial plasma) | $\mathrm{Var}_{\mathrm{pl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{hctz}}$ | `Cve_hctz` | hydrochlorothiazide (venous plasma) | $\mathrm{Vve}_{\mathrm{pl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{hctz}}$ | `Cpo_hctz` | hydrochlorothiazide (portal plasma) | $\mathrm{Vpo}_{\mathrm{pl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{hctz}}$ | `Aurine_hctz` | hydrochlorothiazide (urine) | $\mathrm{Vurine}$ | $0$ | mmol | amount |
| $\mathrm{Afeces}_{\mathrm{hctz}}$ | `Afeces_hctz` | hydrochlorothiazide (feces) | $\mathrm{Vfeces}$ | $0$ | mmol | amount |
| $\mathrm{Cbile}_{\mathrm{hctz}}$ | `Cbile_hctz` | hydrochlorothiazide (bile) | $\mathrm{Vbile}$ | $0$ | mmol/l | concentration |
| $\mathrm{LU}_{\mathrm{\_Cpl\_hctz}}$ | `LU__Cpl_hctz` | hydrochlorothiazide (plasma, lung) | $\mathrm{LU}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LU}_{\mathrm{\_Cti\_hctz}}$ | `LU__Cti_hctz` | hydrochlorothiazide (tissue, lung) | $\mathrm{LU}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{HE}_{\mathrm{\_Cpl\_hctz}}$ | `HE__Cpl_hctz` | hydrochlorothiazide (plasma, heart) | $\mathrm{HE}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{HE}_{\mathrm{\_Cti\_hctz}}$ | `HE__Cti_hctz` | hydrochlorothiazide (tissue, heart) | $\mathrm{HE}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{BR}_{\mathrm{\_Cpl\_hctz}}$ | `BR__Cpl_hctz` | hydrochlorothiazide (plasma, brain) | $\mathrm{BR}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{BR}_{\mathrm{\_Cti\_hctz}}$ | `BR__Cti_hctz` | hydrochlorothiazide (tissue, brain) | $\mathrm{BR}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_Cpl\_hctz}}$ | `LI__Cpl_hctz` | hydrochlorothiazide (plasma, liver) | $\mathrm{LI}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_Cti\_hctz}}$ | `LI__Cti_hctz` | hydrochlorothiazide (tissue, liver) | $\mathrm{LI}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{KI}_{\mathrm{\_Cpl\_hctz}}$ | `KI__Cpl_hctz` | hydrochlorothiazide (plasma, kidney) | $\mathrm{KI}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{KI}_{\mathrm{\_Cis\_hctz}}$ | `KI__Cis_hctz` | hydrochlorothiazide (interstitial, kidney) | $\mathrm{KI}_{\mathrm{\_Vis}}$ | $0$ | mmol/l | concentration |
| $\mathrm{KI}_{\mathrm{\_Cic\_hctz}}$ | `KI__Cic_hctz` | hydrochlorothiazide (intracellular, kidney) | $\mathrm{KI}_{\mathrm{\_Vic}}$ | $0$ | mmol/l | concentration |
| $\mathrm{ST}_{\mathrm{\_Cpl\_hctz}}$ | `ST__Cpl_hctz` | hydrochlorothiazide (plasma, stomach) | $\mathrm{ST}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{ST}_{\mathrm{\_Cti\_hctz}}$ | `ST__Cti_hctz` | hydrochlorothiazide (tissue, stomach) | $\mathrm{ST}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ | `GU__Cpl_hctz` | hydrochlorothiazide (plasma, small intestine) | $\mathrm{GU}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Cti\_hctz}}$ | `GU__Cti_hctz` | hydrochlorothiazide (tissue, small intestine) | $\mathrm{GU}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_st\_hctz}}$ | `GU__Clumen_st_hctz` | hydrochlorothiazide (lumen stomach) | $\mathrm{GU}_{\mathrm{\_Vlumen\_st}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_du\_hctz}}$ | `GU__Clumen_du_hctz` | hydrochlorothiazide (lumen duodenum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_du}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_jej1\_hctz}}$ | `GU__Clumen_jej1_hctz` | hydrochlorothiazide (lumen upper jejunum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_jej1}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_jej2\_hctz}}$ | `GU__Clumen_jej2_hctz` | hydrochlorothiazide (lumen lower jejunum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_jej2}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_ile1\_hctz}}$ | `GU__Clumen_ile1_hctz` | hydrochlorothiazide (lumen upper ileum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_ile1}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_ile2\_hctz}}$ | `GU__Clumen_ile2_hctz` | hydrochlorothiazide (lumen lower ileum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_ile2}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_cae\_hctz}}$ | `GU__Clumen_cae_hctz` | hydrochlorothiazide (lumen caecum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_cae}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_asc\_hctz}}$ | `GU__Clumen_asc_hctz` | hydrochlorothiazide (lumen colon ascendens) | $\mathrm{GU}_{\mathrm{\_Vlumen\_asc}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_tra\_hctz}}$ | `GU__Clumen_tra_hctz` | hydrochlorothiazide (lumen colon transversum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_tra}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_des\_hctz}}$ | `GU__Clumen_des_hctz` | hydrochlorothiazide (lumen colon descendens) | $\mathrm{GU}_{\mathrm{\_Vlumen\_des}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_sig\_hctz}}$ | `GU__Clumen_sig_hctz` | hydrochlorothiazide (lumen colon sigmoid) | $\mathrm{GU}_{\mathrm{\_Vlumen\_sig}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Clumen\_rec\_hctz}}$ | `GU__Clumen_rec_hctz` | hydrochlorothiazide (lumen rectum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_rec}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_Asolid\_du\_hctz}}$ | `GU__Asolid_du_hctz` | hydrochlorothiazide (undissolved, lumen duodenum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_du}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_jej1\_hctz}}$ | `GU__Asolid_jej1_hctz` | hydrochlorothiazide (undissolved, lumen upper jejunum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_jej1}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_jej2\_hctz}}$ | `GU__Asolid_jej2_hctz` | hydrochlorothiazide (undissolved, lumen lower jejunum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_jej2}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_ile1\_hctz}}$ | `GU__Asolid_ile1_hctz` | hydrochlorothiazide (undissolved, lumen upper ileum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_ile1}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_ile2\_hctz}}$ | `GU__Asolid_ile2_hctz` | hydrochlorothiazide (undissolved, lumen lower ileum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_ile2}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_cae\_hctz}}$ | `GU__Asolid_cae_hctz` | hydrochlorothiazide (undissolved, lumen caecum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_cae}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_asc\_hctz}}$ | `GU__Asolid_asc_hctz` | hydrochlorothiazide (undissolved, lumen colon ascendens) | $\mathrm{GU}_{\mathrm{\_Vlumen\_asc}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_tra\_hctz}}$ | `GU__Asolid_tra_hctz` | hydrochlorothiazide (undissolved, lumen colon transversum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_tra}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_des\_hctz}}$ | `GU__Asolid_des_hctz` | hydrochlorothiazide (undissolved, lumen colon descendens) | $\mathrm{GU}_{\mathrm{\_Vlumen\_des}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_sig\_hctz}}$ | `GU__Asolid_sig_hctz` | hydrochlorothiazide (undissolved, lumen colon sigmoid) | $\mathrm{GU}_{\mathrm{\_Vlumen\_sig}}$ | $0$ | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_Asolid\_rec\_hctz}}$ | `GU__Asolid_rec_hctz` | hydrochlorothiazide (undissolved, lumen rectum) | $\mathrm{GU}_{\mathrm{\_Vlumen\_rec}}$ | $0$ | mmol | amount |
| $\mathrm{SP}_{\mathrm{\_Cpl\_hctz}}$ | `SP__Cpl_hctz` | hydrochlorothiazide (plasma, spleen) | $\mathrm{SP}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{SP}_{\mathrm{\_Cti\_hctz}}$ | `SP__Cti_hctz` | hydrochlorothiazide (tissue, spleen) | $\mathrm{SP}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{PA}_{\mathrm{\_Cpl\_hctz}}$ | `PA__Cpl_hctz` | hydrochlorothiazide (plasma, pancreas) | $\mathrm{PA}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{PA}_{\mathrm{\_Cti\_hctz}}$ | `PA__Cti_hctz` | hydrochlorothiazide (tissue, pancreas) | $\mathrm{PA}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{MU}_{\mathrm{\_Cpl\_hctz}}$ | `MU__Cpl_hctz` | hydrochlorothiazide (plasma, muscle) | $\mathrm{MU}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{MU}_{\mathrm{\_Cti\_hctz}}$ | `MU__Cti_hctz` | hydrochlorothiazide (tissue, muscle) | $\mathrm{MU}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{SK}_{\mathrm{\_Cpl\_hctz}}$ | `SK__Cpl_hctz` | hydrochlorothiazide (plasma, skin) | $\mathrm{SK}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{SK}_{\mathrm{\_Cti\_hctz}}$ | `SK__Cti_hctz` | hydrochlorothiazide (tissue, skin) | $\mathrm{SK}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{AD}_{\mathrm{\_Cpl\_hctz}}$ | `AD__Cpl_hctz` | hydrochlorothiazide (plasma, adipose) | $\mathrm{AD}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{AD}_{\mathrm{\_Cti\_hctz}}$ | `AD__Cti_hctz` | hydrochlorothiazide (tissue, adipose) | $\mathrm{AD}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{BO}_{\mathrm{\_Cpl\_hctz}}$ | `BO__Cpl_hctz` | hydrochlorothiazide (plasma, bone) | $\mathrm{BO}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{BO}_{\mathrm{\_Cti\_hctz}}$ | `BO__Cti_hctz` | hydrochlorothiazide (tissue, bone) | $\mathrm{BO}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GO}_{\mathrm{\_Cpl\_hctz}}$ | `GO__Cpl_hctz` | hydrochlorothiazide (plasma, gonads) | $\mathrm{GO}_{\mathrm{\_Vpl\_hctz}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GO}_{\mathrm{\_Cti\_hctz}}$ | `GO__Cti_hctz` | hydrochlorothiazide (tissue, gonads) | $\mathrm{GO}_{\mathrm{\_Vti}}$ | $0$ | mmol/l | concentration |
| $\mathrm{FLUID}_{\mathrm{\_na}}$ | `FLUID__na` | Sodium (Na+) (ECF) | $\mathrm{FLUID}_{\mathrm{\_ECF}}$ | $139.941046660775$ | mmol/l | concentration |
| $\mathrm{FLUID}_{\mathrm{\_na\_loop}}$ | `FLUID__na_loop` | Sodium (Na+) (renal tubule) | $\mathrm{FLUID}_{\mathrm{\_Vloop}}$ | $140.295139436904$ | mmol/l | concentration |
| $\mathrm{FLUID}_{\mathrm{\_na\_urine}}$ | `FLUID__na_urine` | Sodium (Na+) (urine) | $\mathrm{FLUID}_{\mathrm{\_Vurine}}$ | $0$ | mmol | amount |
| $\mathrm{FLUID}_{\mathrm{\_cl}}$ | `FLUID__cl` | Chloride (Cl-) (ECF) | $\mathrm{FLUID}_{\mathrm{\_ECF}}$ | $102.375558447522$ | mmol/l | concentration |
| $\mathrm{FLUID}_{\mathrm{\_cl\_loop}}$ | `FLUID__cl_loop` | Chloride (Cl-) (renal tubule) | $\mathrm{FLUID}_{\mathrm{\_Vloop}}$ | $100.142772655399$ | mmol/l | concentration |
| $\mathrm{FLUID}_{\mathrm{\_cl\_urine}}$ | `FLUID__cl_urine` | Chloride (Cl-) (urine) | $\mathrm{FLUID}_{\mathrm{\_Vurine}}$ | $0$ | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{BW}$ | `BW` | body weight \[kg\] | $73$ | kg | ✓ |
| $\mathrm{HEIGHT}$ | `HEIGHT` | height \[cm\] | $176$ | cm | ✓ |
| $f_{\mathrm{renal\_function}}$ | `f_renal_function` | renal function | $1$ | \- | ✓ |
| $f_{\mathrm{cardiac\_function}}$ | `f_cardiac_function` | cardiac function | $1$ | \- | ✓ |
| $f_{\mathrm{shunt}}$ | `f_shunt` | portosystemic shunt | $0$ | \- | ✓ |
| $f_{\mathrm{functional}}$ | `f_functional` | functional liver fraction | $1$ | \- | ✓ |
| $\mathrm{BW}_{\mathrm{ref}}$ | `BW_ref` | reference body weight \[kg\] | $73$ | kg | ✓ |
| $\mathrm{HEIGHT}_{\mathrm{ref}}$ | `HEIGHT_ref` | reference height \[cm\] | $176$ | cm | ✓ |
| $\mathrm{BSA}_{\mathrm{ref}}$ | `BSA_ref` | reference body surface area \[m2\] |  | m<sup>2</sup> | ✓ |
| $\mathrm{fage}_{\mathrm{FFM}}$ | `fage_FFM` | age factor fat-free mass | $1$ | \- | ✓ |
| $\mathrm{FFM}_{\mathrm{ref}}$ | `FFM_ref` | reference fat-free mass \[kg\] |  | kg | ✓ |
| $\mathrm{CO}_{\mathrm{ref}}$ | `CO_ref` | reference cardiac output \[l/min\] | $6.5$ | l/min | ✓ |
| $\mathrm{GFR}_{\mathrm{ref}}$ | `GFR_ref` | reference glomerular filtration rate \[l/min\] | $0.125$ | l/min | ✓ |
| $\mathrm{Vblood}_{\mathrm{ref}}$ | `Vblood_ref` | reference blood volume \[l\] | $5.3$ | l | ✓ |
| $\mathrm{fage}_{\mathrm{HCT}}$ | `fage_HCT` | age factor hematocrit | $1$ | \- | ✓ |
| $\mathrm{HCT}_{\mathrm{ref}}$ | `HCT_ref` | reference hematocrit |  | \- | ✓ |
| $\mathrm{HCT}$ | `HCT` | hematocrit |  | \- | ✓ |
| $\mathrm{Mlu}_{\mathrm{ref}}$ | `Mlu_ref` | reference tissue mass lung \[kg\] | $0.5$ | kg | ✓ |
| $\mathrm{Mhe}_{\mathrm{ref}}$ | `Mhe_ref` | reference tissue mass heart \[kg\] | $0.33$ | kg | ✓ |
| $\mathrm{Mbr}_{\mathrm{ref}}$ | `Mbr_ref` | reference tissue mass brain \[kg\] | $1.45$ | kg | ✓ |
| $\mathrm{Mli}_{\mathrm{ref}}$ | `Mli_ref` | reference tissue mass liver \[kg\] | $1.8$ | kg | ✓ |
| $\mathrm{Mki}_{\mathrm{ref}}$ | `Mki_ref` | reference tissue mass kidney \[kg\] | $0.31$ | kg | ✓ |
| $\mathrm{Mst}_{\mathrm{ref}}$ | `Mst_ref` | reference tissue mass stomach \[kg\] | $0.15$ | kg | ✓ |
| $\mathrm{Msi}_{\mathrm{ref}}$ | `Msi_ref` | reference tissue mass small intestine \[kg\] | $0.65$ | kg | ✓ |
| $\mathrm{Mla}_{\mathrm{ref}}$ | `Mla_ref` | reference tissue mass large intestine \[kg\] | $0.37$ | kg | ✓ |
| $\mathrm{Msp}_{\mathrm{ref}}$ | `Msp_ref` | reference tissue mass spleen \[kg\] | $0.15$ | kg | ✓ |
| $\mathrm{Mpa}_{\mathrm{ref}}$ | `Mpa_ref` | reference tissue mass pancreas \[kg\] | $0.14$ | kg | ✓ |
| $\mathrm{Mmu}_{\mathrm{ref}}$ | `Mmu_ref` | reference tissue mass muscle \[kg\] | $29$ | kg | ✓ |
| $\mathrm{Msk}_{\mathrm{ref}}$ | `Msk_ref` | reference tissue mass skin \[kg\] | $3.3$ | kg | ✓ |
| $\mathrm{Mbo}_{\mathrm{ref}}$ | `Mbo_ref` | reference tissue mass bone \[kg\] | $10.5$ | kg | ✓ |
| $\mathrm{Mgo}_{\mathrm{ref}}$ | `Mgo_ref` | reference tissue mass gonads \[kg\] | $0.035$ | kg | ✓ |
| $\mathrm{fage}_{\mathrm{Qbr}}$ | `fage_Qbr` | age factor brain flow | $1$ | \- | ✓ |
| $\mathrm{fage}_{\mathrm{Qli}}$ | `fage_Qli` | age factor liver flow | $1$ | \- | ✓ |
| $\mathrm{fage}_{\mathrm{Qki}}$ | `fage_Qki` | age factor kidney flow | $1$ | \- | ✓ |
| $\mathrm{fage}_{\mathrm{Qrest}}$ | `fage_Qrest` | age factor of the organs besides the brain |  | \- | ✓ |
| $\mathrm{fage}_{\mathrm{Qother}}$ | `fage_Qother` | age factor of the organs without a factor of their own |  | \- | ✓ |
| $\mathrm{fQhe}$ | `fQhe` | blood flow fraction heart |  | \- | ✓ |
| $\mathrm{fQbr}$ | `fQbr` | blood flow fraction brain |  | \- | ✓ |
| $\mathrm{fQli}$ | `fQli` | blood flow fraction liver |  | \- | ✓ |
| $\mathrm{fQki}$ | `fQki` | blood flow fraction kidney |  | \- | ✓ |
| $\mathrm{fQst}$ | `fQst` | blood flow fraction stomach |  | \- | ✓ |
| $\mathrm{fQsi}$ | `fQsi` | blood flow fraction small intestine |  | \- | ✓ |
| $\mathrm{fQla}$ | `fQla` | blood flow fraction large intestine |  | \- | ✓ |
| $\mathrm{fQsp}$ | `fQsp` | blood flow fraction spleen |  | \- | ✓ |
| $\mathrm{fQpa}$ | `fQpa` | blood flow fraction pancreas |  | \- | ✓ |
| $\mathrm{fQmu}$ | `fQmu` | blood flow fraction muscle |  | \- | ✓ |
| $\mathrm{fQsk}$ | `fQsk` | blood flow fraction skin |  | \- | ✓ |
| $\mathrm{fQad}$ | `fQad` | blood flow fraction adipose |  | \- | ✓ |
| $\mathrm{fQbo}$ | `fQbo` | blood flow fraction bone |  | \- | ✓ |
| $\mathrm{fQgo}$ | `fQgo` | blood flow fraction gonads |  | \- | ✓ |
| $\mathrm{fVar}$ | `fVar` | blood fraction arterial pool | $0.105$ | \- | ✓ |
| $\mathrm{fVve}$ | `fVve` | blood fraction venous pool | $0.246772$ | \- | ✓ |
| $\mathrm{fVpo}$ | `fVpo` | blood fraction portal pool | $0.000828$ | \- | ✓ |
| $\mathrm{BMI}$ | `BMI` | body mass index \[kg/m2\] |  | kg/m<sup>2</sup> | ✓ |
| $\mathrm{BSA}$ | `BSA` | body surface area \[m2\] |  | m<sup>2</sup> | ✓ |
| $\mathrm{FFM}$ | `FFM` | fat-free mass \[kg\] |  | kg | ✓ |
| $\mathrm{SV}_{\mathrm{tis}}$ | `SV_tis` | scaling factor of the lean tissues |  | \- | ✓ |
| $\mathrm{Vblood}$ | `Vblood` | blood volume \[l\] |  | l | ✓ |
| $\mathrm{Mlu}$ | `Mlu` | tissue mass lung \[kg\] |  | kg | ✓ |
| $\mathrm{Mhe}$ | `Mhe` | tissue mass heart \[kg\] |  | kg | ✓ |
| $\mathrm{Mbr}$ | `Mbr` | tissue mass brain \[kg\] |  | kg | ✓ |
| $\mathrm{Mli}$ | `Mli` | tissue mass liver \[kg\] |  | kg | ✓ |
| $\mathrm{Mki}$ | `Mki` | tissue mass kidney \[kg\] |  | kg | ✓ |
| $\mathrm{Mst}$ | `Mst` | tissue mass stomach \[kg\] |  | kg | ✓ |
| $\mathrm{Msi}$ | `Msi` | tissue mass small intestine \[kg\] |  | kg | ✓ |
| $\mathrm{Mla}$ | `Mla` | tissue mass large intestine \[kg\] |  | kg | ✓ |
| $\mathrm{Msp}$ | `Msp` | tissue mass spleen \[kg\] |  | kg | ✓ |
| $\mathrm{Mpa}$ | `Mpa` | tissue mass pancreas \[kg\] |  | kg | ✓ |
| $\mathrm{Mmu}$ | `Mmu` | tissue mass muscle \[kg\] |  | kg | ✓ |
| $\mathrm{Msk}$ | `Msk` | tissue mass skin \[kg\] |  | kg | ✓ |
| $\mathrm{Mbo}$ | `Mbo` | tissue mass bone \[kg\] |  | kg | ✓ |
| $\mathrm{Mgo}$ | `Mgo` | tissue mass gonads \[kg\] |  | kg | ✓ |
| $\mathrm{Mlean}$ | `Mlean` | mass of the lean organ tissues \[kg\] |  | kg | ✓ |
| $\mathrm{Mad}$ | `Mad` | tissue mass adipose \[kg\] |  | kg | ✓ |
| $\mathrm{Vlu}$ | `Vlu` | volume lung \[l\] |  | l | ✓ |
| $\mathrm{Vhe}$ | `Vhe` | volume heart \[l\] |  | l | ✓ |
| $\mathrm{Vbr}$ | `Vbr` | volume brain \[l\] |  | l | ✓ |
| $\mathrm{Vli}$ | `Vli` | volume liver \[l\] |  | l | ✓ |
| $\mathrm{Vki}$ | `Vki` | volume kidney \[l\] |  | l | ✓ |
| $\mathrm{Vst}$ | `Vst` | volume stomach \[l\] |  | l | ✓ |
| $\mathrm{Vsi}$ | `Vsi` | volume small intestine \[l\] |  | l | ✓ |
| $\mathrm{Vla}$ | `Vla` | volume large intestine \[l\] |  | l | ✓ |
| $\mathrm{Vsp}$ | `Vsp` | volume spleen \[l\] |  | l | ✓ |
| $\mathrm{Vpa}$ | `Vpa` | volume pancreas \[l\] |  | l | ✓ |
| $\mathrm{Vmu}$ | `Vmu` | volume muscle \[l\] |  | l | ✓ |
| $\mathrm{Vsk}$ | `Vsk` | volume skin \[l\] |  | l | ✓ |
| $\mathrm{Vad}$ | `Vad` | volume adipose \[l\] |  | l | ✓ |
| $\mathrm{Vbo}$ | `Vbo` | volume bone \[l\] |  | l | ✓ |
| $\mathrm{Vgo}$ | `Vgo` | volume gonads \[l\] |  | l | ✓ |
| $\mathrm{Var}$ | `Var` | volume arterial blood \[l\] |  | l | ✓ |
| $\mathrm{Vve}$ | `Vve` | volume venous blood \[l\] |  | l | ✓ |
| $\mathrm{Vpo}$ | `Vpo` | volume portal blood \[l\] |  | l | ✓ |
| $f_{\mathrm{vas\_lu}}$ | `f_vas_lu` | vascular fraction lung |  | \- | ✓ |
| $f_{\mathrm{int\_lu}}$ | `f_int_lu` | interstitial fraction lung |  | \- | ✓ |
| $f_{\mathrm{vas\_he}}$ | `f_vas_he` | vascular fraction heart |  | \- | ✓ |
| $f_{\mathrm{int\_he}}$ | `f_int_he` | interstitial fraction heart |  | \- | ✓ |
| $f_{\mathrm{vas\_br}}$ | `f_vas_br` | vascular fraction brain |  | \- | ✓ |
| $f_{\mathrm{int\_br}}$ | `f_int_br` | interstitial fraction brain |  | \- | ✓ |
| $f_{\mathrm{vas\_li}}$ | `f_vas_li` | vascular fraction liver |  | \- | ✓ |
| $f_{\mathrm{int\_li}}$ | `f_int_li` | interstitial fraction liver |  | \- | ✓ |
| $f_{\mathrm{vas\_ki}}$ | `f_vas_ki` | vascular fraction kidney |  | \- | ✓ |
| $f_{\mathrm{int\_ki}}$ | `f_int_ki` | interstitial fraction kidney |  | \- | ✓ |
| $f_{\mathrm{vas\_st}}$ | `f_vas_st` | vascular fraction stomach |  | \- | ✓ |
| $f_{\mathrm{int\_st}}$ | `f_int_st` | interstitial fraction stomach |  | \- | ✓ |
| $f_{\mathrm{vas\_si}}$ | `f_vas_si` | vascular fraction small intestine |  | \- | ✓ |
| $f_{\mathrm{int\_si}}$ | `f_int_si` | interstitial fraction small intestine |  | \- | ✓ |
| $f_{\mathrm{vas\_la}}$ | `f_vas_la` | vascular fraction large intestine |  | \- | ✓ |
| $f_{\mathrm{int\_la}}$ | `f_int_la` | interstitial fraction large intestine |  | \- | ✓ |
| $f_{\mathrm{vas\_sp}}$ | `f_vas_sp` | vascular fraction spleen |  | \- | ✓ |
| $f_{\mathrm{int\_sp}}$ | `f_int_sp` | interstitial fraction spleen |  | \- | ✓ |
| $f_{\mathrm{vas\_pa}}$ | `f_vas_pa` | vascular fraction pancreas |  | \- | ✓ |
| $f_{\mathrm{int\_pa}}$ | `f_int_pa` | interstitial fraction pancreas |  | \- | ✓ |
| $f_{\mathrm{vas\_mu}}$ | `f_vas_mu` | vascular fraction muscle |  | \- | ✓ |
| $f_{\mathrm{int\_mu}}$ | `f_int_mu` | interstitial fraction muscle |  | \- | ✓ |
| $f_{\mathrm{vas\_sk}}$ | `f_vas_sk` | vascular fraction skin |  | \- | ✓ |
| $f_{\mathrm{int\_sk}}$ | `f_int_sk` | interstitial fraction skin |  | \- | ✓ |
| $f_{\mathrm{vas\_ad}}$ | `f_vas_ad` | vascular fraction adipose |  | \- | ✓ |
| $f_{\mathrm{int\_ad}}$ | `f_int_ad` | interstitial fraction adipose |  | \- | ✓ |
| $f_{\mathrm{vas\_bo}}$ | `f_vas_bo` | vascular fraction bone |  | \- | ✓ |
| $f_{\mathrm{int\_bo}}$ | `f_int_bo` | interstitial fraction bone |  | \- | ✓ |
| $f_{\mathrm{vas\_go}}$ | `f_vas_go` | vascular fraction gonads |  | \- | ✓ |
| $f_{\mathrm{int\_go}}$ | `f_int_go` | interstitial fraction gonads |  | \- | ✓ |
| $\mathrm{CO}_{\mathrm{base}}$ | `CO_base` | cardiac output without impairment \[l/min\] |  | l/min | ✓ |
| $\mathrm{CO}$ | `CO` | cardiac output \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qlu}$ | `Qlu` | blood flow lung \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qhe}$ | `Qhe` | blood flow heart \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qbr}$ | `Qbr` | blood flow brain \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qli}$ | `Qli` | blood flow liver \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qki}$ | `Qki` | blood flow kidney \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qst}$ | `Qst` | blood flow stomach \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qsi}$ | `Qsi` | blood flow small intestine \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qla}$ | `Qla` | blood flow large intestine \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qsp}$ | `Qsp` | blood flow spleen \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qpa}$ | `Qpa` | blood flow pancreas \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qmu}$ | `Qmu` | blood flow muscle \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qsk}$ | `Qsk` | blood flow skin \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qad}$ | `Qad` | blood flow adipose \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qbo}$ | `Qbo` | blood flow bone \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qgo}$ | `Qgo` | blood flow gonads \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qha}$ | `Qha` | hepatic arterial blood flow \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qpo}$ | `Qpo` | portal venous blood flow \[l/min\] |  | l/min | ✓ |
| $\mathrm{Qh}$ | `Qh` | liver blood flow \[l/min\] |  | l/min | ✓ |
| $\mathrm{fage}_{\mathrm{GFR}}$ | `fage_GFR` | age factor GFR | $1$ | \- | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate at renal function 1 \[l/min\] |  | l/min | ✓ |
| $\mathrm{GFR}$ | `GFR` | glomerular filtration rate \[l/min\] |  | l/min | ✓ |
| $\mathrm{CP}_{\mathrm{severity}}$ | `CP_severity` | severity of liver cirrhosis | $0$ | \- | ✓ |
| $\mathrm{HF}_{\mathrm{severity}}$ | `HF_severity` | severity of heart failure | $0$ | \- | ✓ |
| $\mathrm{CKD}_{\mathrm{hepatic}}$ | `CKD_hepatic` | hepatic changes of chronic kidney disease | $0$ | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{functional\_liver}}$ | `fcp_functional_liver` | cirrhosis factor functional\_liver |  | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{hepatic\_artery\_flow}}$ | `fcp_hepatic_artery_flow` | cirrhosis factor hepatic\_artery\_flow |  | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{kidney\_flow}}$ | `fcp_kidney_flow` | cirrhosis factor kidney\_flow |  | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{cardiac\_index}}$ | `fcp_cardiac_index` | cirrhosis factor cardiac\_index |  | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{gfr}}$ | `fcp_gfr` | cirrhosis factor gfr |  | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{albumin}}$ | `fcp_albumin` | cirrhosis factor albumin |  | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{agp}}$ | `fcp_agp` | cirrhosis factor agp |  | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{hematocrit}}$ | `fcp_hematocrit` | cirrhosis factor hematocrit |  | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{shunt}}$ | `fcp_shunt` | cirrhosis factor shunt |  | \- | ✓ |
| $\mathrm{fcp}_{\mathrm{rest\_flow}}$ | `fcp_rest_flow` | cirrhosis factor flow of the other organs |  | \- | ✓ |
| $\mathrm{eGFR}$ | `eGFR` | GFR per 1.73 m2 of the renal function \[l/min\] |  | l/min | ✓ |
| $\mathrm{fckd}_{\mathrm{plasma\_protein}}$ | `fckd_plasma_protein` | CKD factor plasma\_protein |  | \- | ✓ |
| $\mathrm{fckd}_{\mathrm{hematocrit}}$ | `fckd_hematocrit` | CKD factor hematocrit |  | \- | ✓ |
| $\mathrm{fckd}_{\mathrm{kidney\_volume}}$ | `fckd_kidney_volume` | CKD factor kidney\_volume |  | \- | ✓ |
| $\mathrm{fckd}_{\mathrm{kidney\_flow}}$ | `fckd_kidney_flow` | CKD factor kidney\_flow |  | \- | ✓ |
| $\mathrm{fckd}_{\mathrm{gastric\_emptying\_time}}$ | `fckd_gastric_emptying_time` | CKD factor gastric\_emptying\_time |  | \- | ✓ |
| $\mathrm{fckd}_{\mathrm{si\_transit\_time}}$ | `fckd_si_transit_time` | CKD factor si\_transit\_time |  | \- | ✓ |
| $\mathrm{fhf}_{\mathrm{liver\_flow}}$ | `fhf_liver_flow` | heart failure factor liver flow |  | \- | ✓ |
| $\mathrm{fhf}_{\mathrm{kidney\_flow}}$ | `fhf_kidney_flow` | heart failure factor kidney flow |  | \- | ✓ |
| $\mathrm{fhf}_{\mathrm{peripheral\_flow}}$ | `fhf_peripheral_flow` | heart failure factor peripheral flow |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qhe}}$ | `fimp_Qhe` | impairment factor Qhe |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qbr}}$ | `fimp_Qbr` | impairment factor Qbr |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qli}}$ | `fimp_Qli` | impairment factor Qli |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qki}}$ | `fimp_Qki` | impairment factor Qki |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qst}}$ | `fimp_Qst` | impairment factor Qst |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qsi}}$ | `fimp_Qsi` | impairment factor Qsi |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qla}}$ | `fimp_Qla` | impairment factor Qla |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qsp}}$ | `fimp_Qsp` | impairment factor Qsp |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qpa}}$ | `fimp_Qpa` | impairment factor Qpa |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qmu}}$ | `fimp_Qmu` | impairment factor Qmu |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qsk}}$ | `fimp_Qsk` | impairment factor Qsk |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qad}}$ | `fimp_Qad` | impairment factor Qad |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qbo}}$ | `fimp_Qbo` | impairment factor Qbo |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Qgo}}$ | `fimp_Qgo` | impairment factor Qgo |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{CO}}$ | `fimp_CO` | impairment factor cardiac output |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{GFR}}$ | `fimp_GFR` | impairment factor GFR |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{HCT}}$ | `fimp_HCT` | impairment factor HCT |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{Mki}}$ | `fimp_Mki` | impairment factor Mki |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{albumin}}$ | `fimp_albumin` | impairment factor albumin |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{agp}}$ | `fimp_agp` | impairment factor agp |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{plasma\_protein}}$ | `fimp_plasma_protein` | impairment factor plasma\_protein |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{t\_stomach}}$ | `fimp_t_stomach` | impairment factor t\_stomach |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{t\_si}}$ | `fimp_t_si` | impairment factor t\_si |  | \- | ✓ |
| $\mathrm{fimp}_{\mathrm{ki\_slc22a6}}$ | `fimp_ki_slc22a6` | individual factor activity SLC22A6 kidney |  | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{ren}}$ | `Mr_ren` | molecular weight renin | $45057$ | g/mol | ✓ |
| $\mathrm{Mr}_{\mathrm{hctz}}$ | `Mr_hctz` | molecular weight hctz \[g/mole\] | $297.7$ | g/mol | ✓ |
| $\mathrm{fu}_{\mathrm{ref\_hctz}}$ | `fu_ref_hctz` | reference fraction unbound hctz | $1$ | \- | ✓ |
| $\mathrm{fu}_{\mathrm{hctz}}$ | `fu_hctz` | fraction unbound hctz |  | \- | ✓ |
| $f_{\mathrm{reabsorbed\_hctz}}$ | `f_reabsorbed_hctz` | fraction reabsorbed hctz | $0$ | \- | ✓ |
| $\mathrm{Kp}_{\mathrm{hctz}}$ | `Kp_hctz` | tissue to plasma coefficient hctz | $1.36015667679099$ | \- | ✓ |
| $\mathrm{ftissue}_{\mathrm{hctz}}$ | `ftissue_hctz` | whole-body exchange hctz \[l/min\] | $0.0317692988614749$ | l/min | ✓ |
| $\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}$ | `Vti_total_ref_hctz` | reference tissue volume of the organs hctz enters \[l\] | $35.5281724463884$ | l | ✓ |
| $\mathrm{BP}_{\mathrm{hctz}}$ | `BP_hctz` | blood to plasma ratio hctz | $1.7$ | \- | ✓ |
| $k_{\mathrm{bile}}$ | `k_bile` | transit bile to intestinal lumen \[1/min\] | $0.01$ | 1/min | ✓ |
| $\mathrm{ka}_{\mathrm{hctz}}$ | `ka_hctz` | absorption hctz \[1/hr\] | $0.307841020366845$ | 1/hr | ✓ |
| $\mathrm{FED}$ | `FED` | fed state (0 fasted, 1 fed) | $0$ | \- | ✓ |
| $\mathrm{IVDOSE}_{\mathrm{hctz}}$ | `IVDOSE_hctz` | intravenous dose hctz \[mg\] | $0$ | mg |  |
| $\mathrm{ti}_{\mathrm{hctz}}$ | `ti_hctz` | injection time hctz \[s\] | $10$ | s | ✓ |
| $\mathrm{Kiv}_{\mathrm{hctz}}$ | `Kiv_hctz` | injection rate hctz \[1/min\] |  | 1/min |  |
| $\mathrm{Ri}_{\mathrm{hctz}}$ | `Ri_hctz` | infusion rate hctz \[mg/min\] | $0$ | mg/min | ✓ |
| $\mathrm{PODOSE}_{\mathrm{hctz}}$ | `PODOSE_hctz` | oral dose hctz (tablet) \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{dis\_hctz}}$ | `Ka_dis_hctz` | dissolution rate hctz \[1/hr\] | $1.46649187054811$ | 1/hr | ✓ |
| $\mathrm{SOLDOSE}_{\mathrm{hctz}}$ | `SOLDOSE_hctz` | oral dose hctz (solution) \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{sol\_hctz}}$ | `Ka_sol_hctz` | application rate hctz (solution) \[1/hr\] | $60$ | 1/hr | ✓ |
| $w_{\mathrm{arm\_sk}}$ | `w_arm_sk` | weight of venous outflow of the skin in the arm vein | $0.7$ | \- | ✓ |
| $w_{\mathrm{arm\_mu}}$ | `w_arm_mu` | weight of venous outflow of the muscle in the arm vein | $0.3$ | \- | ✓ |
| $\mathrm{Car}_{\mathrm{free\_hctz}}$ | `Car_free_hctz` | unbound plasma concentration hctz arterial \[mM\] |  | mmol/l |  |
| $\mathrm{Car}_{\mathrm{blood\_hctz}}$ | `Car_blood_hctz` | blood concentration hctz arterial \[mM\] |  | mmol/l |  |
| $\mathrm{Cve}_{\mathrm{free\_hctz}}$ | `Cve_free_hctz` | unbound plasma concentration hctz venous \[mM\] |  | mmol/l |  |
| $\mathrm{Cve}_{\mathrm{blood\_hctz}}$ | `Cve_blood_hctz` | blood concentration hctz venous \[mM\] |  | mmol/l |  |
| $\mathrm{Cpo}_{\mathrm{free\_hctz}}$ | `Cpo_free_hctz` | unbound plasma concentration hctz portal \[mM\] |  | mmol/l |  |
| $\mathrm{Cpo}_{\mathrm{blood\_hctz}}$ | `Cpo_blood_hctz` | blood concentration hctz portal \[mM\] |  | mmol/l |  |
| $\mathrm{Chv}_{\mathrm{hctz}}$ | `Chv_hctz` | hepatic vein plasma concentration hctz \[mM\] |  | mmol/l |  |
| $\mathrm{Chv}_{\mathrm{free\_hctz}}$ | `Chv_free_hctz` | hepatic vein unbound plasma concentration hctz \[mM\] |  | mmol/l |  |
| $\mathrm{Chv}_{\mathrm{blood\_hctz}}$ | `Chv_blood_hctz` | hepatic vein blood concentration hctz \[mM\] |  | mmol/l |  |
| $\mathrm{Carm}_{\mathrm{hctz}}$ | `Carm_hctz` | arm vein plasma concentration hctz \[mM\] |  | mmol/l |  |
| $\mathrm{Carm}_{\mathrm{free\_hctz}}$ | `Carm_free_hctz` | arm vein unbound plasma concentration hctz \[mM\] |  | mmol/l |  |
| $\mathrm{Carm}_{\mathrm{blood\_hctz}}$ | `Carm_blood_hctz` | arm vein blood concentration hctz \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{lu\_hctz}}$ | `Cout_lu_hctz` | outflow plasma concentration hctz lung \[mM\] |  | mmol/l |  |
| $\mathrm{LU}_{\mathrm{\_PS\_hctz}}$ | `LU__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{LU}_{\mathrm{\_Cu\_ti\_hctz}}$ | `LU__Cu_ti_hctz` | unbound concentration hctz tissue lung \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{he\_hctz}}$ | `Cout_he_hctz` | outflow plasma concentration hctz heart \[mM\] |  | mmol/l |  |
| $\mathrm{HE}_{\mathrm{\_PS\_hctz}}$ | `HE__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{HE}_{\mathrm{\_Cu\_ti\_hctz}}$ | `HE__Cu_ti_hctz` | unbound concentration hctz tissue heart \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{br\_hctz}}$ | `Cout_br_hctz` | outflow plasma concentration hctz brain \[mM\] |  | mmol/l |  |
| $\mathrm{BR}_{\mathrm{\_PS\_hctz}}$ | `BR__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{BR}_{\mathrm{\_Cu\_ti\_hctz}}$ | `BR__Cu_ti_hctz` | unbound concentration hctz tissue brain \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{li\_hctz}}$ | `Cout_li_hctz` | outflow plasma concentration hctz liver \[mM\] |  | mmol/l |  |
| $\mathrm{LI}_{\mathrm{\_PS\_hctz}}$ | `LI__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_Cu\_ti\_hctz}}$ | `LI__Cu_ti_hctz` | unbound concentration hctz tissue liver \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{ki\_hctz}}$ | `Cout_ki_hctz` | outflow plasma concentration hctz kidney \[mM\] |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_f\_water\_int}}$ | `KI__f_water_int` | water fraction interstitial fluid | $0.93049$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_f\_water\_pls}}$ | `KI__f_water_pls` | water fraction plasma | $0.93049$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_r\_protein\_int\_pls}}$ | `KI__r_protein_int_pls` | protein of the interstitial fluid relative to plasma | $0.37$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_K\_int\_pls\_hctz}}$ | `KI__K_int_pls_hctz` | interstitial to plasma coefficient hctz |  | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_K\_cell\_pls\_hctz}}$ | `KI__K_cell_pls_hctz` | intracellular to plasma coefficient hctz |  | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_k\_vas}}$ | `KI__k_vas` | exchange plasma and interstitium per organ volume \[1/min\] | $1000$ | 1/min | ✓ |
| $\mathrm{KI}_{\mathrm{\_PS\_vas}}$ | `KI__PS_vas` | exchange plasma and interstitium \[l/min\] |  | l/min | ✓ |
| $\mathrm{KI}_{\mathrm{\_PS\_hctz}}$ | `KI__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{KI}_{\mathrm{\_Cu\_is\_hctz}}$ | `KI__Cu_is_hctz` | unbound concentration hctz interstitium kidney \[mM\] |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_Cu\_ic\_hctz}}$ | `KI__Cu_ic_hctz` | unbound concentration hctz intracellular space kidney \[mM\] |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_f\_slc22a6}}$ | `KI__f_slc22a6` | activity SLC22A6 | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_f\_abcc4}}$ | `KI__f_abcc4` | activity ABCC4 | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_f\_tubular}}$ | `KI__f_tubular` | share of the tubular capacity which follows the renal function | $1$ | \- | ✓ |
| $\mathrm{Rurine}_{\mathrm{hctz}}$ | `Rurine_hctz` | urinary excretion rate hctz \[mmole/min\] |  | mmol/min |  |
| $\mathrm{KI}_{\mathrm{\_HCTZUP\_k}}$ | `KI__HCTZUP_k` | clearance per volume HCTZUP \[1/min\] | $0.362349245398128$ | 1/min | ✓ |
| $\mathrm{KI}_{\mathrm{\_HCTZSEC\_k}}$ | `KI__HCTZSEC_k` | clearance HCTZSEC \[l/min\] | $10$ | l/min | ✓ |
| $\mathrm{Cout}_{\mathrm{st\_hctz}}$ | `Cout_st_hctz` | outflow plasma concentration hctz stomach \[mM\] |  | mmol/l |  |
| $\mathrm{ST}_{\mathrm{\_PS\_hctz}}$ | `ST__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{ST}_{\mathrm{\_Cu\_ti\_hctz}}$ | `ST__Cu_ti_hctz` | unbound concentration hctz tissue stomach \[mM\] |  | mmol/l |  |
| $\mathrm{GU}_{\mathrm{\_Vgu}}$ | `GU__Vgu` | volume intestine \[l\] |  | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_vas\_gu}}$ | `GU__f_vas_gu` | vascular fraction intestine |  | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_st}}$ | `GU__T_st` | transit time stomach \[min\] | $22.79$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_du}}$ | `GU__T_du` | transit time duodenum \[min\] | $14.3$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_du}}$ | `GU__f_area_du` | absorption area factor duodenum | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_jej1}}$ | `GU__T_jej1` | transit time upper jejunum \[min\] | $35.74$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_jej1}}$ | `GU__f_area_jej1` | absorption area factor upper jejunum | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_jej2}}$ | `GU__T_jej2` | transit time lower jejunum \[min\] | $35.74$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_jej2}}$ | `GU__f_area_jej2` | absorption area factor lower jejunum | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_ile1}}$ | `GU__T_ile1` | transit time upper ileum \[min\] | $53.11$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_ile1}}$ | `GU__f_area_ile1` | absorption area factor upper ileum | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_ile2}}$ | `GU__T_ile2` | transit time lower ileum \[min\] | $53.11$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_ile2}}$ | `GU__f_area_ile2` | absorption area factor lower ileum | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_cae}}$ | `GU__T_cae` | transit time caecum \[min\] | $339$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_cae}}$ | `GU__f_area_cae` | absorption area factor caecum | $0.0362$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_asc}}$ | `GU__T_asc` | transit time colon ascendens \[min\] | $339$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_asc}}$ | `GU__f_area_asc` | absorption area factor colon ascendens | $0.0362$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_tra}}$ | `GU__T_tra` | transit time colon transversum \[min\] | $342$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_tra}}$ | `GU__f_area_tra` | absorption area factor colon transversum | $0.0362$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_des}}$ | `GU__T_des` | transit time colon descendens \[min\] | $342$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_des}}$ | `GU__f_area_des` | absorption area factor colon descendens | $0.0362$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_sig}}$ | `GU__T_sig` | transit time colon sigmoid \[min\] | $372$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_sig}}$ | `GU__f_area_sig` | absorption area factor colon sigmoid | $0.0362$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_rec}}$ | `GU__T_rec` | transit time rectum \[min\] | $372$ | min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_area\_rec}}$ | `GU__f_area_rec` | absorption area factor rectum | $0.0362$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_T\_st\_fed}}$ | `GU__T_st_fed` | transit time stomach fed \[min\] | $63.48$ | min | ✓ |
| $\mathrm{Cout}_{\mathrm{si\_hctz}}$ | `Cout_si_hctz` | outflow plasma concentration hctz small intestine \[mM\] |  | mmol/l |  |
| $\mathrm{GU}_{\mathrm{\_Qgu}}$ | `GU__Qgu` | blood flow intestine \[l/min\] |  | l/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_PS\_hctz}}$ | `GU__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_Cu\_ti\_hctz}}$ | `GU__Cu_ti_hctz` | unbound concentration hctz tissue small intestine \[mM\] |  | mmol/l |  |
| $T_{\mathrm{st\_eff}}$ | `T_st_eff` | transit time stomach \[min\] |  | min | ✓ |
| $\mathrm{Cout}_{\mathrm{sp\_hctz}}$ | `Cout_sp_hctz` | outflow plasma concentration hctz spleen \[mM\] |  | mmol/l |  |
| $\mathrm{SP}_{\mathrm{\_PS\_hctz}}$ | `SP__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{SP}_{\mathrm{\_Cu\_ti\_hctz}}$ | `SP__Cu_ti_hctz` | unbound concentration hctz tissue spleen \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{pa\_hctz}}$ | `Cout_pa_hctz` | outflow plasma concentration hctz pancreas \[mM\] |  | mmol/l |  |
| $\mathrm{PA}_{\mathrm{\_PS\_hctz}}$ | `PA__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{PA}_{\mathrm{\_Cu\_ti\_hctz}}$ | `PA__Cu_ti_hctz` | unbound concentration hctz tissue pancreas \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{mu\_hctz}}$ | `Cout_mu_hctz` | outflow plasma concentration hctz muscle \[mM\] |  | mmol/l |  |
| $\mathrm{MU}_{\mathrm{\_kps\_hctz}}$ | `MU__kps_hctz` | exchange per volume plasma and tissue hctz \[1/min\] | $0.0215555200253895$ | 1/min | ✓ |
| $\mathrm{MU}_{\mathrm{\_PS\_hctz}}$ | `MU__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{MU}_{\mathrm{\_Cu\_ti\_hctz}}$ | `MU__Cu_ti_hctz` | unbound concentration hctz tissue muscle \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{sk\_hctz}}$ | `Cout_sk_hctz` | outflow plasma concentration hctz skin \[mM\] |  | mmol/l |  |
| $\mathrm{SK}_{\mathrm{\_PS\_hctz}}$ | `SK__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{SK}_{\mathrm{\_Cu\_ti\_hctz}}$ | `SK__Cu_ti_hctz` | unbound concentration hctz tissue skin \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{ad\_hctz}}$ | `Cout_ad_hctz` | outflow plasma concentration hctz adipose \[mM\] |  | mmol/l |  |
| $\mathrm{AD}_{\mathrm{\_PS\_hctz}}$ | `AD__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{AD}_{\mathrm{\_Cu\_ti\_hctz}}$ | `AD__Cu_ti_hctz` | unbound concentration hctz tissue adipose \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{bo\_hctz}}$ | `Cout_bo_hctz` | outflow plasma concentration hctz bone \[mM\] |  | mmol/l |  |
| $\mathrm{BO}_{\mathrm{\_PS\_hctz}}$ | `BO__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{BO}_{\mathrm{\_Cu\_ti\_hctz}}$ | `BO__Cu_ti_hctz` | unbound concentration hctz tissue bone \[mM\] |  | mmol/l |  |
| $\mathrm{Cout}_{\mathrm{go\_hctz}}$ | `Cout_go_hctz` | outflow plasma concentration hctz gonads \[mM\] |  | mmol/l |  |
| $\mathrm{GO}_{\mathrm{\_PS\_hctz}}$ | `GO__PS_hctz` | exchange plasma and tissue hctz \[l/min\] |  | l/min | ✓ |
| $\mathrm{GO}_{\mathrm{\_Cu\_ti\_hctz}}$ | `GO__Cu_ti_hctz` | unbound concentration hctz tissue gonads \[mM\] |  | mmol/l |  |
| $\mathrm{FLUID}_{\mathrm{\_GFR\_base}}$ | `FLUID__GFR_base` | glomerular filtration rate at renal function 1 |  | ml/min |  |
| $\mathrm{FLUID}_{\mathrm{\_f\_TBW}}$ | `FLUID__f_TBW` | Total body water (TBW) fraction of bodyweight | $0.55$ | l/kg | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_f\_ECF}}$ | `FLUID__f_ECF` | ECF fraction of TBW | $0.33$ | \- | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_ECF\_ref}}$ | `FLUID__ECF_ref` | Reference extracellular fluid volume (ECF) |  | l |  |
| $\mathrm{FLUID}_{\mathrm{\_Psys\_ref}}$ | `FLUID__Psys_ref` | Reference systolic blood pressure | $120$ | (133.322 N)/m<sup>2</sup> | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_Pdia\_ref}}$ | `FLUID__Pdia_ref` | Reference diastolic blood pressure | $80$ | (133.322 N)/m<sup>2</sup> | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_bp\_systolic}}$ | `FLUID__bp_systolic` | Systolic blood pressure |  | (133.322 N)/m<sup>2</sup> |  |
| $\mathrm{FLUID}_{\mathrm{\_bp\_diastolic}}$ | `FLUID__bp_diastolic` | Diastolic blood pressure |  | (133.322 N)/m<sup>2</sup> |  |
| $\mathrm{FLUID}_{\mathrm{\_bp\_mean}}$ | `FLUID__bp_mean` | Mean arterial pressure |  | (133.322 N)/m<sup>2</sup> |  |
| $\mathrm{FLUID}_{\mathrm{\_Mr\_nacl}}$ | `FLUID__Mr_nacl` | Molecular weight sodium chloride | $58.44$ | g/mol | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_Mr\_na}}$ | `FLUID__Mr_na` | Molecular weight sodium | $22.99$ | g/mol | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_Mr\_cl}}$ | `FLUID__Mr_cl` | Molecular weight chloride | $35.45$ | g/mol | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_vin\_na}}$ | `FLUID__vin_na` | Na uptake via food |  | mmol/min |  |
| $\mathrm{FLUID}_{\mathrm{\_vin\_cl}}$ | `FLUID__vin_cl` | Cl uptake via food |  | mmol/min |  |
| $\mathrm{FLUID}_{\mathrm{\_vin\_h2o}}$ | `FLUID__vin_h2o` | H2O uptake via food | $0.00159722222222222$ | l/min | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_vout\_h2o}}$ | `FLUID__vout_h2o` | H2O loss without urine | $0.000625$ | l/min | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_k\_na}}$ | `FLUID__k_na` |  | $0.00065800648455606$ | l/min | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_k\_cl}}$ | `FLUID__k_cl` |  | $0.00376049881572118$ | l/min | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_k\_h2o}}$ | `FLUID__k_h2o` |  | $\mathrm{NaN}$ | l/ml |  |
| $\mathrm{FLUID}_{\mathrm{\_h2o\_reabsorption}}$ | `FLUID__h2o_reabsorption` | H2O reabsorption from the renal tubule |  | l/min |  |
| $\mathrm{FLUID}_{\mathrm{\_diuresis}}$ | `FLUID__diuresis` |  |  | l/min |  |
| $\mathrm{FLUID}_{\mathrm{\_f\_h2o\_max}}$ | `FLUID__f_h2o_max` | maximal fractional excretion of water | $0.3$ | \- | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_counter\_gamma}}$ | `FLUID__counter_gamma` |  | $5$ | \- | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_E50\_hctz\_nacl}}$ | `FLUID__E50_hctz_nacl` |  | $7.47394627108756 \times 10^{-5}$ | mmol/l | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_Emax\_hctz\_na}}$ | `FLUID__Emax_hctz_na` |  | $1.82023051317122$ | \- | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_Emax\_hctz\_cl}}$ | `FLUID__Emax_hctz_cl` |  | $0.511521048025687$ | \- | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_f\_ECF\_start}}$ | `FLUID__f_ECF_start` | extracellular fluid at the start over its reference | $0.999840620430365$ | \- | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_na\_ref}}$ | `FLUID__na_ref` |  | $140$ | mmol/l | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_cl\_ref}}$ | `FLUID__cl_ref` |  | $102$ | mmol/l | ✓ |
| $\mathrm{FLUID}_{\mathrm{\_GFR}}$ | `FLUID__GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{FLUID}_{\mathrm{\_vout\_na}}$ | `FLUID__vout_na` |  |  | mg/min |  |
| $\mathrm{FLUID}_{\mathrm{\_vout\_cl}}$ | `FLUID__vout_cl` |  |  | mg/min |  |
| $\mathrm{FLUID}_{\mathrm{\_H2O\_UPTAKE}}$ | `FLUID__H2O_UPTAKE` |  |  | l/min |  |
| $\mathrm{FLUID}_{\mathrm{\_hctz\_urine\_excretion}}$ | `FLUID__hctz_urine_excretion` | HCTZ concentration in excreted urine |  | mmol/l |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{BSA}_{\mathrm{ref}} &= 0.007184 \cdot \mathopen{}\left(\frac{\mathrm{BW}_{\mathrm{ref}}}{1}\right)^{0.425} \cdot \mathopen{}\left(\frac{\mathrm{HEIGHT}_{\mathrm{ref}}}{1}\right)^{0.725} \\[1ex]
\mathrm{FFM}_{\mathrm{ref}} &= \frac{\mathrm{BW}_{\mathrm{ref}} \cdot 9270}{6680 + \frac{216 \cdot \frac{\mathrm{BW}_{\mathrm{ref}}}{1}}{\mathopen{}\left(\frac{\mathrm{HEIGHT}_{\mathrm{ref}}}{100}\right)^{2}}} \cdot \mathrm{fage}_{\mathrm{FFM}} \\[1ex]
\mathrm{HCT}_{\mathrm{ref}} &= 0.43 \cdot \mathrm{fage}_{\mathrm{HCT}} \\[1ex]
\mathrm{fage}_{\mathrm{Qrest}} &= \frac{1 - 0.129659643435981 \cdot \mathrm{fage}_{\mathrm{Qbr}}}{0.870340356564019} \\[1ex]
\mathrm{fage}_{\mathrm{Qother}} &= \frac{1 - 0.129659643435981 - 0.0702323068611561 \cdot \mathrm{fage}_{\mathrm{Qli}} - 0.0432198811453268 \cdot \mathrm{fage}_{\mathrm{Qli}} - 0.0108049702863317 \cdot \mathrm{fage}_{\mathrm{Qli}} - 0.108049702863317 \cdot \mathrm{fage}_{\mathrm{Qli}} - 0.0324149108589951 \cdot \mathrm{fage}_{\mathrm{Qli}} - 0.0108049702863317 \cdot \mathrm{fage}_{\mathrm{Qli}} - 0.205294435440303 \cdot \mathrm{fage}_{\mathrm{Qki}}}{0.389519178822258} \\[1ex]
\mathrm{fQhe} &= 0.0432198811453268 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qother}} \\[1ex]
\mathrm{fQbr} &= 0.129659643435981 \cdot \mathrm{fage}_{\mathrm{Qbr}} \\[1ex]
\mathrm{fQli} &= 0.0702323068611561 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qli}} \\[1ex]
\mathrm{fQki} &= 0.205294435440303 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qki}} \\[1ex]
\mathrm{fQst} &= 0.0108049702863317 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qli}} \\[1ex]
\mathrm{fQsi} &= 0.108049702863317 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qli}} \\[1ex]
\mathrm{fQla} &= 0.0432198811453268 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qli}} \\[1ex]
\mathrm{fQsp} &= 0.0324149108589951 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qli}} \\[1ex]
\mathrm{fQpa} &= 0.0108049702863317 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qli}} \\[1ex]
\mathrm{fQmu} &= 0.183684494867639 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qother}} \\[1ex]
\mathrm{fQsk} &= 0.0540248514316586 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qother}} \\[1ex]
\mathrm{fQad} &= 0.0540248514316586 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qother}} \\[1ex]
\mathrm{fQbo} &= 0.0540248514316586 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qother}} \\[1ex]
\mathrm{fQgo} &= 0.000540248514316586 \cdot \mathrm{fage}_{\mathrm{Qrest}} \cdot \mathrm{fage}_{\mathrm{Qother}} \\[1ex]
\mathrm{BMI} &= \frac{\frac{\mathrm{BW}}{1}}{\mathopen{}\left(\frac{\mathrm{HEIGHT}}{100}\right)^{2}} \cdot 1 \\[1ex]
\mathrm{BSA} &= 0.007184 \cdot \mathopen{}\left(\frac{\mathrm{BW}}{1}\right)^{0.425} \cdot \mathopen{}\left(\frac{\mathrm{HEIGHT}}{1}\right)^{0.725} \\[1ex]
\mathrm{FFM} &= \frac{\mathrm{BW} \cdot 9270}{6680 + \frac{216 \cdot \mathrm{BMI}}{1}} \cdot \mathrm{fage}_{\mathrm{FFM}} \\[1ex]
\mathrm{Mbr} &= \mathrm{Mbr}_{\mathrm{ref}} \\[1ex]
\mathrm{Msk} &= \frac{\mathrm{Msk}_{\mathrm{ref}} \cdot \mathrm{BSA}}{\mathrm{BSA}_{\mathrm{ref}}} \\[1ex]
\mathrm{SV}_{\mathrm{tis}} &= \frac{\mathrm{FFM} - \mathrm{Mbr} - \mathrm{Msk}}{\mathrm{FFM}_{\mathrm{ref}} - \mathrm{Mbr}_{\mathrm{ref}} - \mathrm{Msk}_{\mathrm{ref}}} \\[1ex]
\mathrm{Vblood} &= \mathrm{Vblood}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Mlu} &= \mathrm{Mlu}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Mhe} &= \mathrm{Mhe}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Mli} &= \mathrm{Mli}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Mst} &= \mathrm{Mst}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Msi} &= \mathrm{Msi}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Mla} &= \mathrm{Mla}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Msp} &= \mathrm{Msp}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Mpa} &= \mathrm{Mpa}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Mmu} &= \mathrm{Mmu}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Mbo} &= \mathrm{Mbo}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Mgo} &= \mathrm{Mgo}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \\[1ex]
\mathrm{Vlu} &= \frac{\mathrm{Mlu}}{1} + 0.125 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vhe} &= \frac{\mathrm{Mhe}}{1} + 0.01 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vbr} &= \frac{\mathrm{Mbr}}{1.04} + 0.012 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vli} &= \frac{\mathrm{Mli}}{1} + 0.1 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vst} &= \frac{\mathrm{Mst}}{1.045} + 0.01 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vsi} &= \frac{\mathrm{Msi}}{1.045} + 0.038 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vla} &= \frac{\mathrm{Mla}}{1.045} + 0.022 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vsp} &= \frac{\mathrm{Msp}}{1.06} + 0.014 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vpa} &= \frac{\mathrm{Mpa}}{1} + 0.006 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vmu} &= \frac{\mathrm{Mmu}}{1} + 0.14 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vsk} &= \frac{\mathrm{Msk}}{1.1} + 0.03 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vbo} &= \frac{\mathrm{Mbo}}{1.3} + 0.07 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vgo} &= \frac{\mathrm{Mgo}}{1.04} + 0.0004 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Var} &= \mathrm{fVar} \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Var}_{\mathrm{pl\_hctz}} &= \mathrm{Var} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
\mathrm{Vve} &= \mathrm{fVve} \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vve}_{\mathrm{pl\_hctz}} &= \mathrm{Vve} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
\mathrm{Vpo} &= \mathrm{fVpo} \cdot \mathrm{Vblood} \\[1ex]
\mathrm{Vpo}_{\mathrm{pl\_hctz}} &= \mathrm{Vpo} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{vas\_lu}} &= \frac{0.125 \cdot \mathrm{Vblood}}{\mathrm{Vlu}} \\[1ex]
\mathrm{LU}_{\mathrm{\_Vti}} &= \mathrm{Vlu} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_lu}}\right) \\[1ex]
\mathrm{LU}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vlu} \cdot f_{\mathrm{vas\_lu}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_lu}} &= 0.2 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_lu}}\right) \\[1ex]
f_{\mathrm{vas\_he}} &= \frac{0.01 \cdot \mathrm{Vblood}}{\mathrm{Vhe}} \\[1ex]
\mathrm{HE}_{\mathrm{\_Vti}} &= \mathrm{Vhe} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_he}}\right) \\[1ex]
\mathrm{HE}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vhe} \cdot f_{\mathrm{vas\_he}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_he}} &= 0.25 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_he}}\right) \\[1ex]
f_{\mathrm{vas\_br}} &= \frac{0.012 \cdot \mathrm{Vblood}}{\mathrm{Vbr}} \\[1ex]
\mathrm{BR}_{\mathrm{\_Vti}} &= \mathrm{Vbr} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_br}}\right) \\[1ex]
\mathrm{BR}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vbr} \cdot f_{\mathrm{vas\_br}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_br}} &= 0.00500015684306283 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_br}}\right) \\[1ex]
f_{\mathrm{vas\_li}} &= \frac{0.1 \cdot \mathrm{Vblood}}{\mathrm{Vli}} \\[1ex]
\mathrm{LI}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vli} \cdot f_{\mathrm{vas\_li}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_li}} &= 0.230032362459547 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_li}}\right) \\[1ex]
f_{\mathrm{vas\_st}} &= \frac{0.01 \cdot \mathrm{Vblood}}{\mathrm{Vst}} \\[1ex]
\mathrm{ST}_{\mathrm{\_Vti}} &= \mathrm{Vst} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_st}}\right) \\[1ex]
\mathrm{ST}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vst} \cdot f_{\mathrm{vas\_st}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_st}} &= 0.0960016431603451 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_st}}\right) \\[1ex]
f_{\mathrm{vas\_si}} &= \frac{0.038 \cdot \mathrm{Vblood}}{\mathrm{Vsi}} \\[1ex]
f_{\mathrm{int\_si}} &= 0.0960021180831348 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_si}}\right) \\[1ex]
f_{\mathrm{vas\_la}} &= \frac{0.022 \cdot \mathrm{Vblood}}{\mathrm{Vla}} \\[1ex]
f_{\mathrm{int\_la}} &= 0.0959989365944437 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_la}}\right) \\[1ex]
f_{\mathrm{vas\_sp}} &= \frac{0.014 \cdot \mathrm{Vblood}}{\mathrm{Vsp}} \\[1ex]
\mathrm{SP}_{\mathrm{\_Vti}} &= \mathrm{Vsp} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_sp}}\right) \\[1ex]
\mathrm{SP}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vsp} \cdot f_{\mathrm{vas\_sp}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_sp}} &= 0.255030487804878 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_sp}}\right) \\[1ex]
f_{\mathrm{vas\_pa}} &= \frac{0.006 \cdot \mathrm{Vblood}}{\mathrm{Vpa}} \\[1ex]
\mathrm{PA}_{\mathrm{\_Vti}} &= \mathrm{Vpa} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_pa}}\right) \\[1ex]
\mathrm{PA}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vpa} \cdot f_{\mathrm{vas\_pa}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_pa}} &= 0.095999509142226 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_pa}}\right) \\[1ex]
f_{\mathrm{vas\_mu}} &= \frac{0.14 \cdot \mathrm{Vblood}}{\mathrm{Vmu}} \\[1ex]
\mathrm{MU}_{\mathrm{\_Vti}} &= \mathrm{Vmu} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_mu}}\right) \\[1ex]
\mathrm{MU}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vmu} \cdot f_{\mathrm{vas\_mu}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_mu}} &= 0.150043587508333 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_mu}}\right) \\[1ex]
f_{\mathrm{vas\_sk}} &= \frac{0.03 \cdot \mathrm{Vblood}}{\mathrm{Vsk}} \\[1ex]
\mathrm{SK}_{\mathrm{\_Vti}} &= \mathrm{Vsk} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_sk}}\right) \\[1ex]
\mathrm{SK}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vsk} \cdot f_{\mathrm{vas\_sk}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_sk}} &= 0.599997894005286 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_sk}}\right) \\[1ex]
f_{\mathrm{vas\_bo}} &= \frac{0.07 \cdot \mathrm{Vblood}}{\mathrm{Vbo}} \\[1ex]
\mathrm{BO}_{\mathrm{\_Vti}} &= \mathrm{Vbo} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_bo}}\right) \\[1ex]
\mathrm{BO}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vbo} \cdot f_{\mathrm{vas\_bo}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_bo}} &= 0.100002091875157 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_bo}}\right) \\[1ex]
f_{\mathrm{vas\_go}} &= \frac{0.0004 \cdot \mathrm{Vblood}}{\mathrm{Vgo}} \\[1ex]
\mathrm{GO}_{\mathrm{\_Vti}} &= \mathrm{Vgo} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_go}}\right) \\[1ex]
\mathrm{GO}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vgo} \cdot f_{\mathrm{vas\_go}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_go}} &= 0.0959988944873185 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_go}}\right) \\[1ex]
\mathrm{CO}_{\mathrm{base}} &= \mathrm{CO}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \cdot f_{\mathrm{cardiac\_function}} \\[1ex]
\mathrm{fcp}_{\mathrm{functional\_liver}} &= \begin{cases} 1 & \text{if } \mathrm{CP}_{\mathrm{severity}} \leq 0 \\ 1 - 0.1018 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 1 \\ 0.8982 - 0.1128 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 2 \\ 0.7854 - 0.1199 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 3 \\ 0.6655 & \text{otherwise} \end{cases} \\[1ex]
f_{\mathrm{functional}} &= \mathrm{fcp}_{\mathrm{functional\_liver}} \\[1ex]
\mathrm{LI}_{\mathrm{\_Vti}} &= \mathrm{Vli} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_li}}\right) \cdot f_{\mathrm{functional}} \\[1ex]
\mathrm{fcp}_{\mathrm{hepatic\_artery\_flow}} &= \begin{cases} 1 & \text{if } \mathrm{CP}_{\mathrm{severity}} \leq 0 \\ 1 + 0.3 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 1 \\ 1.3 + 1 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 2 \\ 2.3 + 1.1 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 3 \\ 3.4 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fcp}_{\mathrm{kidney\_flow}} &= \begin{cases} 1 & \text{if } \mathrm{CP}_{\mathrm{severity}} \leq 0 \\ 1 - 0.12 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 1 \\ 0.88 - 0.23 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 2 \\ 0.65 - 0.17 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 3 \\ 0.48 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fcp}_{\mathrm{cardiac\_index}} &= \begin{cases} 1 & \text{if } \mathrm{CP}_{\mathrm{severity}} \leq 0 \\ 1 + 0.099 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 1 \\ 1.099 + 0.111 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 2 \\ 1.21 + 0.15 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 3 \\ 1.36 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fcp}_{\mathrm{gfr}} &= \begin{cases} 1 & \text{if } \mathrm{CP}_{\mathrm{severity}} \leq 0 \\ 1 + 0 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 1 \\ 1 - 0.3 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 2 \\ 0.7 - 0.34 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 3 \\ 0.36 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fcp}_{\mathrm{albumin}} &= \begin{cases} 1 & \text{if } \mathrm{CP}_{\mathrm{severity}} \leq 0 \\ 1 - 0.1355 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 1 \\ 0.8645 - 0.1847 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 2 \\ 0.6798 - 0.1906 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 3 \\ 0.4892 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fcp}_{\mathrm{agp}} &= \begin{cases} 1 & \text{if } \mathrm{CP}_{\mathrm{severity}} \leq 0 \\ 1 - 0.4 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 1 \\ 0.6 - 0.0399999999999999 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 2 \\ 0.56 - 0.26 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 3 \\ 0.3 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fcp}_{\mathrm{hematocrit}} &= \begin{cases} 1 & \text{if } \mathrm{CP}_{\mathrm{severity}} \leq 0 \\ 1 - 0.0768 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 1 \\ 0.9232 - 0.1821 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 2 \\ 0.7411 - 0.0179 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 3 \\ 0.7232 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fcp}_{\mathrm{shunt}} &= \begin{cases} 0 & \text{if } \mathrm{CP}_{\mathrm{severity}} \leq 0 \\ 0 + 0.399489795918367 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 1 \\ 0.399489795918367 + 0.298469387755102 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 2 \\ 0.697959183673469 + 0.114795918367347 \cdot \mathopen{}\left(\mathrm{CP}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{CP}_{\mathrm{severity}} < 3 \\ 0.812755102040816 & \text{otherwise} \end{cases} \\[1ex]
f_{\mathrm{shunt}} &= \mathrm{fcp}_{\mathrm{shunt}} \\[1ex]
\mathrm{fcp}_{\mathrm{rest\_flow}} &= 1 + \frac{\mathrm{fcp}_{\mathrm{cardiac\_index}} - 1 - \mathrm{fQli} \cdot \mathopen{}\left(\mathrm{fcp}_{\mathrm{hepatic\_artery\_flow}} - 1\right) - \mathrm{fQki} \cdot \mathopen{}\left(\mathrm{fcp}_{\mathrm{kidney\_flow}} - 1\right)}{\mathrm{fQhe} + \mathrm{fQmu} + \mathrm{fQsk} + \mathrm{fQad} + \mathrm{fQbo} + \mathrm{fQgo}} \\[1ex]
\mathrm{eGFR} &= 0.114467156025102 \cdot f_{\mathrm{renal\_function}} \\[1ex]
\mathrm{fckd}_{\mathrm{plasma\_protein}} &= \begin{cases} 1 & \text{if } \mathrm{eGFR} \geq 0.09 \\ 1 & \text{if } \mathrm{eGFR} \geq 0.075 \\ 1 + \frac{0.45 \cdot \mathopen{}\left(0.075 - \mathrm{eGFR}\right)}{0.03} & \text{if } \mathrm{eGFR} \geq 0.045 \\ 1.45 + \frac{0.75 \cdot \mathopen{}\left(0.045 - \mathrm{eGFR}\right)}{0.0225} & \text{if } \mathrm{eGFR} \geq 0.0225 \\ 2.2 + \frac{0.3 \cdot \mathopen{}\left(0.0225 - \mathrm{eGFR}\right)}{0.015} & \text{if } \mathrm{eGFR} \geq 0.0075 \\ 2.5 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fckd}_{\mathrm{hematocrit}} &= \begin{cases} 1 & \text{if } \mathrm{eGFR} \geq 0.09 \\ 1 + \frac{-0.0651 \cdot \mathopen{}\left(0.09 - \mathrm{eGFR}\right)}{0.015} & \text{if } \mathrm{eGFR} \geq 0.075 \\ 0.9349 + \frac{-0.0491999999999999 \cdot \mathopen{}\left(0.075 - \mathrm{eGFR}\right)}{0.03} & \text{if } \mathrm{eGFR} \geq 0.045 \\ 0.8857 + \frac{-0.0948 \cdot \mathopen{}\left(0.045 - \mathrm{eGFR}\right)}{0.0225} & \text{if } \mathrm{eGFR} \geq 0.0225 \\ 0.7909 + \frac{-0.0803 \cdot \mathopen{}\left(0.0225 - \mathrm{eGFR}\right)}{0.015} & \text{if } \mathrm{eGFR} \geq 0.0075 \\ 0.7106 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fckd}_{\mathrm{kidney\_volume}} &= \begin{cases} 1 & \text{if } \mathrm{eGFR} \geq 0.09 \\ 1 & \text{if } \mathrm{eGFR} \geq 0.075 \\ 1 & \text{if } \mathrm{eGFR} \geq 0.045 \\ 1 & \text{if } \mathrm{eGFR} \geq 0.0225 \\ 1 & \text{if } \mathrm{eGFR} \geq 0.0075 \\ 1 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fckd}_{\mathrm{kidney\_flow}} &= \begin{cases} 1 & \text{if } \mathrm{eGFR} \geq 0.09 \\ 1 + \frac{-0.2288 \cdot \mathopen{}\left(0.09 - \mathrm{eGFR}\right)}{0.015} & \text{if } \mathrm{eGFR} \geq 0.075 \\ 0.7712 + \frac{-0.2145 \cdot \mathopen{}\left(0.075 - \mathrm{eGFR}\right)}{0.03} & \text{if } \mathrm{eGFR} \geq 0.045 \\ 0.5567 + \frac{-0.1384 \cdot \mathopen{}\left(0.045 - \mathrm{eGFR}\right)}{0.0225} & \text{if } \mathrm{eGFR} \geq 0.0225 \\ 0.4183 + \frac{-0.0839 \cdot \mathopen{}\left(0.0225 - \mathrm{eGFR}\right)}{0.015} & \text{if } \mathrm{eGFR} \geq 0.0075 \\ 0.3344 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fckd}_{\mathrm{gastric\_emptying\_time}} &= \begin{cases} 1 & \text{if } \mathrm{eGFR} \geq 0.09 \\ 1 & \text{if } \mathrm{eGFR} \geq 0.075 \\ 1 & \text{if } \mathrm{eGFR} \geq 0.045 \\ 1 + \frac{0.6 \cdot \mathopen{}\left(0.045 - \mathrm{eGFR}\right)}{0.0225} & \text{if } \mathrm{eGFR} \geq 0.0225 \\ 1.6 & \text{if } \mathrm{eGFR} \geq 0.0075 \\ 1.6 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fckd}_{\mathrm{si\_transit\_time}} &= \begin{cases} 1 & \text{if } \mathrm{eGFR} \geq 0.09 \\ 1 & \text{if } \mathrm{eGFR} \geq 0.075 \\ 1 & \text{if } \mathrm{eGFR} \geq 0.045 \\ 1 + \frac{0.4 \cdot \mathopen{}\left(0.045 - \mathrm{eGFR}\right)}{0.0225} & \text{if } \mathrm{eGFR} \geq 0.0225 \\ 1.4 & \text{if } \mathrm{eGFR} \geq 0.0075 \\ 1.4 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fhf}_{\mathrm{liver\_flow}} &= \begin{cases} 1 & \text{if } \mathrm{HF}_{\mathrm{severity}} \leq 0 \\ 1 - 0.1272 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 1 \\ 0.8728 - 0.1272 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 2 \\ 0.7456 - 0.2189 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 3 \\ 0.5267 - 0.0604999999999999 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 3\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 4 \\ 0.4662 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fhf}_{\mathrm{kidney\_flow}} &= \begin{cases} 1 & \text{if } \mathrm{HF}_{\mathrm{severity}} \leq 0 \\ 1 - 0.1208 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 1 \\ 0.8792 - 0.1208 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 2 \\ 0.7584 - 0.2092 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 3 \\ 0.5492 + 0.0806 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 3\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 4 \\ 0.6298 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fhf}_{\mathrm{peripheral\_flow}} &= \begin{cases} 1 & \text{if } \mathrm{HF}_{\mathrm{severity}} \leq 0 \\ 1 - 0.1756 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 0\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 1 \\ 0.8244 - 0.1756 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 1\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 2 \\ 0.6488 - 0.0779000000000001 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 2\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 3 \\ 0.5709 - 0.1055 \cdot \mathopen{}\left(\mathrm{HF}_{\mathrm{severity}} - 3\right) & \text{if } \mathrm{HF}_{\mathrm{severity}} < 4 \\ 0.4654 & \text{otherwise} \end{cases} \\[1ex]
\mathrm{fimp}_{\mathrm{Qhe}} &= \mathrm{fcp}_{\mathrm{rest\_flow}} \\[1ex]
\mathrm{Qhe} &= \mathrm{fQhe} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qhe}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qbr}} &= 1 \\[1ex]
\mathrm{Qbr} &= \mathrm{fQbr} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qbr}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qli}} &= \mathrm{fcp}_{\mathrm{hepatic\_artery\_flow}} \cdot \mathrm{fhf}_{\mathrm{liver\_flow}} \\[1ex]
\mathrm{Qli} &= \mathrm{fQli} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qli}} \\[1ex]
\mathrm{Qha} &= \mathrm{Qli} \\[1ex]
\mathrm{fimp}_{\mathrm{Qki}} &= \mathrm{fcp}_{\mathrm{kidney\_flow}} \cdot \mathrm{fckd}_{\mathrm{kidney\_flow}} \cdot \mathrm{fhf}_{\mathrm{kidney\_flow}} \\[1ex]
\mathrm{Qki} &= \mathrm{fQki} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qki}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qst}} &= \mathrm{fhf}_{\mathrm{liver\_flow}} \\[1ex]
\mathrm{Qst} &= \mathrm{fQst} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qst}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qsi}} &= \mathrm{fhf}_{\mathrm{liver\_flow}} \\[1ex]
\mathrm{Qsi} &= \mathrm{fQsi} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qsi}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qla}} &= \mathrm{fhf}_{\mathrm{liver\_flow}} \\[1ex]
\mathrm{Qla} &= \mathrm{fQla} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qla}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qsp}} &= \mathrm{fhf}_{\mathrm{liver\_flow}} \\[1ex]
\mathrm{Qsp} &= \mathrm{fQsp} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qsp}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qpa}} &= \mathrm{fhf}_{\mathrm{liver\_flow}} \\[1ex]
\mathrm{Qpa} &= \mathrm{fQpa} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qpa}} \\[1ex]
\mathrm{Qpo} &= \mathrm{Qst} + \mathrm{Qsi} + \mathrm{Qla} + \mathrm{Qsp} \\
&\quad {} + \mathrm{Qpa} \\[1ex]
\mathrm{Qh} &= \mathrm{Qha} + \mathrm{Qpo} \\[1ex]
\mathrm{fimp}_{\mathrm{Qmu}} &= \mathrm{fcp}_{\mathrm{rest\_flow}} \cdot \mathrm{fhf}_{\mathrm{peripheral\_flow}} \\[1ex]
\mathrm{Qmu} &= \mathrm{fQmu} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qmu}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qsk}} &= \mathrm{fcp}_{\mathrm{rest\_flow}} \cdot \mathrm{fhf}_{\mathrm{peripheral\_flow}} \\[1ex]
\mathrm{Qsk} &= \mathrm{fQsk} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qsk}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qad}} &= \mathrm{fcp}_{\mathrm{rest\_flow}} \cdot \mathrm{fhf}_{\mathrm{peripheral\_flow}} \\[1ex]
\mathrm{Qad} &= \mathrm{fQad} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qad}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qbo}} &= \mathrm{fcp}_{\mathrm{rest\_flow}} \\[1ex]
\mathrm{Qbo} &= \mathrm{fQbo} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qbo}} \\[1ex]
\mathrm{fimp}_{\mathrm{Qgo}} &= \mathrm{fcp}_{\mathrm{rest\_flow}} \\[1ex]
\mathrm{Qgo} &= \mathrm{fQgo} \cdot \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{Qgo}} \\[1ex]
\mathrm{fimp}_{\mathrm{CO}} &= 1 + \mathrm{fQbr} \cdot \mathopen{}\left(\mathrm{fimp}_{\mathrm{Qbr}} - 1\right) + \mathrm{fQli} \cdot \mathopen{}\left(\mathrm{fimp}_{\mathrm{Qli}} - 1\right) + \mathrm{fQki} \cdot \mathopen{}\left(\mathrm{fimp}_{\mathrm{Qki}} - 1\right) \\
&\quad {} + \mathrm{fQst} \cdot \mathopen{}\left(\mathrm{fimp}_{\mathrm{Qst}} - 1\right) + \mathrm{fQsi} \cdot \mathopen{}\left(\mathrm{fimp}_{\mathrm{Qsi}} - 1\right) + \mathrm{fQla} \cdot \mathopen{}\left(\mathrm{fimp}_{\mathrm{Qla}} - 1\right) + \mathrm{fQsp} \cdot \mathopen{}\left(\mathrm{fimp}_{\mathrm{Qsp}} - 1\right) \\
&\quad {} + \mathrm{fQpa} \cdot \mathopen{}\left(\mathrm{fimp}_{\mathrm{Qpa}} - 1\right) + \mathopen{}\left(\mathrm{fQhe} + \mathrm{fQbo} + \mathrm{fQgo}\right) \cdot \mathopen{}\left(\mathrm{fcp}_{\mathrm{rest\_flow}} - 1\right) + \mathopen{}\left(\mathrm{fQmu} + \mathrm{fQsk} + \mathrm{fQad}\right) \cdot \mathopen{}\left(\mathrm{fcp}_{\mathrm{rest\_flow}} \cdot \mathrm{fhf}_{\mathrm{peripheral\_flow}} - 1\right) \\[1ex]
\mathrm{CO} &= \mathrm{CO}_{\mathrm{base}} \cdot \mathrm{fimp}_{\mathrm{CO}} \\[1ex]
\mathrm{Qlu} &= \mathrm{CO} \\[1ex]
\mathrm{fimp}_{\mathrm{GFR}} &= \mathrm{fcp}_{\mathrm{gfr}} \cdot \mathrm{fhf}_{\mathrm{kidney\_flow}} \\[1ex]
\mathrm{GFR}_{\mathrm{base}} &= \frac{\mathrm{GFR}_{\mathrm{ref}} \cdot \mathrm{BSA}}{1.88918819606715} \cdot \mathrm{fage}_{\mathrm{GFR}} \cdot \mathrm{fimp}_{\mathrm{GFR}} \\[1ex]
\mathrm{GFR} &= \mathrm{GFR}_{\mathrm{base}} \cdot f_{\mathrm{renal\_function}} \\[1ex]
\mathrm{fimp}_{\mathrm{HCT}} &= \mathrm{fcp}_{\mathrm{hematocrit}} \cdot \mathrm{fckd}_{\mathrm{hematocrit}} \\[1ex]
\mathrm{HCT} &= \mathrm{HCT}_{\mathrm{ref}} \cdot \mathrm{fimp}_{\mathrm{HCT}} \\[1ex]
\mathrm{Var}_{\mathrm{pl}} &= \mathrm{Var} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Var}_{\mathrm{bc}} &= \mathrm{Var} \cdot \mathrm{HCT} \\[1ex]
\mathrm{Vve}_{\mathrm{pl}} &= \mathrm{Vve} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vve}_{\mathrm{bc}} &= \mathrm{Vve} \cdot \mathrm{HCT} \\[1ex]
\mathrm{Vpo}_{\mathrm{pl}} &= \mathrm{Vpo} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vpo}_{\mathrm{bc}} &= \mathrm{Vpo} \cdot \mathrm{HCT} \\[1ex]
\mathrm{LU}_{\mathrm{\_Vpl}} &= \mathrm{Vlu} \cdot f_{\mathrm{vas\_lu}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{HE}_{\mathrm{\_Vpl}} &= \mathrm{Vhe} \cdot f_{\mathrm{vas\_he}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{BR}_{\mathrm{\_Vpl}} &= \mathrm{Vbr} \cdot f_{\mathrm{vas\_br}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{LI}_{\mathrm{\_Vpl}} &= \mathrm{Vli} \cdot f_{\mathrm{vas\_li}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{ST}_{\mathrm{\_Vpl}} &= \mathrm{Vst} \cdot f_{\mathrm{vas\_st}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{SP}_{\mathrm{\_Vpl}} &= \mathrm{Vsp} \cdot f_{\mathrm{vas\_sp}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{PA}_{\mathrm{\_Vpl}} &= \mathrm{Vpa} \cdot f_{\mathrm{vas\_pa}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{MU}_{\mathrm{\_Vpl}} &= \mathrm{Vmu} \cdot f_{\mathrm{vas\_mu}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{SK}_{\mathrm{\_Vpl}} &= \mathrm{Vsk} \cdot f_{\mathrm{vas\_sk}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{BO}_{\mathrm{\_Vpl}} &= \mathrm{Vbo} \cdot f_{\mathrm{vas\_bo}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{GO}_{\mathrm{\_Vpl}} &= \mathrm{Vgo} \cdot f_{\mathrm{vas\_go}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{fimp}_{\mathrm{Mki}} &= \mathrm{fckd}_{\mathrm{kidney\_volume}} \\[1ex]
\mathrm{Mki} &= \mathrm{Mki}_{\mathrm{ref}} \cdot \mathrm{SV}_{\mathrm{tis}} \cdot \mathrm{fimp}_{\mathrm{Mki}} \\[1ex]
\mathrm{Mlean} &= \mathrm{Mlu} + \mathrm{Mhe} + \mathrm{Mbr} + \mathrm{Mli} \\
&\quad {} + \mathrm{Mki} + \mathrm{Mst} + \mathrm{Msi} + \mathrm{Mla} \\
&\quad {} + \mathrm{Msp} + \mathrm{Mpa} + \mathrm{Mmu} + \mathrm{Msk} \\
&\quad {} + \mathrm{Mbo} + \mathrm{Mgo} \\[1ex]
\mathrm{Mad} &= \mathrm{BW} - \mathrm{Mlean} - \mathrm{Vblood} \cdot 1.06 \\[1ex]
\mathrm{Vki} &= \frac{\mathrm{Mki}}{1.05} + 0.02 \cdot \mathrm{Vblood} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_Vki}} &= \mathrm{Vki} \\[1ex]
\mathrm{Vad} &= \frac{\mathrm{Mad}}{1} + 0.05 \cdot \mathrm{Vblood} \\[1ex]
f_{\mathrm{vas\_ki}} &= \frac{0.02 \cdot \mathrm{Vblood}}{\mathrm{Vki}} \\[1ex]
\mathrm{KI}_{\mathrm{\_Vpl}} &= \mathrm{Vki} \cdot f_{\mathrm{vas\_ki}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{KI}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vki} \cdot f_{\mathrm{vas\_ki}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_ki}} &= 0.164990486545257 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_ki}}\right) \\[1ex]
\mathrm{KI}_{\mathrm{\_Vis}} &= \mathrm{Vki} \cdot f_{\mathrm{int\_ki}} \\[1ex]
\mathrm{KI}_{\mathrm{\_Vic}} &= \mathrm{Vki} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_ki}} - f_{\mathrm{int\_ki}}\right) \\[1ex]
f_{\mathrm{vas\_ad}} &= \frac{0.05 \cdot \mathrm{Vblood}}{\mathrm{Vad}} \\[1ex]
\mathrm{AD}_{\mathrm{\_Vpl}} &= \mathrm{Vad} \cdot f_{\mathrm{vas\_ad}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{AD}_{\mathrm{\_Vti}} &= \mathrm{Vad} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_ad}}\right) \\[1ex]
\mathrm{AD}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{Vad} \cdot f_{\mathrm{vas\_ad}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
f_{\mathrm{int\_ad}} &= 0.140013237615193 \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_ad}}\right) \\[1ex]
\mathrm{fimp}_{\mathrm{albumin}} &= \mathrm{fcp}_{\mathrm{albumin}} \\[1ex]
\mathrm{fimp}_{\mathrm{agp}} &= \mathrm{fcp}_{\mathrm{agp}} \\[1ex]
\mathrm{fimp}_{\mathrm{plasma\_protein}} &= \mathrm{fckd}_{\mathrm{plasma\_protein}} \\[1ex]
\mathrm{fimp}_{\mathrm{t\_stomach}} &= \mathrm{fckd}_{\mathrm{gastric\_emptying\_time}} \\[1ex]
\mathrm{fimp}_{\mathrm{t\_si}} &= \mathrm{fckd}_{\mathrm{si\_transit\_time}} \\[1ex]
\mathrm{fimp}_{\mathrm{ki\_slc22a6}} &= 1 \\[1ex]
\mathrm{fu}_{\mathrm{hctz}} &= \mathrm{fu}_{\mathrm{ref\_hctz}} \\[1ex]
\mathrm{LU}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vlu} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_lu}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{HE}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vhe} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_he}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{BR}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vbr} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_br}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vli} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_li}}\right) \cdot f_{\mathrm{functional}}}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{KI}_{\mathrm{\_K\_int\_pls\_hctz}} &= \mathopen{}\left(\mathrm{KI}_{\mathrm{\_f\_water\_int}} + \mathrm{KI}_{\mathrm{\_r\_protein\_int\_pls}} \cdot \mathopen{}\left(\frac{1}{\mathrm{fu}_{\mathrm{hctz}}} - \mathrm{KI}_{\mathrm{\_f\_water\_pls}}\right)\right) \cdot \mathrm{fu}_{\mathrm{hctz}} \\[1ex]
\mathrm{KI}_{\mathrm{\_K\_cell\_pls\_hctz}} &= \begin{cases} \frac{\mathrm{Kp}_{\mathrm{hctz}} \cdot \mathopen{}\left(f_{\mathrm{int\_ki}} + 1 - f_{\mathrm{vas\_ki}} - f_{\mathrm{int\_ki}}\right) - f_{\mathrm{int\_ki}} \cdot \mathrm{KI}_{\mathrm{\_K\_int\_pls\_hctz}}}{1 - f_{\mathrm{vas\_ki}} - f_{\mathrm{int\_ki}}} & \text{if } \frac{\mathrm{Kp}_{\mathrm{hctz}} \cdot \mathopen{}\left(f_{\mathrm{int\_ki}} + 1 - f_{\mathrm{vas\_ki}} - f_{\mathrm{int\_ki}}\right) - f_{\mathrm{int\_ki}} \cdot \mathrm{KI}_{\mathrm{\_K\_int\_pls\_hctz}}}{1 - f_{\mathrm{vas\_ki}} - f_{\mathrm{int\_ki}}} > 10^{-6} \\ 10^{-6} & \text{otherwise} \end{cases} \\[1ex]
\mathrm{KI}_{\mathrm{\_PS\_vas}} &= \mathrm{KI}_{\mathrm{\_k\_vas}} \cdot \mathrm{Vki} \\[1ex]
\mathrm{KI}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vki} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_ki}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{ST}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vst} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_st}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Vgu}} &= \mathrm{Vsi} + \mathrm{Vla} \\[1ex]
\mathrm{GU}_{\mathrm{\_f\_vas\_gu}} &= \frac{\mathrm{Vsi} \cdot f_{\mathrm{vas\_si}} + \mathrm{Vla} \cdot f_{\mathrm{vas\_la}}}{\mathrm{GU}_{\mathrm{\_Vgu}}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Vpl}} &= \mathrm{GU}_{\mathrm{\_Vgu}} \cdot \mathrm{GU}_{\mathrm{\_f\_vas\_gu}} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{GU}_{\mathrm{\_Vti}} &= \mathrm{GU}_{\mathrm{\_Vgu}} \cdot \mathopen{}\left(1 - \mathrm{GU}_{\mathrm{\_f\_vas\_gu}}\right) \\[1ex]
\mathrm{GU}_{\mathrm{\_Vpl\_hctz}} &= \mathrm{GU}_{\mathrm{\_Vgu}} \cdot \mathrm{GU}_{\mathrm{\_f\_vas\_gu}} \cdot \mathrm{BP}_{\mathrm{hctz}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Qgu}} &= \mathrm{Qsi} + \mathrm{Qla} \\[1ex]
\mathrm{GU}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{GU}_{\mathrm{\_Vgu}} \cdot \mathopen{}\left(1 - \mathrm{GU}_{\mathrm{\_f\_vas\_gu}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
T_{\mathrm{st\_eff}} &= \mathopen{}\left(\mathrm{GU}_{\mathrm{\_T\_st}} + \mathrm{FED} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_T\_st\_fed}} - \mathrm{GU}_{\mathrm{\_T\_st}}\right)\right) \cdot \mathrm{fimp}_{\mathrm{t\_stomach}} \\[1ex]
\mathrm{SP}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vsp} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_sp}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{PA}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vpa} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_pa}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{MU}_{\mathrm{\_PS\_hctz}} &= \mathrm{MU}_{\mathrm{\_kps\_hctz}} \cdot \mathrm{Vmu} \\[1ex]
\mathrm{SK}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vsk} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_sk}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{AD}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vad} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_ad}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{BO}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vbo} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_bo}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{GO}_{\mathrm{\_PS\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{Vgo} \cdot \mathopen{}\left(1 - f_{\mathrm{vas\_go}}\right)}{\mathrm{Vti}_{\mathrm{total\_ref\_hctz}}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_ECF}} &= \mathrm{FLUID}_{\mathrm{\_f\_ECF\_start}} \cdot \mathrm{FLUID}_{\mathrm{\_ECF\_ref}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_Vloop}} &= 0.05 \cdot \mathrm{FLUID}_{\mathrm{\_ECF\_ref}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_k\_h2o}} &= \frac{\mathrm{FLUID}_{\mathrm{\_vin\_h2o}} - \mathrm{FLUID}_{\mathrm{\_vout\_h2o}}}{\mathrm{FLUID}_{\mathrm{\_GFR\_base}}}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{Kiv}_{\mathrm{hctz}} &= \frac{\ln\mathopen{}\left(2\right)}{\mathrm{ti}_{\mathrm{hctz}}} \cdot 60 \\[1ex]
\mathrm{Car}_{\mathrm{free\_hctz}} &= \mathrm{fu}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
\mathrm{Car}_{\mathrm{blood\_hctz}} &= \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
\mathrm{Cve}_{\mathrm{free\_hctz}} &= \mathrm{fu}_{\mathrm{hctz}} \cdot \mathrm{Cve}_{\mathrm{hctz}} \\[1ex]
\mathrm{Cve}_{\mathrm{blood\_hctz}} &= \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cve}_{\mathrm{hctz}} \\[1ex]
\mathrm{Cpo}_{\mathrm{free\_hctz}} &= \mathrm{fu}_{\mathrm{hctz}} \cdot \mathrm{Cpo}_{\mathrm{hctz}} \\[1ex]
\mathrm{Cpo}_{\mathrm{blood\_hctz}} &= \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cpo}_{\mathrm{hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{lu\_hctz}} &= \mathrm{LU}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{LU}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{LU}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{he\_hctz}} &= \mathrm{HE}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{HE}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{HE}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{br\_hctz}} &= \mathrm{BR}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{BR}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{BR}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{li\_hctz}} &= \mathrm{LI}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{Chv}_{\mathrm{hctz}} &= \frac{\mathopen{}\left(1 - f_{\mathrm{shunt}}\right) \cdot \mathrm{Qh} \cdot \mathrm{Cout}_{\mathrm{li\_hctz}} + f_{\mathrm{shunt}} \cdot \mathopen{}\left(\mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{hctz}} + \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{hctz}}\right)}{\mathrm{Qh}} \\[1ex]
\mathrm{Chv}_{\mathrm{free\_hctz}} &= \mathrm{fu}_{\mathrm{hctz}} \cdot \mathrm{Chv}_{\mathrm{hctz}} \\[1ex]
\mathrm{Chv}_{\mathrm{blood\_hctz}} &= \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Chv}_{\mathrm{hctz}} \\[1ex]
\mathrm{LI}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{LI}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{ki\_hctz}} &= \mathrm{KI}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{KI}_{\mathrm{\_Cu\_is\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{KI}_{\mathrm{\_K\_int\_pls\_hctz}}} \cdot \mathrm{KI}_{\mathrm{\_Cis\_hctz}} \\[1ex]
\mathrm{KI}_{\mathrm{\_Cu\_ic\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{KI}_{\mathrm{\_K\_cell\_pls\_hctz}}} \cdot \mathrm{KI}_{\mathrm{\_Cic\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{st\_hctz}} &= \mathrm{ST}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{ST}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{ST}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{si\_hctz}} &= \mathrm{GU}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{GU}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{sp\_hctz}} &= \mathrm{SP}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{SP}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{SP}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{pa\_hctz}} &= \mathrm{PA}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{PA}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{PA}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{mu\_hctz}} &= \mathrm{MU}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{MU}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{MU}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{sk\_hctz}} &= \mathrm{SK}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{Carm}_{\mathrm{hctz}} &= w_{\mathrm{arm\_sk}} \cdot \mathrm{Cout}_{\mathrm{sk\_hctz}} + w_{\mathrm{arm\_mu}} \cdot \mathrm{Cout}_{\mathrm{mu\_hctz}} \\[1ex]
\mathrm{Carm}_{\mathrm{free\_hctz}} &= \mathrm{fu}_{\mathrm{hctz}} \cdot \mathrm{Carm}_{\mathrm{hctz}} \\[1ex]
\mathrm{Carm}_{\mathrm{blood\_hctz}} &= \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Carm}_{\mathrm{hctz}} \\[1ex]
\mathrm{SK}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{SK}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{ad\_hctz}} &= \mathrm{AD}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{AD}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{AD}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{bo\_hctz}} &= \mathrm{BO}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{BO}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{BO}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{Cout}_{\mathrm{go\_hctz}} &= \mathrm{GO}_{\mathrm{\_Cpl\_hctz}} \\[1ex]
\mathrm{GO}_{\mathrm{\_Cu\_ti\_hctz}} &= \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}} \cdot \mathrm{GO}_{\mathrm{\_Cti\_hctz}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_ECF\_ref}} &= \mathrm{FLUID}_{\mathrm{\_f\_ECF}} \cdot \mathrm{FLUID}_{\mathrm{\_f\_TBW}} \cdot \mathrm{BW} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_bp\_systolic}} &= \frac{\mathrm{FLUID}_{\mathrm{\_Psys\_ref}} \cdot \mathrm{FLUID}_{\mathrm{\_ECF}}}{\mathrm{FLUID}_{\mathrm{\_ECF\_ref}}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_bp\_diastolic}} &= \frac{\mathrm{FLUID}_{\mathrm{\_Pdia\_ref}} \cdot \mathrm{FLUID}_{\mathrm{\_ECF}}}{\mathrm{FLUID}_{\mathrm{\_ECF\_ref}}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_bp\_mean}} &= \frac{\mathrm{FLUID}_{\mathrm{\_bp\_systolic}} + 2 \cdot \mathrm{FLUID}_{\mathrm{\_bp\_diastolic}}}{3} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_vin\_na}} &= \mathrm{FLUID}_{\mathrm{\_k\_na}} \cdot \mathrm{FLUID}_{\mathrm{\_na\_ref}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_vin\_cl}} &= \mathrm{FLUID}_{\mathrm{\_k\_cl}} \cdot \mathrm{FLUID}_{\mathrm{\_cl\_ref}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_GFR}} &= \mathrm{GFR} \cdot 1000 \\[1ex]
\mathrm{FLUID}_{\mathrm{\_GFR\_base}} &= \mathrm{GFR}_{\mathrm{base}} \cdot 1000 \\[1ex]
\mathrm{FLUID}_{\mathrm{\_H2O\_UPTAKE}} &= \frac{\mathrm{FLUID}_{\mathrm{\_vin\_h2o}} \cdot \mathrm{FLUID}_{\mathrm{\_ECF\_ref}}^{\mathrm{FLUID}_{\mathrm{\_counter\_gamma}}}}{\mathrm{FLUID}_{\mathrm{\_ECF}}^{\mathrm{FLUID}_{\mathrm{\_counter\_gamma}}}} \\[1ex]
\mathrm{Rurine}_{\mathrm{hctz}} &= v_{\mathrm{KI\_\_J\_gfr\_hctz}} + v_{\mathrm{KI\_\_HCTZSEC}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_vout\_na}} &= v_{\mathrm{FLUID\_\_NA\_EXCRETION}} \cdot \mathrm{FLUID}_{\mathrm{\_Mr\_na}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_diuresis}} &= \min\mathopen{}\left(\frac{\frac{\mathrm{FLUID}_{\mathrm{\_k\_h2o}} \cdot \mathrm{FLUID}_{\mathrm{\_GFR}} \cdot \mathrm{FLUID}_{\mathrm{\_ECF}}^{\mathrm{FLUID}_{\mathrm{\_counter\_gamma}}}}{\mathrm{FLUID}_{\mathrm{\_ECF\_ref}}^{\mathrm{FLUID}_{\mathrm{\_counter\_gamma}}}} \cdot v_{\mathrm{FLUID\_\_NA\_EXCRETION}}}{\mathrm{FLUID}_{\mathrm{\_vin\_na}}}, \mathrm{FLUID}_{\mathrm{\_f\_h2o\_max}} \cdot \mathrm{FLUID}_{\mathrm{\_GFR}} \cdot 0.001\right) \\[1ex]
\mathrm{FLUID}_{\mathrm{\_h2o\_reabsorption}} &= \mathrm{FLUID}_{\mathrm{\_GFR}} \cdot 0.001 - \mathrm{FLUID}_{\mathrm{\_diuresis}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_hctz\_urine\_excretion}} &= \frac{\mathrm{Rurine}_{\mathrm{hctz}}}{\mathrm{FLUID}_{\mathrm{\_diuresis}}} \\[1ex]
\mathrm{FLUID}_{\mathrm{\_vout\_cl}} &= v_{\mathrm{FLUID\_\_CL\_EXCRETION}} \cdot \mathrm{FLUID}_{\mathrm{\_Mr\_cl}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $v_{\mathrm{J\_iv\_hctz}}$ | `J_iv_hctz` | intravenous application hctz | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{LU\_\_J\_in\_ve\_pl\_hctz}}$ | `LU__J_in_ve_pl_hctz` | inflow hctz from venous pool | $\mathrm{Cve}_{\mathrm{hctz}} \longrightarrow \mathrm{LU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{LU\_\_J\_out\_pl\_hctz}}$ | `LU__J_out_pl_hctz` | outflow hctz into arterial pool | $\mathrm{LU}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Car}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{LU\_\_J\_ti\_hctz}}$ | `LU__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{LU}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{LU}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{HE\_\_J\_in\_ar\_pl\_hctz}}$ | `HE__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{HE}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{HE\_\_J\_out\_pl\_hctz}}$ | `HE__J_out_pl_hctz` | outflow hctz into venous pool | $\mathrm{HE}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{HE\_\_J\_ti\_hctz}}$ | `HE__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{HE}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{HE}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{BR\_\_J\_in\_ar\_pl\_hctz}}$ | `BR__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{BR}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{BR\_\_J\_out\_pl\_hctz}}$ | `BR__J_out_pl_hctz` | outflow hctz into venous pool | $\mathrm{BR}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{BR\_\_J\_ti\_hctz}}$ | `BR__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{BR}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{BR}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{LI\_\_J\_in\_ar\_pl\_hctz}}$ | `LI__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{LI}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{LI\_\_J\_shunt\_ar\_pl\_hctz}}$ | `LI__J_shunt_ar_pl_hctz` | shunt hctz from arterial pool past the liver into venous pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{LI\_\_J\_in\_po\_pl\_hctz}}$ | `LI__J_in_po_pl_hctz` | inflow hctz from portal pool | $\mathrm{Cpo}_{\mathrm{hctz}} \longrightarrow \mathrm{LI}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{LI\_\_J\_shunt\_po\_pl\_hctz}}$ | `LI__J_shunt_po_pl_hctz` | shunt hctz from portal pool past the liver into venous pool | $\mathrm{Cpo}_{\mathrm{hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{LI\_\_J\_out\_pl\_hctz}}$ | `LI__J_out_pl_hctz` | outflow hctz into venous pool | $\mathrm{LI}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{LI\_\_J\_ti\_hctz}}$ | `LI__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{LI}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{LI}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{KI\_\_J\_in\_ar\_pl\_hctz}}$ | `KI__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{KI}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{KI\_\_J\_out\_pl\_hctz}}$ | `KI__J_out_pl_hctz` | outflow hctz into venous pool | $\mathrm{KI}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{KI\_\_J\_gfr\_hctz}}$ | `KI__J_gfr_hctz` | glomerular filtration hctz | $\mathrm{KI}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Aurine}_{\mathrm{hctz}}$ | $\mathrm{Car}_{\mathrm{hctz}}$ |
| $v_{\mathrm{KI\_\_J\_is\_hctz}}$ | `KI__J_is_hctz` | exchange hctz plasma and interstitium | $\mathrm{KI}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{KI}_{\mathrm{\_Cis\_hctz}}$ |  |
| $v_{\mathrm{KI\_\_J\_ic\_hctz}}$ | `KI__J_ic_hctz` | passive exchange hctz interstitium and cells | $\mathrm{KI}_{\mathrm{\_Cis\_hctz}} \rightleftharpoons \mathrm{KI}_{\mathrm{\_Cic\_hctz}}$ |  |
| $v_{\mathrm{KI\_\_HCTZUP}}$ | `KI__HCTZUP` | influx hctz basolateral (SLC22A6) | $\mathrm{KI}_{\mathrm{\_Cis\_hctz}} \longrightarrow \mathrm{KI}_{\mathrm{\_Cic\_hctz}}$ |  |
| $v_{\mathrm{KI\_\_HCTZSEC}}$ | `KI__HCTZSEC` | efflux hctz apical (ABCC4) | $\mathrm{KI}_{\mathrm{\_Cic\_hctz}} \longrightarrow \mathrm{Aurine}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{ST\_\_J\_in\_ar\_pl\_hctz}}$ | `ST__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{ST}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{ST\_\_J\_out\_pl\_hctz}}$ | `ST__J_out_pl_hctz` | outflow hctz into portal pool | $\mathrm{ST}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cpo}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{ST\_\_J\_ti\_hctz}}$ | `ST__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{ST}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{ST}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_in\_ar\_pl\_hctz}}$ | `GU__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_out\_pl\_hctz}}$ | `GU__J_out_pl_hctz` | outflow hctz into portal pool | $\mathrm{GU}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cpo}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_ti\_hctz}}$ | `GU__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{GU}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{GU}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_st\_hctz}}$ | `GU__J_tr_st_hctz` | transit hctz stomach | $\mathrm{GU}_{\mathrm{\_Clumen\_st\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_du\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_du\_hctz}}$ | `GU__J_tr_du_hctz` | transit hctz duodenum | $\mathrm{GU}_{\mathrm{\_Clumen\_du\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_jej1\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_du\_hctz}}$ | `GU__J_abs_du_hctz` | absorption hctz duodenum | $\mathrm{GU}_{\mathrm{\_Clumen\_du\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_jej1\_hctz}}$ | `GU__J_tr_jej1_hctz` | transit hctz upper jejunum | $\mathrm{GU}_{\mathrm{\_Clumen\_jej1\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_jej2\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_jej1\_hctz}}$ | `GU__J_abs_jej1_hctz` | absorption hctz upper jejunum | $\mathrm{GU}_{\mathrm{\_Clumen\_jej1\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_jej2\_hctz}}$ | `GU__J_tr_jej2_hctz` | transit hctz lower jejunum | $\mathrm{GU}_{\mathrm{\_Clumen\_jej2\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_ile1\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_jej2\_hctz}}$ | `GU__J_abs_jej2_hctz` | absorption hctz lower jejunum | $\mathrm{GU}_{\mathrm{\_Clumen\_jej2\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_ile1\_hctz}}$ | `GU__J_tr_ile1_hctz` | transit hctz upper ileum | $\mathrm{GU}_{\mathrm{\_Clumen\_ile1\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_ile2\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_ile1\_hctz}}$ | `GU__J_abs_ile1_hctz` | absorption hctz upper ileum | $\mathrm{GU}_{\mathrm{\_Clumen\_ile1\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_ile2\_hctz}}$ | `GU__J_tr_ile2_hctz` | transit hctz lower ileum | $\mathrm{GU}_{\mathrm{\_Clumen\_ile2\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_cae\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_ile2\_hctz}}$ | `GU__J_abs_ile2_hctz` | absorption hctz lower ileum | $\mathrm{GU}_{\mathrm{\_Clumen\_ile2\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_cae\_hctz}}$ | `GU__J_tr_cae_hctz` | transit hctz caecum | $\mathrm{GU}_{\mathrm{\_Clumen\_cae\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_asc\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_cae\_hctz}}$ | `GU__J_abs_cae_hctz` | absorption hctz caecum | $\mathrm{GU}_{\mathrm{\_Clumen\_cae\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_asc\_hctz}}$ | `GU__J_tr_asc_hctz` | transit hctz colon ascendens | $\mathrm{GU}_{\mathrm{\_Clumen\_asc\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_tra\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_asc\_hctz}}$ | `GU__J_abs_asc_hctz` | absorption hctz colon ascendens | $\mathrm{GU}_{\mathrm{\_Clumen\_asc\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_tra\_hctz}}$ | `GU__J_tr_tra_hctz` | transit hctz colon transversum | $\mathrm{GU}_{\mathrm{\_Clumen\_tra\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_des\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_tra\_hctz}}$ | `GU__J_abs_tra_hctz` | absorption hctz colon transversum | $\mathrm{GU}_{\mathrm{\_Clumen\_tra\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_des\_hctz}}$ | `GU__J_tr_des_hctz` | transit hctz colon descendens | $\mathrm{GU}_{\mathrm{\_Clumen\_des\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_sig\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_des\_hctz}}$ | `GU__J_abs_des_hctz` | absorption hctz colon descendens | $\mathrm{GU}_{\mathrm{\_Clumen\_des\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_sig\_hctz}}$ | `GU__J_tr_sig_hctz` | transit hctz colon sigmoid | $\mathrm{GU}_{\mathrm{\_Clumen\_sig\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_rec\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_sig\_hctz}}$ | `GU__J_abs_sig_hctz` | absorption hctz colon sigmoid | $\mathrm{GU}_{\mathrm{\_Clumen\_sig\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_tr\_rec\_hctz}}$ | `GU__J_tr_rec_hctz` | transit hctz rectum | $\mathrm{GU}_{\mathrm{\_Clumen\_rec\_hctz}} \longrightarrow \mathrm{Afeces}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_abs\_rec\_hctz}}$ | `GU__J_abs_rec_hctz` | absorption hctz rectum | $\mathrm{GU}_{\mathrm{\_Clumen\_rec\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_bile\_hctz}}$ | `GU__J_bile_hctz` | transit hctz bile to intestinal lumen | $\mathrm{Cbile}_{\mathrm{hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_du\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_po\_hctz}}$ | `GU__J_po_hctz` | dissolution hctz (tablet) stomach | $\varnothing \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_st\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_st\_hctz}}$ | `GU__J_trs_st_hctz` | transit hctz undissolved stomach | $\varnothing \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_du\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_du\_hctz}}$ | `GU__J_dis_du_hctz` | dissolution hctz duodenum | $\mathrm{GU}_{\mathrm{\_Asolid\_du\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_du\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_du\_hctz}}$ | `GU__J_trs_du_hctz` | transit hctz undissolved duodenum | $\mathrm{GU}_{\mathrm{\_Asolid\_du\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_jej1\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_jej1\_hctz}}$ | `GU__J_dis_jej1_hctz` | dissolution hctz upper jejunum | $\mathrm{GU}_{\mathrm{\_Asolid\_jej1\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_jej1\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_jej1\_hctz}}$ | `GU__J_trs_jej1_hctz` | transit hctz undissolved upper jejunum | $\mathrm{GU}_{\mathrm{\_Asolid\_jej1\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_jej2\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_jej2\_hctz}}$ | `GU__J_dis_jej2_hctz` | dissolution hctz lower jejunum | $\mathrm{GU}_{\mathrm{\_Asolid\_jej2\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_jej2\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_jej2\_hctz}}$ | `GU__J_trs_jej2_hctz` | transit hctz undissolved lower jejunum | $\mathrm{GU}_{\mathrm{\_Asolid\_jej2\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_ile1\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_ile1\_hctz}}$ | `GU__J_dis_ile1_hctz` | dissolution hctz upper ileum | $\mathrm{GU}_{\mathrm{\_Asolid\_ile1\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_ile1\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_ile1\_hctz}}$ | `GU__J_trs_ile1_hctz` | transit hctz undissolved upper ileum | $\mathrm{GU}_{\mathrm{\_Asolid\_ile1\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_ile2\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_ile2\_hctz}}$ | `GU__J_dis_ile2_hctz` | dissolution hctz lower ileum | $\mathrm{GU}_{\mathrm{\_Asolid\_ile2\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_ile2\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_ile2\_hctz}}$ | `GU__J_trs_ile2_hctz` | transit hctz undissolved lower ileum | $\mathrm{GU}_{\mathrm{\_Asolid\_ile2\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_cae\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_cae\_hctz}}$ | `GU__J_dis_cae_hctz` | dissolution hctz caecum | $\mathrm{GU}_{\mathrm{\_Asolid\_cae\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_cae\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_cae\_hctz}}$ | `GU__J_trs_cae_hctz` | transit hctz undissolved caecum | $\mathrm{GU}_{\mathrm{\_Asolid\_cae\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_asc\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_asc\_hctz}}$ | `GU__J_dis_asc_hctz` | dissolution hctz colon ascendens | $\mathrm{GU}_{\mathrm{\_Asolid\_asc\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_asc\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_asc\_hctz}}$ | `GU__J_trs_asc_hctz` | transit hctz undissolved colon ascendens | $\mathrm{GU}_{\mathrm{\_Asolid\_asc\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_tra\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_tra\_hctz}}$ | `GU__J_dis_tra_hctz` | dissolution hctz colon transversum | $\mathrm{GU}_{\mathrm{\_Asolid\_tra\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_tra\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_tra\_hctz}}$ | `GU__J_trs_tra_hctz` | transit hctz undissolved colon transversum | $\mathrm{GU}_{\mathrm{\_Asolid\_tra\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_des\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_des\_hctz}}$ | `GU__J_dis_des_hctz` | dissolution hctz colon descendens | $\mathrm{GU}_{\mathrm{\_Asolid\_des\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_des\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_des\_hctz}}$ | `GU__J_trs_des_hctz` | transit hctz undissolved colon descendens | $\mathrm{GU}_{\mathrm{\_Asolid\_des\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_sig\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_sig\_hctz}}$ | `GU__J_dis_sig_hctz` | dissolution hctz colon sigmoid | $\mathrm{GU}_{\mathrm{\_Asolid\_sig\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_sig\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_sig\_hctz}}$ | `GU__J_trs_sig_hctz` | transit hctz undissolved colon sigmoid | $\mathrm{GU}_{\mathrm{\_Asolid\_sig\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Asolid\_rec\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_dis\_rec\_hctz}}$ | `GU__J_dis_rec_hctz` | dissolution hctz rectum | $\mathrm{GU}_{\mathrm{\_Asolid\_rec\_hctz}} \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_rec\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_trs\_rec\_hctz}}$ | `GU__J_trs_rec_hctz` | transit hctz undissolved rectum | $\mathrm{GU}_{\mathrm{\_Asolid\_rec\_hctz}} \longrightarrow \mathrm{Afeces}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{GU\_\_J\_sol\_hctz}}$ | `GU__J_sol_hctz` | oral application hctz (solution) | $\varnothing \longrightarrow \mathrm{GU}_{\mathrm{\_Clumen\_st\_hctz}}$ |  |
| $v_{\mathrm{SP\_\_J\_in\_ar\_pl\_hctz}}$ | `SP__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{SP}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{SP\_\_J\_out\_pl\_hctz}}$ | `SP__J_out_pl_hctz` | outflow hctz into portal pool | $\mathrm{SP}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cpo}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{SP\_\_J\_ti\_hctz}}$ | `SP__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{SP}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{SP}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{PA\_\_J\_in\_ar\_pl\_hctz}}$ | `PA__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{PA}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{PA\_\_J\_out\_pl\_hctz}}$ | `PA__J_out_pl_hctz` | outflow hctz into portal pool | $\mathrm{PA}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cpo}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{PA\_\_J\_ti\_hctz}}$ | `PA__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{PA}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{PA}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{MU\_\_J\_in\_ar\_pl\_hctz}}$ | `MU__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{MU}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{MU\_\_J\_out\_pl\_hctz}}$ | `MU__J_out_pl_hctz` | outflow hctz into venous pool | $\mathrm{MU}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{MU\_\_J\_ti\_hctz}}$ | `MU__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{MU}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{MU}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{SK\_\_J\_in\_ar\_pl\_hctz}}$ | `SK__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{SK}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{SK\_\_J\_out\_pl\_hctz}}$ | `SK__J_out_pl_hctz` | outflow hctz into venous pool | $\mathrm{SK}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{SK\_\_J\_ti\_hctz}}$ | `SK__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{SK}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{SK}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{AD\_\_J\_in\_ar\_pl\_hctz}}$ | `AD__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{AD}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{AD\_\_J\_out\_pl\_hctz}}$ | `AD__J_out_pl_hctz` | outflow hctz into venous pool | $\mathrm{AD}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{AD\_\_J\_ti\_hctz}}$ | `AD__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{AD}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{AD}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{BO\_\_J\_in\_ar\_pl\_hctz}}$ | `BO__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{BO}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{BO\_\_J\_out\_pl\_hctz}}$ | `BO__J_out_pl_hctz` | outflow hctz into venous pool | $\mathrm{BO}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{BO\_\_J\_ti\_hctz}}$ | `BO__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{BO}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{BO}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{GO\_\_J\_in\_ar\_pl\_hctz}}$ | `GO__J_in_ar_pl_hctz` | inflow hctz from arterial pool | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{GO}_{\mathrm{\_Cpl\_hctz}}$ |  |
| $v_{\mathrm{GO\_\_J\_out\_pl\_hctz}}$ | `GO__J_out_pl_hctz` | outflow hctz into venous pool | $\mathrm{GO}_{\mathrm{\_Cpl\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{GO\_\_J\_ti\_hctz}}$ | `GO__J_ti_hctz` | exchange hctz plasma and tissue | $\mathrm{GO}_{\mathrm{\_Cpl\_hctz}} \rightleftharpoons \mathrm{GO}_{\mathrm{\_Cti\_hctz}}$ |  |
| $v_{\mathrm{FLUID\_\_NA\_UPTAKE}}$ | `FLUID__NA_UPTAKE` | Na uptake via food | $\varnothing \longrightarrow \mathrm{FLUID}_{\mathrm{\_na}}$ |  |
| $v_{\mathrm{FLUID\_\_CL\_UPTAKE}}$ | `FLUID__CL_UPTAKE` | Cl uptake via food | $\varnothing \longrightarrow \mathrm{FLUID}_{\mathrm{\_cl}}$ |  |
| $v_{\mathrm{FLUID\_\_NA\_FILTRATION}}$ | `FLUID__NA_FILTRATION` | Na filtration kidney | $\mathrm{FLUID}_{\mathrm{\_na}} \longrightarrow \mathrm{FLUID}_{\mathrm{\_na\_loop}}$ |  |
| $v_{\mathrm{FLUID\_\_NA\_EXCRETION}}$ | `FLUID__NA_EXCRETION` | Na excretion urine | $\mathrm{FLUID}_{\mathrm{\_na\_loop}} \longrightarrow \mathrm{FLUID}_{\mathrm{\_na\_urine}}$ |  |
| $v_{\mathrm{FLUID\_\_NA\_REABSORPTION}}$ | `FLUID__NA_REABSORPTION` | Na reabsorption kidney | $\mathrm{FLUID}_{\mathrm{\_na\_loop}} \longrightarrow \mathrm{FLUID}_{\mathrm{\_na}}$ |  |
| $v_{\mathrm{FLUID\_\_CL\_FILTRATION}}$ | `FLUID__CL_FILTRATION` | Cl filtration kidney | $\mathrm{FLUID}_{\mathrm{\_cl}} \longrightarrow \mathrm{FLUID}_{\mathrm{\_cl\_loop}}$ |  |
| $v_{\mathrm{FLUID\_\_CL\_EXCRETION}}$ | `FLUID__CL_EXCRETION` | Cl excretion urine | $\mathrm{FLUID}_{\mathrm{\_cl\_loop}} \longrightarrow \mathrm{FLUID}_{\mathrm{\_cl\_urine}}$ |  |
| $v_{\mathrm{FLUID\_\_CL\_REABSORPTION}}$ | `FLUID__CL_REABSORPTION` | Cl reabsorption kidney | $\mathrm{FLUID}_{\mathrm{\_cl\_loop}} \longrightarrow \mathrm{FLUID}_{\mathrm{\_cl}}$ |  |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{J\_iv\_hctz}} &= \frac{\mathrm{Kiv}_{\mathrm{hctz}} \cdot \mathrm{IVDOSE}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}} \\[1ex]
v_{\mathrm{LU\_\_J\_in\_ve\_pl\_hctz}} &= \mathrm{Qlu} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cve}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{LU\_\_J\_out\_pl\_hctz}} &= \mathrm{Qlu} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{lu\_hctz}} \\[1ex]
v_{\mathrm{LU\_\_J\_ti\_hctz}} &= \mathrm{LU}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{LU}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{LU}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{HE\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qhe} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{HE\_\_J\_out\_pl\_hctz}} &= \mathrm{Qhe} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{he\_hctz}} \\[1ex]
v_{\mathrm{HE\_\_J\_ti\_hctz}} &= \mathrm{HE}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{HE}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{HE}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{BR\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qbr} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{BR\_\_J\_out\_pl\_hctz}} &= \mathrm{Qbr} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{br\_hctz}} \\[1ex]
v_{\mathrm{BR\_\_J\_ti\_hctz}} &= \mathrm{BR}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{BR}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{BR}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{LI\_\_J\_in\_ar\_pl\_hctz}} &= \mathopen{}\left(1 - f_{\mathrm{shunt}}\right) \cdot \mathrm{Qha} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{LI\_\_J\_shunt\_ar\_pl\_hctz}} &= f_{\mathrm{shunt}} \cdot \mathrm{Qha} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{LI\_\_J\_in\_po\_pl\_hctz}} &= \mathopen{}\left(1 - f_{\mathrm{shunt}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cpo}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{LI\_\_J\_shunt\_po\_pl\_hctz}} &= f_{\mathrm{shunt}} \cdot \mathrm{Qpo} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cpo}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{LI\_\_J\_out\_pl\_hctz}} &= \mathopen{}\left(1 - f_{\mathrm{shunt}}\right) \cdot \mathrm{Qh} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{li\_hctz}} \\[1ex]
v_{\mathrm{LI\_\_J\_ti\_hctz}} &= \mathrm{LI}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{LI}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{LI}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{KI\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qki} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{KI\_\_J\_out\_pl\_hctz}} &= \mathrm{Qki} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{ki\_hctz}} - \mathrm{fu}_{\mathrm{hctz}} \cdot \mathrm{GFR} \cdot \mathrm{Cout}_{\mathrm{ki\_hctz}} \cdot \mathopen{}\left(1 - f_{\mathrm{reabsorbed\_hctz}}\right) \\[1ex]
v_{\mathrm{KI\_\_J\_gfr\_hctz}} &= \mathrm{fu}_{\mathrm{hctz}} \cdot \mathrm{GFR} \cdot \mathrm{Car}_{\mathrm{hctz}} \cdot \mathopen{}\left(1 - f_{\mathrm{reabsorbed\_hctz}}\right) \\[1ex]
v_{\mathrm{KI\_\_J\_is\_hctz}} &= \mathrm{KI}_{\mathrm{\_PS\_vas}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{KI}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{KI}_{\mathrm{\_Cis\_hctz}}}{\mathrm{KI}_{\mathrm{\_K\_int\_pls\_hctz}}}\right) \\[1ex]
v_{\mathrm{KI\_\_J\_ic\_hctz}} &= \mathrm{KI}_{\mathrm{\_PS\_hctz}} \cdot \mathopen{}\left(\frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{KI}_{\mathrm{\_K\_int\_pls\_hctz}}} \cdot \mathrm{KI}_{\mathrm{\_Cis\_hctz}} - \frac{\mathrm{fu}_{\mathrm{hctz}}}{\mathrm{KI}_{\mathrm{\_K\_cell\_pls\_hctz}}} \cdot \mathrm{KI}_{\mathrm{\_Cic\_hctz}}\right) \\[1ex]
v_{\mathrm{KI\_\_HCTZUP}} &= \frac{\mathrm{KI}_{\mathrm{\_f\_slc22a6}} \cdot \mathrm{fimp}_{\mathrm{ki\_slc22a6}} \cdot \mathopen{}\left(1 - \mathrm{KI}_{\mathrm{\_f\_tubular}} + \mathrm{KI}_{\mathrm{\_f\_tubular}} \cdot f_{\mathrm{renal\_function}}\right) \cdot \mathrm{KI}_{\mathrm{\_HCTZUP\_k}} \cdot \mathrm{Vki} \cdot \mathrm{fu}_{\mathrm{hctz}}}{\mathrm{KI}_{\mathrm{\_K\_int\_pls\_hctz}}} \cdot \mathrm{KI}_{\mathrm{\_Cis\_hctz}} \\[1ex]
v_{\mathrm{KI\_\_HCTZSEC}} &= \frac{\mathrm{KI}_{\mathrm{\_f\_abcc4}} \cdot \mathopen{}\left(1 - \mathrm{KI}_{\mathrm{\_f\_tubular}} + \mathrm{KI}_{\mathrm{\_f\_tubular}} \cdot f_{\mathrm{renal\_function}}\right) \cdot \mathrm{KI}_{\mathrm{\_HCTZSEC\_k}} \cdot \mathrm{fu}_{\mathrm{hctz}}}{\mathrm{KI}_{\mathrm{\_K\_cell\_pls\_hctz}}} \cdot \mathrm{KI}_{\mathrm{\_Cic\_hctz}} \\[1ex]
v_{\mathrm{ST\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qst} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{ST\_\_J\_out\_pl\_hctz}} &= \mathrm{Qst} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{st\_hctz}} \\[1ex]
v_{\mathrm{ST\_\_J\_ti\_hctz}} &= \mathrm{ST}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{ST}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{ST}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{GU\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{GU}_{\mathrm{\_Qgu}} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_out\_pl\_hctz}} &= \mathrm{GU}_{\mathrm{\_Qgu}} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{si\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_ti\_hctz}} &= \mathrm{GU}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{GU}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_st\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_st}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_st\_hctz}}}{\mathopen{}\left(\mathrm{GU}_{\mathrm{\_T\_st}} + \mathrm{FED} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_T\_st\_fed}} - \mathrm{GU}_{\mathrm{\_T\_st}}\right)\right) \cdot \mathrm{fimp}_{\mathrm{t\_stomach}}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_du\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_du}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_du\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_du}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_du\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_du}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_du}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_du\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_jej1\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_jej1}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_jej1\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_jej1}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_jej1\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_jej1}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_jej1}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_jej1\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_jej2\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_jej2}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_jej2\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_jej2}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_jej2\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_jej2}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_jej2}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_jej2\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_ile1\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_ile1}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_ile1\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_ile1}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_ile1\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_ile1}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_ile1}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_ile1\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_ile2\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_ile2}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_ile2\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_ile2}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_ile2\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_ile2}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_ile2}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_ile2\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_cae\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_cae}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_cae\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_cae}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_cae\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_cae}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_cae}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_cae\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_asc\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_asc}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_asc\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_asc}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_asc\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_asc}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_asc}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_asc\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_tra\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_tra}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_tra\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_tra}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_tra\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_tra}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_tra}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_tra\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_des\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_des}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_des\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_des}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_des\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_des}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_des}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_des\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_sig\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_sig}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_sig\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_sig}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_sig\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_sig}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_sig}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_sig\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_tr\_rec\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Vlumen\_rec}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_rec\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_rec}}} \\[1ex]
v_{\mathrm{GU\_\_J\_abs\_rec\_hctz}} &= \frac{\mathrm{ka}_{\mathrm{hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_f\_area\_rec}} \cdot \mathrm{GU}_{\mathrm{\_Vlumen\_rec}} \cdot \mathrm{GU}_{\mathrm{\_Clumen\_rec\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_bile\_hctz}} &= k_{\mathrm{bile}} \cdot \mathrm{Vbile} \cdot \mathrm{Cbile}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_po\_hctz}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_st\_hctz}} &= \frac{\frac{\mathrm{PODOSE}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}}}{\mathopen{}\left(\mathrm{GU}_{\mathrm{\_T\_st}} + \mathrm{FED} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_T\_st\_fed}} - \mathrm{GU}_{\mathrm{\_T\_st}}\right)\right) \cdot \mathrm{fimp}_{\mathrm{t\_stomach}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_du\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_du\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_du\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_du\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_du}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_jej1\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_jej1\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_jej1\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_jej1\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_jej1}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_jej2\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_jej2\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_jej2\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_jej2\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_jej2}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_ile1\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_ile1\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_ile1\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_ile1\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_ile1}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_ile2\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_ile2\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_ile2\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_ile2\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_ile2}} \cdot \mathrm{fimp}_{\mathrm{t\_si}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_cae\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_cae\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_cae\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_cae\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_cae}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_asc\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_asc\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_asc\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_asc\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_asc}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_tra\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_tra\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_tra\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_tra\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_tra}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_des\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_des\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_des\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_des\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_des}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_sig\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_sig\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_sig\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_sig\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_sig}}} \\[1ex]
v_{\mathrm{GU\_\_J\_dis\_rec\_hctz}} &= \frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_Asolid\_rec\_hctz}} \\[1ex]
v_{\mathrm{GU\_\_J\_trs\_rec\_hctz}} &= \frac{\mathrm{GU}_{\mathrm{\_Asolid\_rec\_hctz}}}{\mathrm{GU}_{\mathrm{\_T\_rec}}} \\[1ex]
v_{\mathrm{GU\_\_J\_sol\_hctz}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{sol\_hctz}}}{60} \cdot \mathrm{SOLDOSE}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}} \\[1ex]
v_{\mathrm{SP\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qsp} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{SP\_\_J\_out\_pl\_hctz}} &= \mathrm{Qsp} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{sp\_hctz}} \\[1ex]
v_{\mathrm{SP\_\_J\_ti\_hctz}} &= \mathrm{SP}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{SP}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{SP}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{PA\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qpa} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{PA\_\_J\_out\_pl\_hctz}} &= \mathrm{Qpa} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{pa\_hctz}} \\[1ex]
v_{\mathrm{PA\_\_J\_ti\_hctz}} &= \mathrm{PA}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{PA}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{PA}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{MU\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qmu} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{MU\_\_J\_out\_pl\_hctz}} &= \mathrm{Qmu} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{mu\_hctz}} \\[1ex]
v_{\mathrm{MU\_\_J\_ti\_hctz}} &= \mathrm{MU}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{MU}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{MU}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{SK\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qsk} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{SK\_\_J\_out\_pl\_hctz}} &= \mathrm{Qsk} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{sk\_hctz}} \\[1ex]
v_{\mathrm{SK\_\_J\_ti\_hctz}} &= \mathrm{SK}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{SK}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{SK}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{AD\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qad} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{AD\_\_J\_out\_pl\_hctz}} &= \mathrm{Qad} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{ad\_hctz}} \\[1ex]
v_{\mathrm{AD\_\_J\_ti\_hctz}} &= \mathrm{AD}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{AD}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{AD}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{BO\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qbo} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{BO\_\_J\_out\_pl\_hctz}} &= \mathrm{Qbo} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{bo\_hctz}} \\[1ex]
v_{\mathrm{BO\_\_J\_ti\_hctz}} &= \mathrm{BO}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{BO}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{BO}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{GO\_\_J\_in\_ar\_pl\_hctz}} &= \mathrm{Qgo} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{GO\_\_J\_out\_pl\_hctz}} &= \mathrm{Qgo} \cdot \mathrm{BP}_{\mathrm{hctz}} \cdot \mathrm{Cout}_{\mathrm{go\_hctz}} \\[1ex]
v_{\mathrm{GO\_\_J\_ti\_hctz}} &= \mathrm{GO}_{\mathrm{\_PS\_hctz}} \cdot \mathrm{fu}_{\mathrm{hctz}} \cdot \mathopen{}\left(\mathrm{GO}_{\mathrm{\_Cpl\_hctz}} - \frac{\mathrm{GO}_{\mathrm{\_Cti\_hctz}}}{\mathrm{Kp}_{\mathrm{hctz}}}\right) \\[1ex]
v_{\mathrm{FLUID\_\_NA\_UPTAKE}} &= \frac{\mathrm{FLUID}_{\mathrm{\_vin\_na}} \cdot \mathrm{FLUID}_{\mathrm{\_na\_ref}}^{\mathrm{FLUID}_{\mathrm{\_counter\_gamma}}}}{\mathrm{FLUID}_{\mathrm{\_na}}^{\mathrm{FLUID}_{\mathrm{\_counter\_gamma}}}} \\[1ex]
v_{\mathrm{FLUID\_\_CL\_UPTAKE}} &= \frac{\mathrm{FLUID}_{\mathrm{\_vin\_cl}} \cdot \mathrm{FLUID}_{\mathrm{\_cl\_ref}}^{\mathrm{FLUID}_{\mathrm{\_counter\_gamma}}}}{\mathrm{FLUID}_{\mathrm{\_cl}}^{\mathrm{FLUID}_{\mathrm{\_counter\_gamma}}}} \\[1ex]
v_{\mathrm{FLUID\_\_NA\_FILTRATION}} &= \mathrm{FLUID}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{FLUID}_{\mathrm{\_na}} \\[1ex]
v_{\mathrm{FLUID\_\_NA\_EXCRETION}} &= \mathrm{FLUID}_{\mathrm{\_k\_na}} \cdot \mathrm{FLUID}_{\mathrm{\_na\_loop}} \cdot \mathopen{}\left(1 + \frac{\frac{\mathrm{FLUID}_{\mathrm{\_GFR}}}{\mathrm{FLUID}_{\mathrm{\_GFR\_base}}} \cdot \mathrm{FLUID}_{\mathrm{\_Emax\_hctz\_na}} \cdot \max\mathopen{}\left(\mathrm{Cout}_{\mathrm{ki\_hctz}}, 0\right)}{\max\mathopen{}\left(\mathrm{Cout}_{\mathrm{ki\_hctz}}, 0\right) + \mathrm{FLUID}_{\mathrm{\_E50\_hctz\_nacl}}}\right) \\[1ex]
v_{\mathrm{FLUID\_\_NA\_REABSORPTION}} &= \mathrm{FLUID}_{\mathrm{\_h2o\_reabsorption}} \cdot \mathrm{FLUID}_{\mathrm{\_na\_loop}} \\[1ex]
v_{\mathrm{FLUID\_\_CL\_FILTRATION}} &= \mathrm{FLUID}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{FLUID}_{\mathrm{\_cl}} \\[1ex]
v_{\mathrm{FLUID\_\_CL\_EXCRETION}} &= \mathrm{FLUID}_{\mathrm{\_k\_cl}} \cdot \mathrm{FLUID}_{\mathrm{\_cl\_loop}} \cdot \mathopen{}\left(1 + \frac{\frac{\mathrm{FLUID}_{\mathrm{\_GFR}}}{\mathrm{FLUID}_{\mathrm{\_GFR\_base}}} \cdot \mathrm{FLUID}_{\mathrm{\_Emax\_hctz\_cl}} \cdot \max\mathopen{}\left(\mathrm{Cout}_{\mathrm{ki\_hctz}}, 0\right)}{\max\mathopen{}\left(\mathrm{Cout}_{\mathrm{ki\_hctz}}, 0\right) + \mathrm{FLUID}_{\mathrm{\_E50\_hctz\_nacl}}}\right) \\[1ex]
v_{\mathrm{FLUID\_\_CL\_REABSORPTION}} &= \mathrm{FLUID}_{\mathrm{\_h2o\_reabsorption}} \cdot \mathrm{FLUID}_{\mathrm{\_cl\_loop}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_ECF}}}{\mathrm{d} t} &= \mathrm{FLUID}_{\mathrm{\_H2O\_UPTAKE}} - \mathrm{FLUID}_{\mathrm{\_vout\_h2o}} - \mathrm{FLUID}_{\mathrm{\_GFR}} \cdot 0.001 + \mathrm{FLUID}_{\mathrm{\_h2o\_reabsorption}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_Vloop}}}{\mathrm{d} t} &= \mathrm{FLUID}_{\mathrm{\_GFR}} \cdot 0.001 - \mathrm{FLUID}_{\mathrm{\_diuresis}} - \mathrm{FLUID}_{\mathrm{\_h2o\_reabsorption}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_Vurine}}}{\mathrm{d} t} &= \mathrm{FLUID}_{\mathrm{\_diuresis}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}_{\mathrm{pl\_hctz}}} \Bigl( v_{\mathrm{LU\_\_J\_out\_pl\_hctz}} - v_{\mathrm{HE\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{BR\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{LI\_\_J\_in\_ar\_pl\_hctz}} \\
&\quad {} - v_{\mathrm{LI\_\_J\_shunt\_ar\_pl\_hctz}} - v_{\mathrm{KI\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{ST\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{GU\_\_J\_in\_ar\_pl\_hctz}} \\
&\quad {} - v_{\mathrm{SP\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{PA\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{MU\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{SK\_\_J\_in\_ar\_pl\_hctz}} \\
&\quad {} - v_{\mathrm{AD\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{BO\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{GO\_\_J\_in\_ar\_pl\_hctz}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}_{\mathrm{pl\_hctz}}} \Bigl( v_{\mathrm{J\_iv\_hctz}} - v_{\mathrm{LU\_\_J\_in\_ve\_pl\_hctz}} + v_{\mathrm{HE\_\_J\_out\_pl\_hctz}} + v_{\mathrm{BR\_\_J\_out\_pl\_hctz}} \\
&\quad {} + v_{\mathrm{LI\_\_J\_shunt\_ar\_pl\_hctz}} + v_{\mathrm{LI\_\_J\_shunt\_po\_pl\_hctz}} + v_{\mathrm{LI\_\_J\_out\_pl\_hctz}} + v_{\mathrm{KI\_\_J\_out\_pl\_hctz}} \\
&\quad {} + v_{\mathrm{MU\_\_J\_out\_pl\_hctz}} + v_{\mathrm{SK\_\_J\_out\_pl\_hctz}} + v_{\mathrm{AD\_\_J\_out\_pl\_hctz}} + v_{\mathrm{BO\_\_J\_out\_pl\_hctz}} \\
&\quad {} + v_{\mathrm{GO\_\_J\_out\_pl\_hctz}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vpo}_{\mathrm{pl\_hctz}}} \Bigl( -v_{\mathrm{LI\_\_J\_in\_po\_pl\_hctz}} - v_{\mathrm{LI\_\_J\_shunt\_po\_pl\_hctz}} + v_{\mathrm{ST\_\_J\_out\_pl\_hctz}} + v_{\mathrm{GU\_\_J\_out\_pl\_hctz}} \\
&\quad {} + v_{\mathrm{SP\_\_J\_out\_pl\_hctz}} + v_{\mathrm{PA\_\_J\_out\_pl\_hctz}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{hctz}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_J\_gfr\_hctz}} + v_{\mathrm{KI\_\_HCTZSEC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_tr\_rec\_hctz}} + v_{\mathrm{GU\_\_J\_trs\_rec\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cbile}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{GU\_\_J\_bile\_hctz}}}{\mathrm{Vbile}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LU}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LU\_\_J\_in\_ve\_pl\_hctz}} - v_{\mathrm{LU\_\_J\_out\_pl\_hctz}} - v_{\mathrm{LU\_\_J\_ti\_hctz}}}{\mathrm{LU}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LU}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LU\_\_J\_ti\_hctz}}}{\mathrm{LU}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{HE}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{HE\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{HE\_\_J\_out\_pl\_hctz}} - v_{\mathrm{HE\_\_J\_ti\_hctz}}}{\mathrm{HE}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{HE}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{HE\_\_J\_ti\_hctz}}}{\mathrm{HE}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{BR}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{BR\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{BR\_\_J\_out\_pl\_hctz}} - v_{\mathrm{BR\_\_J\_ti\_hctz}}}{\mathrm{BR}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{BR}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{BR\_\_J\_ti\_hctz}}}{\mathrm{BR}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_J\_in\_ar\_pl\_hctz}} + v_{\mathrm{LI\_\_J\_in\_po\_pl\_hctz}} - v_{\mathrm{LI\_\_J\_out\_pl\_hctz}} - v_{\mathrm{LI\_\_J\_ti\_hctz}}}{\mathrm{LI}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_J\_ti\_hctz}}}{\mathrm{LI}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{KI}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{KI\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{KI\_\_J\_out\_pl\_hctz}} - v_{\mathrm{KI\_\_J\_gfr\_hctz}} - v_{\mathrm{KI\_\_J\_is\_hctz}}}{\mathrm{KI}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{KI}_{\mathrm{\_Cis\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{KI\_\_J\_is\_hctz}} - v_{\mathrm{KI\_\_J\_ic\_hctz}} - v_{\mathrm{KI\_\_HCTZUP}}}{\mathrm{KI}_{\mathrm{\_Vis}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{KI}_{\mathrm{\_Cic\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{KI\_\_J\_ic\_hctz}} + v_{\mathrm{KI\_\_HCTZUP}} - v_{\mathrm{KI\_\_HCTZSEC}}}{\mathrm{KI}_{\mathrm{\_Vic}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ST}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{ST\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{ST\_\_J\_out\_pl\_hctz}} - v_{\mathrm{ST\_\_J\_ti\_hctz}}}{\mathrm{ST}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ST}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{ST\_\_J\_ti\_hctz}}}{\mathrm{ST}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{1}{\mathrm{GU}_{\mathrm{\_Vpl\_hctz}}} \Bigl( v_{\mathrm{GU\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{GU\_\_J\_out\_pl\_hctz}} - v_{\mathrm{GU\_\_J\_ti\_hctz}} + v_{\mathrm{GU\_\_J\_abs\_du\_hctz}} \\
&\quad {} + v_{\mathrm{GU\_\_J\_abs\_jej1\_hctz}} + v_{\mathrm{GU\_\_J\_abs\_jej2\_hctz}} + v_{\mathrm{GU\_\_J\_abs\_ile1\_hctz}} + v_{\mathrm{GU\_\_J\_abs\_ile2\_hctz}} \\
&\quad {} + v_{\mathrm{GU\_\_J\_abs\_cae\_hctz}} + v_{\mathrm{GU\_\_J\_abs\_asc\_hctz}} + v_{\mathrm{GU\_\_J\_abs\_tra\_hctz}} + v_{\mathrm{GU\_\_J\_abs\_des\_hctz}} \\
&\quad {} + v_{\mathrm{GU\_\_J\_abs\_sig\_hctz}} + v_{\mathrm{GU\_\_J\_abs\_rec\_hctz}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_ti\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_st\_hctz}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{GU\_\_J\_tr\_st\_hctz}} + v_{\mathrm{GU\_\_J\_po\_hctz}} + v_{\mathrm{GU\_\_J\_sol\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_st}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_du\_hctz}}}{\mathrm{d} t} &= \frac{1}{\mathrm{GU}_{\mathrm{\_Vlumen\_du}}} \Bigl( v_{\mathrm{GU\_\_J\_tr\_st\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_du\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_du\_hctz}} + v_{\mathrm{GU\_\_J\_bile\_hctz}} \\
&\quad {} + v_{\mathrm{GU\_\_J\_dis\_du\_hctz}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_jej1\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_du\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_jej1\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_jej1\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_jej1\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_jej1}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_jej2\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_jej1\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_jej2\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_jej2\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_jej2\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_jej2}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_ile1\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_jej2\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_ile1\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_ile1\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_ile1\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_ile1}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_ile2\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_ile1\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_ile2\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_ile2\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_ile2\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_ile2}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_cae\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_ile2\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_cae\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_cae\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_cae\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_cae}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_asc\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_cae\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_asc\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_asc\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_asc\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_asc}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_tra\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_asc\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_tra\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_tra\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_tra\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_tra}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_des\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_tra\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_des\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_des\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_des\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_des}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_sig\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_des\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_sig\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_sig\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_sig\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_sig}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Clumen\_rec\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_J\_tr\_sig\_hctz}} - v_{\mathrm{GU\_\_J\_tr\_rec\_hctz}} - v_{\mathrm{GU\_\_J\_abs\_rec\_hctz}} + v_{\mathrm{GU\_\_J\_dis\_rec\_hctz}}}{\mathrm{GU}_{\mathrm{\_Vlumen\_rec}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_du\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_st\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_du\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_du\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_jej1\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_du\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_jej1\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_jej1\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_jej2\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_jej1\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_jej2\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_jej2\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_ile1\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_jej2\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_ile1\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_ile1\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_ile2\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_ile1\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_ile2\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_ile2\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_cae\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_ile2\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_cae\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_cae\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_asc\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_cae\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_asc\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_asc\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_tra\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_asc\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_tra\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_tra\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_des\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_tra\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_des\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_des\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_sig\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_des\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_sig\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_sig\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_Asolid\_rec\_hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_J\_trs\_sig\_hctz}} - v_{\mathrm{GU\_\_J\_dis\_rec\_hctz}} - v_{\mathrm{GU\_\_J\_trs\_rec\_hctz}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{SP}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{SP\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{SP\_\_J\_out\_pl\_hctz}} - v_{\mathrm{SP\_\_J\_ti\_hctz}}}{\mathrm{SP}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{SP}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{SP\_\_J\_ti\_hctz}}}{\mathrm{SP}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PA}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{PA\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{PA\_\_J\_out\_pl\_hctz}} - v_{\mathrm{PA\_\_J\_ti\_hctz}}}{\mathrm{PA}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PA}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{PA\_\_J\_ti\_hctz}}}{\mathrm{PA}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{MU}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{MU\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{MU\_\_J\_out\_pl\_hctz}} - v_{\mathrm{MU\_\_J\_ti\_hctz}}}{\mathrm{MU}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{MU}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{MU\_\_J\_ti\_hctz}}}{\mathrm{MU}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{SK}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{SK\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{SK\_\_J\_out\_pl\_hctz}} - v_{\mathrm{SK\_\_J\_ti\_hctz}}}{\mathrm{SK}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{SK}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{SK\_\_J\_ti\_hctz}}}{\mathrm{SK}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{AD}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{AD\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{AD\_\_J\_out\_pl\_hctz}} - v_{\mathrm{AD\_\_J\_ti\_hctz}}}{\mathrm{AD}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{AD}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{AD\_\_J\_ti\_hctz}}}{\mathrm{AD}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{BO}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{BO\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{BO\_\_J\_out\_pl\_hctz}} - v_{\mathrm{BO\_\_J\_ti\_hctz}}}{\mathrm{BO}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{BO}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{BO\_\_J\_ti\_hctz}}}{\mathrm{BO}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GO}_{\mathrm{\_Cpl\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GO\_\_J\_in\_ar\_pl\_hctz}} - v_{\mathrm{GO\_\_J\_out\_pl\_hctz}} - v_{\mathrm{GO\_\_J\_ti\_hctz}}}{\mathrm{GO}_{\mathrm{\_Vpl\_hctz}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GO}_{\mathrm{\_Cti\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GO\_\_J\_ti\_hctz}}}{\mathrm{GO}_{\mathrm{\_Vti}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_na}}}{\mathrm{d} t} &= \frac{v_{\mathrm{FLUID\_\_NA\_UPTAKE}} - v_{\mathrm{FLUID\_\_NA\_FILTRATION}} + v_{\mathrm{FLUID\_\_NA\_REABSORPTION}}}{\mathrm{FLUID}_{\mathrm{\_ECF}}} - \frac{\mathrm{FLUID}_{\mathrm{\_na}}}{\mathrm{FLUID}_{\mathrm{\_ECF}}} \cdot \frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_ECF}}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_na\_loop}}}{\mathrm{d} t} &= \frac{v_{\mathrm{FLUID\_\_NA\_FILTRATION}} - v_{\mathrm{FLUID\_\_NA\_EXCRETION}} - v_{\mathrm{FLUID\_\_NA\_REABSORPTION}}}{\mathrm{FLUID}_{\mathrm{\_Vloop}}} - \frac{\mathrm{FLUID}_{\mathrm{\_na\_loop}}}{\mathrm{FLUID}_{\mathrm{\_Vloop}}} \cdot \frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_Vloop}}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_na\_urine}}}{\mathrm{d} t} &= v_{\mathrm{FLUID\_\_NA\_EXCRETION}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_cl}}}{\mathrm{d} t} &= \frac{v_{\mathrm{FLUID\_\_CL\_UPTAKE}} - v_{\mathrm{FLUID\_\_CL\_FILTRATION}} + v_{\mathrm{FLUID\_\_CL\_REABSORPTION}}}{\mathrm{FLUID}_{\mathrm{\_ECF}}} - \frac{\mathrm{FLUID}_{\mathrm{\_cl}}}{\mathrm{FLUID}_{\mathrm{\_ECF}}} \cdot \frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_ECF}}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_cl\_loop}}}{\mathrm{d} t} &= \frac{v_{\mathrm{FLUID\_\_CL\_FILTRATION}} - v_{\mathrm{FLUID\_\_CL\_EXCRETION}} - v_{\mathrm{FLUID\_\_CL\_REABSORPTION}}}{\mathrm{FLUID}_{\mathrm{\_Vloop}}} - \frac{\mathrm{FLUID}_{\mathrm{\_cl\_loop}}}{\mathrm{FLUID}_{\mathrm{\_Vloop}}} \cdot \frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_Vloop}}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{FLUID}_{\mathrm{\_cl\_urine}}}{\mathrm{d} t} &= v_{\mathrm{FLUID\_\_CL\_EXCRETION}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{IVDOSE}_{\mathrm{hctz}}}{\mathrm{d} t} &= -v_{\mathrm{J\_iv\_hctz}} \cdot \mathrm{Mr}_{\mathrm{hctz}} + \mathrm{Ri}_{\mathrm{hctz}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{hctz}}}{\mathrm{d} t} &= -\mathopen{}\left(v_{\mathrm{GU\_\_J\_po\_hctz}} + v_{\mathrm{GU\_\_J\_trs\_st\_hctz}}\right) \cdot \mathrm{Mr}_{\mathrm{hctz}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{SOLDOSE}_{\mathrm{hctz}}}{\mathrm{d} t} &= -v_{\mathrm{GU\_\_J\_sol\_hctz}} \cdot \mathrm{Mr}_{\mathrm{hctz}} \qquad \text{(rate rule)}
\end{aligned}
$$

The concentration of a species in a compartment whose size changes is diluted by the rate of the size (SBML Level 3 Version 2, section 3.4.6), the amount it holds is kept.
