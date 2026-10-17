# Hydrochlorothiazide (HCTZ) body model

Model `hctz_body`, SBML Level 3 Version 2, read from hctz\_body\_flat.xml, written by sbmlode 0.3.0.

Hydrochlorothiazide (HCTZ) body model

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
| $\mathrm{ECF}$ | `ECF` | extracellular fluid (ECF) | $\mathrm{NaN}$ | l |  |
| $\mathrm{Vloop}$ | `Vloop` | renal tubule | $0.5$ | l |  |
| $\mathrm{Vre}$ | `Vre` | rest of body |  | l |  |
| $\mathrm{Vgu}$ | `Vgu` | gut |  | l |  |
| $\mathrm{Vki}$ | `Vki` | kidney |  | l |  |
| $\mathrm{Vli}$ | `Vli` | liver |  | l |  |
| $\mathrm{Vlu}$ | `Vlu` | lung |  | l |  |
| $\mathrm{Vve}$ | `Vve` | venous blood |  | l |  |
| $\mathrm{Var}$ | `Var` | arterial blood |  | l |  |
| $\mathrm{Vurine}$ | `Vurine` | urine | $10^{-6}$ | l |  |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vgu}_{\mathrm{lumen}}$ | `Vgu_lumen` | intestinal lumen |  | l |  |
| $\mathrm{Vpo}$ | `Vpo` | portal plasma |  | l |  |
| $\mathrm{Vhv}$ | `Vhv` | hepatic venous plasma |  | l |  |
| $\mathrm{Vki}_{\mathrm{tissue}}$ | `Vki_tissue` | ki tissue |  | l |  |
| $\mathrm{Vki}_{\mathrm{plasma}}$ | `Vki_plasma` | ki plasma |  | l |  |
| $\mathrm{Vli}_{\mathrm{tissue}}$ | `Vli_tissue` | li tissue |  | l |  |
| $\mathrm{Vli}_{\mathrm{plasma}}$ | `Vli_plasma` | li plasma |  | l |  |
| $\mathrm{Vlu}_{\mathrm{tissue}}$ | `Vlu_tissue` | lu tissue |  | l |  |
| $\mathrm{Vlu}_{\mathrm{plasma}}$ | `Vlu_plasma` | lu plasma |  | l |  |
| $\mathrm{Vgu}_{\mathrm{tissue}}$ | `Vgu_tissue` | gu tissue |  | l |  |
| $\mathrm{Vgu}_{\mathrm{plasma}}$ | `Vgu_plasma` | gu plasma |  | l |  |
| $\mathrm{Vre}_{\mathrm{tissue}}$ | `Vre_tissue` | re tissue |  | l |  |
| $\mathrm{Vre}_{\mathrm{plasma}}$ | `Vre_plasma` | re plasma |  | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{hctz}$ | `hctz` | hydrochlorothiazide | $\mathrm{ECF}$ |  | mmol/l | concentration |
| $\mathrm{na}$ | `na` | Sodium (Na+) (ECF) | $\mathrm{ECF}$ | $140$ | mmol/l | concentration |
| $\mathrm{na}_{\mathrm{loop}}$ | `na_loop` | Sodium (Na+) (renal tubule) | $\mathrm{Vloop}$ | $140$ | mmol/l | concentration |
| $\mathrm{na}_{\mathrm{urine}}$ | `na_urine` | Sodium (Na+) (urine) | $\mathrm{Vurine}$ | $0$ | mmol | amount |
| $\mathrm{cl}$ | `cl` | Chloride (Cl-) (ECF) | $\mathrm{ECF}$ | $102$ | mmol/l | concentration |
| $\mathrm{cl}_{\mathrm{loop}}$ | `cl_loop` | Chloride (Cl-) (renal tubule) | $\mathrm{Vloop}$ | $102$ | mmol/l | concentration |
| $\mathrm{cl}_{\mathrm{urine}}$ | `cl_urine` | Chloride (Cl-) (urine) | $\mathrm{Vurine}$ | $0$ | mmol | amount |
| $\mathrm{Cki}_{\mathrm{plasma\_hctz}}$ | `Cki_plasma_hctz` | hydrochlorothiazide (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_hctz}}$ | `Cli_plasma_hctz` | hydrochlorothiazide (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_hctz}}$ | `Clu_plasma_hctz` | hydrochlorothiazide (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_hctz}}$ | `Cgu_plasma_hctz` | hydrochlorothiazide (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_hctz}}$ | `Cre_plasma_hctz` | hydrochlorothiazide (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{hctz}}$ | `Car_hctz` | hydrochlorothiazide (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{hctz}}$ | `Cve_hctz` | hydrochlorothiazide (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{hctz}}$ | `Cpo_hctz` | hydrochlorothiazide (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{hctz}}$ | `Chv_hctz` | hydrochlorothiazide (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{hctz}}$ | `Cli_hctz` | hydrochlorothiazide (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{hctz}}$ | `Clu_hctz` | hydrochlorothiazide (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{hctz}}$ | `Cre_hctz` | hydrochlorothiazide (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{hctz}}$ | `Aurine_hctz` | hydrochlorothiazide (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Afeces}_{\mathrm{hctz}}$ | `Afeces_hctz` | hydrochlorothiazide (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Cgu}_{\mathrm{hctz}}$ | `Cgu_hctz` | hydrochlorothiazide (intestinal lumen) | $\mathrm{Vgu}_{\mathrm{lumen}}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{TBW}}$ | `f_TBW` | Total body water (TBW) fraction of bodyweight | $0.55$ | l/kg | ✓ |
| $f_{\mathrm{ECF}}$ | `f_ECF` | ECF fraction of TBW | $0.33$ | \- | ✓ |
| $\mathrm{ECF}_{\mathrm{ref}}$ | `ECF_ref` | Reference extracellular fluid volume (ECF) |  | l |  |
| $\mathrm{Psys}_{\mathrm{ref}}$ | `Psys_ref` | Reference systolic blood pressure | $120$ | (133.322 N)/m<sup>2</sup> | ✓ |
| $\mathrm{Pdia}_{\mathrm{ref}}$ | `Pdia_ref` | Reference diastolic blood pressure | $80$ | (133.322 N)/m<sup>2</sup> | ✓ |
| $\mathrm{bp}_{\mathrm{systolic}}$ | `bp_systolic` | Systolic blood pressure |  | (133.322 N)/m<sup>2</sup> |  |
| $\mathrm{bp}_{\mathrm{diastolic}}$ | `bp_diastolic` | Diastolic blood pressure |  | (133.322 N)/m<sup>2</sup> |  |
| $\mathrm{bp}_{\mathrm{mean}}$ | `bp_mean` | Mean arterial pressure |  | (133.322 N)/m<sup>2</sup> |  |
| $\mathrm{Mr}_{\mathrm{nacl}}$ | `Mr_nacl` | Molecular weight sodium chloride | $58.44$ | g/mol | ✓ |
| $\mathrm{Mr}_{\mathrm{na}}$ | `Mr_na` | Molecular weight sodium | $22.99$ | g/mol | ✓ |
| $\mathrm{Mr}_{\mathrm{cl}}$ | `Mr_cl` | Molecular weight chloride | $35.45$ | g/mol | ✓ |
| $\mathrm{vin}_{\mathrm{na}}$ | `vin_na` | Na uptake via food |  | mmol/min |  |
| $\mathrm{vin}_{\mathrm{cl}}$ | `vin_cl` | Cl uptake via food |  | mmol/min |  |
| $\mathrm{vin}_{\mathrm{h2o}}$ | `vin_h2o` | H2O uptake via food | $0.00159722222222222$ | l/min | ✓ |
| $\mathrm{vout}_{\mathrm{h2o}}$ | `vout_h2o` | H2O loss without urine | $0.000625$ | l/min | ✓ |
| $k_{\mathrm{na}}$ | `k_na` |  | $0.000676649741186695$ | l/min | ✓ |
| $k_{\mathrm{cl}}$ | `k_cl` |  | $0.00370716553162286$ | l/min | ✓ |
| $k_{\mathrm{h2o}}$ | `k_h2o` |  | $\mathrm{NaN}$ | l/ml |  |
| $\mathrm{h2o}_{\mathrm{reabsorption}}$ | `h2o_reabsorption` | H2O reabsorption from the renal tubule |  | l/min |  |
| $\mathrm{diuresis}$ | `diuresis` |  |  | l/min |  |
| $f_{\mathrm{h2o\_max}}$ | `f_h2o_max` | maximal fractional excretion of water | $0.3$ | \- | ✓ |
| $\mathrm{counter}_{\mathrm{gamma}}$ | `counter_gamma` |  | $5$ | \- | ✓ |
| $\mathrm{E50}_{\mathrm{hctz\_nacl}}$ | `E50_hctz_nacl` |  | $8.61825350924873 \times 10^{-5}$ | mmol/l | ✓ |
| $\mathrm{Emax}_{\mathrm{hctz\_na}}$ | `Emax_hctz_na` |  | $1.72544627809791$ | \- | ✓ |
| $\mathrm{Emax}_{\mathrm{hctz\_cl}}$ | `Emax_hctz_cl` |  | $0.457489998677387$ | \- | ✓ |
| $\mathrm{na}_{\mathrm{ref}}$ | `na_ref` |  | $140$ | mmol/l | ✓ |
| $\mathrm{cl}_{\mathrm{ref}}$ | `cl_ref` |  | $102$ | mmol/l | ✓ |
| $\mathrm{BW}$ | `BW` | body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{BW}_{\mathrm{ref}}$ | `BW_ref` | reference body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{HEIGHT}$ | `HEIGHT` | height \[cm\] | $170$ | cm | ✓ |
| $f_{\mathrm{renal\_function}}$ | `f_renal_function` | renal function | $1$ | \- | ✓ |
| $f_{\mathrm{GFR\_Qki}}$ | `f_GFR_Qki` | relationship GFR and Qki | $76.3105006271061$ | ml/l | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (base) |  | ml/min |  |
| $\mathrm{BSA}$ | `BSA` | body surface area \[m^2\] |  | m<sup>2</sup> |  |
| $f_{\mathrm{cardiac\_function}}$ | `f_cardiac_function` | factor for cardiac impairment | $1$ | \- | ✓ |
| $\mathrm{COBW}$ | `COBW` | cardiac output per bodyweight \[ml/s/kg\] | $1.548$ | ml/s/kg | ✓ |
| $\mathrm{CO}$ | `CO` | cardiac output \[ml/s\] |  | ml/s |  |
| $\mathrm{QC}$ | `QC` | cardiac output \[l/min\] |  | l/min |  |
| $\mathrm{Fblood}$ | `Fblood` | blood fraction of organ volume | $0.02$ | \- | ✓ |
| $\mathrm{FVgu}$ | `FVgu` | gut fractional tissue volume | $0.0171$ | l/kg | ✓ |
| $\mathrm{FVki}$ | `FVki` | kidney fractional tissue volume | $0.0044$ | l/kg | ✓ |
| $\mathrm{FVli}$ | `FVli` | liver fractional tissue volume | $0.021$ | l/kg | ✓ |
| $\mathrm{FVlu}$ | `FVlu` | lung fractional tissue volume | $0.0076$ | l/kg | ✓ |
| $\mathrm{FVre}$ | `FVre` | rest of body fractional tissue volume |  | l/kg |  |
| $\mathrm{FVve}$ | `FVve` | venous fractional tissue volume | $0.0514$ | l/kg | ✓ |
| $\mathrm{FVar}$ | `FVar` | arterial fractional tissue volume | $0.0257$ | l/kg | ✓ |
| $\mathrm{FVpo}$ | `FVpo` | portal fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FVhv}$ | `FVhv` | hepatic venous fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FQgu}$ | `FQgu` | gut fractional tissue blood flow | $0.18$ | \- | ✓ |
| $\mathrm{FQki}$ | `FQki` | kidney fractional tissue blood flow | $0.19$ | \- | ✓ |
| $\mathrm{FQh}$ | `FQh` | hepatic (venous side) fractional tissue blood flow | $0.215$ | \- | ✓ |
| $\mathrm{FQlu}$ | `FQlu` | lung fractional tissue blood flow | $1$ | \- | ✓ |
| $\mathrm{FQre}$ | `FQre` | rest of body fractional tissue blood flow |  | \- |  |
| $\mathrm{conversion}_{\mathrm{min\_per\_day}}$ | `conversion_min_per_day` | Conversion factor day to min | $1440$ | min/day | ✓ |
| $f_{\mathrm{cirrhosis}}$ | `f_cirrhosis` | severity of cirrhosis \[0, 0.95\] | $0$ | \- | ✓ |
| $f_{\mathrm{shunts}}$ | `f_shunts` | fraction of portal venous blood shunted by the liver |  | \- |  |
| $f_{\mathrm{tissue\_loss}}$ | `f_tissue_loss` | fraction of lost parenchymal liver volume |  | \- |  |
| $\mathrm{PODOSE}_{\mathrm{hctz}}$ | `PODOSE_hctz` | oral dose hctz \[mg\] | $0$ | mg |  |
| $\mathrm{POSOLUTION}_{\mathrm{hctz}}$ | `POSOLUTION_hctz` | oral dose as solution hctz \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{dis\_hctz}}$ | `Ka_dis_hctz` | Ka\_dis \[1/hr\] dissolution hydrochlorothiazide | $1.30141095353971$ | 1/hr | ✓ |
| $v_{\mathrm{HCTZEX}}$ | `v_HCTZEX` | rate of HCTZ excretion |  | mmol/min |  |
| $\mathrm{Mr}_{\mathrm{hctz}}$ | `Mr_hctz` | Molecular weight hctz \[g/mole\] | $297.7$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{hctz}}$ | `ftissue_hctz` | tissue distribution hctz | $0.0637160968791131$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{hctz}}$ | `Kp_hctz` | tissue/plasma partition coefficient hctz | $2.36426059508621$ | \- | ✓ |
| $\mathrm{IVDOSE}_{\mathrm{hctz}}$ | `IVDOSE_hctz` | IV bolus dose hctz \[mg\] | $0$ | mg |  |
| $\mathrm{ti}_{\mathrm{hctz}}$ | `ti_hctz` | injection time hctz \[s\] | $10$ | s | ✓ |
| $\mathrm{Ki}_{\mathrm{hctz}}$ | `Ki_hctz` | Ki \[1/min\] injection hctz |  | 1/min |  |
| $\mathrm{GFR}$ | `GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{vout}_{\mathrm{na}}$ | `vout_na` |  |  | mg/min |  |
| $\mathrm{vout}_{\mathrm{cl}}$ | `vout_cl` |  |  | mg/min |  |
| $\mathrm{H2O}_{\mathrm{UPTAKE}}$ | `H2O_UPTAKE` |  |  | l/min |  |
| $\mathrm{Qgu}$ | `Qgu` | gut blood flow |  | l/min |  |
| $\mathrm{Qki}$ | `Qki` | kidney blood flow |  | l/min |  |
| $\mathrm{Qh}$ | `Qh` | hepatic (venous side) blood flow |  | l/min |  |
| $\mathrm{Qha}$ | `Qha` | hepatic artery blood flow |  | l/min |  |
| $\mathrm{Qlu}$ | `Qlu` | lung blood flow |  | l/min |  |
| $\mathrm{Qre}$ | `Qre` | rest of body blood flow |  | l/min |  |
| $\mathrm{Qpo}$ | `Qpo` | portal blood flow |  | l/min |  |
| $\mathrm{hctz}_{\mathrm{urine\_excretion}}$ | `hctz_urine_excretion` | HCTZ concentration in excreted urine |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_HCTZEX\_f}}$ | `KI__HCTZEX_f` | intrinsic renal clearance of hydrochlorothiazide relative to the GFR | $3.23772819218966$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_GFR}}$ | `KI__GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{GU}_{\mathrm{\_F\_hctz\_abs}}$ | `GU__F_hctz_abs` | fraction absorbed hydrochlorothiazide | $0.7$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_HCTZABS\_k}}$ | `GU__HCTZABS_k` | rate of hydrochlorothiazide absorption | $0.00507166463188506$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_POSTOMACH\_hctz}}$ | `GU__POSTOMACH_hctz` | oral dose in stomach hydrochlorothiazide \[mg\] | $0$ | mg |  |
| $\mathrm{GU}_{\mathrm{\_Ka\_application\_hctz}}$ | `GU__Ka_application_hctz` | Ka \[1/hr\] application hydrochlorothiazide | $1000$ | 1/hr | ✓ |
| $\mathrm{GU}_{\mathrm{\_application\_hctz}}$ | `GU__application_hctz` | PO application hydrochlorothiazide |  | mmol/min |  |
| $\mathrm{GU}_{\mathrm{\_absorption}}$ | `GU__absorption` | absorption hydrochlorothiazide |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{na} &= \mathrm{na}_{\mathrm{ref}} \\[1ex]
\mathrm{cl} &= \mathrm{cl}_{\mathrm{ref}} \\[1ex]
\mathrm{Aurine}_{\mathrm{hctz}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Afeces}_{\mathrm{hctz}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{ECF} &= \mathrm{ECF}_{\mathrm{ref}} \\[1ex]
\mathrm{Vloop} &= 0.05 \cdot \mathrm{ECF}_{\mathrm{ref}} \\[1ex]
k_{\mathrm{h2o}} &= \frac{\mathrm{vin}_{\mathrm{h2o}} - \mathrm{vout}_{\mathrm{h2o}}}{\mathrm{GFR}_{\mathrm{base}}}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{ECF}_{\mathrm{ref}} &= f_{\mathrm{ECF}} \cdot f_{\mathrm{TBW}} \cdot \mathrm{BW} \\[1ex]
\mathrm{bp}_{\mathrm{systolic}} &= \frac{\mathrm{Psys}_{\mathrm{ref}} \cdot \mathrm{ECF}}{\mathrm{ECF}_{\mathrm{ref}}} \\[1ex]
\mathrm{bp}_{\mathrm{diastolic}} &= \frac{\mathrm{Pdia}_{\mathrm{ref}} \cdot \mathrm{ECF}}{\mathrm{ECF}_{\mathrm{ref}}} \\[1ex]
\mathrm{bp}_{\mathrm{mean}} &= \frac{\mathrm{bp}_{\mathrm{systolic}} + 2 \cdot \mathrm{bp}_{\mathrm{diastolic}}}{3} \\[1ex]
\mathrm{vin}_{\mathrm{na}} &= k_{\mathrm{na}} \cdot \mathrm{na}_{\mathrm{ref}} \\[1ex]
\mathrm{vin}_{\mathrm{cl}} &= k_{\mathrm{cl}} \cdot \mathrm{cl}_{\mathrm{ref}} \\[1ex]
\mathrm{H2O}_{\mathrm{UPTAKE}} &= \frac{\mathrm{vin}_{\mathrm{h2o}} \cdot \mathrm{ECF}_{\mathrm{ref}}^{\mathrm{counter}_{\mathrm{gamma}}}}{\mathrm{ECF}^{\mathrm{counter}_{\mathrm{gamma}}}} \\[1ex]
f_{\mathrm{shunts}} &= f_{\mathrm{cirrhosis}} \\[1ex]
f_{\mathrm{tissue\_loss}} &= f_{\mathrm{cirrhosis}} \\[1ex]
\mathrm{FVre} &= 1 - \mathrm{FVgu} - \mathrm{FVki} - \mathrm{FVli} \\
&\quad {} - \mathrm{FVlu} - \mathrm{FVve} - \mathrm{FVar} \\[1ex]
\mathrm{FQre} &= 1 - \mathrm{FQki} - \mathrm{FQh} \\[1ex]
\mathrm{BSA} &= 0.024265 \cdot \mathopen{}\left(\frac{\mathrm{BW}}{1}\right)^{0.5378} \cdot \mathopen{}\left(\frac{\mathrm{HEIGHT}}{1}\right)^{0.3964} \\[1ex]
\mathrm{CO} &= \mathrm{BW} \cdot f_{\mathrm{cardiac\_function}} \cdot \mathrm{COBW} \\[1ex]
\mathrm{QC} &= \frac{\mathrm{CO}}{1000} \cdot 60 \\[1ex]
\mathrm{Vgu} &= \mathrm{BW} \cdot \mathrm{FVgu} \\[1ex]
\mathrm{Vgu}_{\mathrm{lumen}} &= \mathrm{Vgu} \\[1ex]
\mathrm{Vki} &= \mathrm{BW} \cdot \mathrm{FVki} \\[1ex]
\mathrm{Vli} &= \mathrm{BW} \cdot \mathrm{FVli} \\[1ex]
\mathrm{Vlu} &= \mathrm{BW} \cdot \mathrm{FVlu} \\[1ex]
\mathrm{Vre} &= \mathrm{BW} \cdot \mathrm{FVre} \\[1ex]
\mathrm{Vve} &= \mathrm{BW} \cdot \mathrm{FVve} - \frac{\mathrm{FVve}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Var} &= \mathrm{BW} \cdot \mathrm{FVar} - \frac{\mathrm{FVar}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Vpo} &= \mathrm{BW} \cdot \mathrm{FVpo} - \frac{\mathrm{FVpo}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right) \\[1ex]
\mathrm{Vhv} &= \mathrm{BW} \cdot \mathrm{FVhv} - \frac{\mathrm{FVhv}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right) \\[1ex]
\mathrm{Qgu} &= \mathrm{QC} \cdot \mathrm{FQgu} \\[1ex]
\mathrm{Qki} &= \mathrm{QC} \cdot \mathrm{FQki} \\[1ex]
\mathrm{Qh} &= \mathrm{QC} \cdot \mathrm{FQh} \\[1ex]
\mathrm{Qha} &= \mathrm{Qh} - \mathrm{Qgu} \\[1ex]
\mathrm{Qlu} &= \mathrm{QC} \cdot \mathrm{FQlu} \\[1ex]
\mathrm{Qre} &= \mathrm{QC} \cdot \mathrm{FQre} \\[1ex]
\mathrm{Qpo} &= \mathrm{Qgu} \\[1ex]
\mathrm{GFR}_{\mathrm{base}} &= f_{\mathrm{GFR\_Qki}} \cdot \mathrm{Qki} \\[1ex]
\mathrm{GFR} &= f_{\mathrm{renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
\mathrm{Vki}_{\mathrm{plasma}} &= \mathrm{Vki} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vki}_{\mathrm{tissue}} &= \mathrm{Vki} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{plasma}} &= \mathrm{Vli} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vli}_{\mathrm{tissue}} &= \mathrm{Vli} \cdot \mathopen{}\left(1 - f_{\mathrm{tissue\_loss}}\right) \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{plasma}} &= \mathrm{Vlu} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vlu}_{\mathrm{tissue}} &= \mathrm{Vlu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{plasma}} &= \mathrm{Vgu} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vgu}_{\mathrm{tissue}} &= \mathrm{Vgu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{plasma}} &= \mathrm{Vre} \cdot \mathrm{Fblood} \\[1ex]
\mathrm{Vre}_{\mathrm{tissue}} &= \mathrm{Vre} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Ki}_{\mathrm{hctz}} &= \frac{0.693}{\mathrm{ti}_{\mathrm{hctz}}} \cdot 60 \\[1ex]
\mathrm{hctz} &= \mathrm{Cki}_{\mathrm{plasma\_hctz}} \\[1ex]
\mathrm{KI}_{\mathrm{\_GFR}} &= f_{\mathrm{renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
v_{\mathrm{HCTZEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{KI}_{\mathrm{\_HCTZEX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_hctz}} \\[1ex]
\mathrm{GU}_{\mathrm{\_absorption}} &= \mathrm{GU}_{\mathrm{\_HCTZABS\_k}} \cdot \mathrm{Vgu}_{\mathrm{lumen}} \cdot \mathrm{Cgu}_{\mathrm{hctz}} \\[1ex]
\mathrm{GU}_{\mathrm{\_application\_hctz}} &= \frac{\frac{\mathrm{GU}_{\mathrm{\_Ka\_application\_hctz}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}} \\[1ex]
\mathrm{vout}_{\mathrm{na}} &= v_{\mathrm{NA\_EXCRETION}} \cdot \mathrm{Mr}_{\mathrm{na}} \\[1ex]
\mathrm{diuresis} &= \min\mathopen{}\left(\frac{\frac{k_{\mathrm{h2o}} \cdot \mathrm{GFR} \cdot \mathrm{ECF}^{\mathrm{counter}_{\mathrm{gamma}}}}{\mathrm{ECF}_{\mathrm{ref}}^{\mathrm{counter}_{\mathrm{gamma}}}} \cdot v_{\mathrm{NA\_EXCRETION}}}{\mathrm{vin}_{\mathrm{na}}}, f_{\mathrm{h2o\_max}} \cdot \mathrm{GFR} \cdot 0.001\right) \\[1ex]
\mathrm{h2o}_{\mathrm{reabsorption}} &= \mathrm{GFR} \cdot 0.001 - \mathrm{diuresis} \\[1ex]
\mathrm{hctz}_{\mathrm{urine\_excretion}} &= \frac{v_{\mathrm{HCTZEX}}}{\mathrm{diuresis}} \\[1ex]
\mathrm{vout}_{\mathrm{cl}} &= v_{\mathrm{CL\_EXCRETION}} \cdot \mathrm{Mr}_{\mathrm{cl}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $v_{\mathrm{NA\_UPTAKE}}$ | `NA_UPTAKE` | Na uptake via food | $\varnothing \longrightarrow \mathrm{na}$ |  |
| $v_{\mathrm{CL\_UPTAKE}}$ | `CL_UPTAKE` | Cl uptake via food | $\varnothing \longrightarrow \mathrm{cl}$ |  |
| $v_{\mathrm{NA\_FILTRATION}}$ | `NA_FILTRATION` | Na filtration kidney | $\mathrm{na} \longrightarrow \mathrm{na}_{\mathrm{loop}}$ |  |
| $v_{\mathrm{NA\_EXCRETION}}$ | `NA_EXCRETION` | Na excretion urine | $\mathrm{na}_{\mathrm{loop}} \longrightarrow \mathrm{na}_{\mathrm{urine}}$ | $\mathrm{hctz}$ |
| $v_{\mathrm{NA\_REABSORPTION}}$ | `NA_REABSORPTION` | Na reabsorption kidney | $\mathrm{na}_{\mathrm{loop}} \longrightarrow \mathrm{na}$ |  |
| $v_{\mathrm{CL\_FILTRATION}}$ | `CL_FILTRATION` | Cl filtration kidney | $\mathrm{cl} \longrightarrow \mathrm{cl}_{\mathrm{loop}}$ |  |
| $v_{\mathrm{CL\_EXCRETION}}$ | `CL_EXCRETION` | Cl excretion urine | $\mathrm{cl}_{\mathrm{loop}} \longrightarrow \mathrm{cl}_{\mathrm{urine}}$ | $\mathrm{hctz}$ |
| $v_{\mathrm{CL\_REABSORPTION}}$ | `CL_REABSORPTION` | Cl reabsorption kidney | $\mathrm{cl}_{\mathrm{loop}} \longrightarrow \mathrm{cl}$ |  |
| $v_{\mathrm{transport\_li\_hctz}}$ | `transport_li_hctz` | transport hydrochlorothiazide | $\mathrm{Cli}_{\mathrm{plasma\_hctz}} \rightleftharpoons \mathrm{Cli}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{transport\_lu\_hctz}}$ | `transport_lu_hctz` | transport hydrochlorothiazide | $\mathrm{Clu}_{\mathrm{plasma\_hctz}} \rightleftharpoons \mathrm{Clu}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{transport\_re\_hctz}}$ | `transport_re_hctz` | transport hydrochlorothiazide | $\mathrm{Cre}_{\mathrm{plasma\_hctz}} \rightleftharpoons \mathrm{Cre}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{iv\_hctz}}$ | `iv_hctz` | iv hydrochlorothiazide | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_hctz}}$ | `Flow_ar_ki_hctz` | inflow kidney hydrochlorothiazide | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_hctz}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_hctz}}$ | `Flow_ki_ve_hctz` | outflow kidney hydrochlorothiazide | $\mathrm{Cki}_{\mathrm{plasma\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_hctz}}$ | `Flow_arli_li_hctz` | arterial inflow liver hydrochlorothiazide | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_hctz}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_hctz}}$ | `Flow_arli_hv_hctz` | flow arterial shunts | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{Chv}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_hctz}}$ | `Flow_po_li_hctz` | outflow po hydrochlorothiazide | $\mathrm{Cpo}_{\mathrm{hctz}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_hctz}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_hctz}}$ | `Flow_po_hv_hctz` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{hctz}} \longrightarrow \mathrm{Chv}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_hctz}}$ | `Flow_li_hv_hctz` | outflow liver hydrochlorothiazide | $\mathrm{Cli}_{\mathrm{plasma\_hctz}} \longrightarrow \mathrm{Chv}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_hctz}}$ | `Flow_hv_ve_hctz` | outflow hepatic vein hydrochlorothiazide | $\mathrm{Chv}_{\mathrm{hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_hctz}}$ | `Flow_ve_lu_hctz` | inflow lung hydrochlorothiazide | $\mathrm{Cve}_{\mathrm{hctz}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_hctz}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_hctz}}$ | `Flow_lu_ar_hctz` | outflow lung hydrochlorothiazide | $\mathrm{Clu}_{\mathrm{plasma\_hctz}} \longrightarrow \mathrm{Car}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_hctz}}$ | `Flow_ar_gu_hctz` | inflow gut hydrochlorothiazide | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_hctz}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_hctz}}$ | `Flow_gu_po_hctz` | outflow gut hydrochlorothiazide | $\mathrm{Cgu}_{\mathrm{plasma\_hctz}} \longrightarrow \mathrm{Cpo}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_hctz}}$ | `Flow_ar_re_hctz` | inflow rest hydrochlorothiazide | $\mathrm{Car}_{\mathrm{hctz}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_hctz}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_hctz}}$ | `Flow_re_ve_hctz` | outflow rest hydrochlorothiazide | $\mathrm{Cre}_{\mathrm{plasma\_hctz}} \longrightarrow \mathrm{Cve}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{KI\_\_HCTZEX}}$ | `KI__HCTZEX` | hydrochlorothiazide renal excretion | $\mathrm{Cki}_{\mathrm{plasma\_hctz}} \longrightarrow \mathrm{Aurine}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{GU\_\_HCTZABS}}$ | `GU__HCTZABS` | absorption hydrochlorothiazide | $\mathrm{Cgu}_{\mathrm{hctz}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_hctz}}$ |  |
| $v_{\mathrm{GU\_\_HCTZEXC}}$ | `GU__HCTZEXC` | excretion hydrochlorothiazide (feces) | $\mathrm{Cgu}_{\mathrm{hctz}} \longrightarrow \mathrm{Afeces}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{GU\_\_dissolution\_hctz}}$ | `GU__dissolution_hctz` | dissolution hydrochlorothiazide | $\varnothing \longrightarrow \mathrm{Cgu}_{\mathrm{hctz}}$ |  |
| $v_{\mathrm{GU\_\_application\_solution\_hctz}}$ | `GU__application_solution_hctz` | application of the solution hydrochlorothiazide | $\varnothing \longrightarrow \mathrm{Cgu}_{\mathrm{hctz}}$ |  |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{NA\_UPTAKE}} &= \frac{\mathrm{vin}_{\mathrm{na}} \cdot \mathrm{na}_{\mathrm{ref}}^{\mathrm{counter}_{\mathrm{gamma}}}}{\mathrm{na}^{\mathrm{counter}_{\mathrm{gamma}}}} \\[1ex]
v_{\mathrm{CL\_UPTAKE}} &= \frac{\mathrm{vin}_{\mathrm{cl}} \cdot \mathrm{cl}_{\mathrm{ref}}^{\mathrm{counter}_{\mathrm{gamma}}}}{\mathrm{cl}^{\mathrm{counter}_{\mathrm{gamma}}}} \\[1ex]
v_{\mathrm{NA\_FILTRATION}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{na} \\[1ex]
v_{\mathrm{NA\_EXCRETION}} &= k_{\mathrm{na}} \cdot \mathrm{na}_{\mathrm{loop}} \cdot \mathopen{}\left(1 + \frac{\frac{\mathrm{GFR}}{\mathrm{GFR}_{\mathrm{base}}} \cdot \mathrm{Emax}_{\mathrm{hctz\_na}} \cdot \max\mathopen{}\left(\mathrm{hctz}, 0\right)}{\max\mathopen{}\left(\mathrm{hctz}, 0\right) + \mathrm{E50}_{\mathrm{hctz\_nacl}}}\right) \\[1ex]
v_{\mathrm{NA\_REABSORPTION}} &= \mathrm{h2o}_{\mathrm{reabsorption}} \cdot \mathrm{na}_{\mathrm{loop}} \\[1ex]
v_{\mathrm{CL\_FILTRATION}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{cl} \\[1ex]
v_{\mathrm{CL\_EXCRETION}} &= k_{\mathrm{cl}} \cdot \mathrm{cl}_{\mathrm{loop}} \cdot \mathopen{}\left(1 + \frac{\frac{\mathrm{GFR}}{\mathrm{GFR}_{\mathrm{base}}} \cdot \mathrm{Emax}_{\mathrm{hctz\_cl}} \cdot \max\mathopen{}\left(\mathrm{hctz}, 0\right)}{\max\mathopen{}\left(\mathrm{hctz}, 0\right) + \mathrm{E50}_{\mathrm{hctz\_nacl}}}\right) \\[1ex]
v_{\mathrm{CL\_REABSORPTION}} &= \mathrm{h2o}_{\mathrm{reabsorption}} \cdot \mathrm{cl}_{\mathrm{loop}} \\[1ex]
v_{\mathrm{transport\_li\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cli}_{\mathrm{plasma\_hctz}} \cdot \mathrm{Kp}_{\mathrm{hctz}} - \mathrm{Cli}_{\mathrm{hctz}}\right) \\[1ex]
v_{\mathrm{transport\_lu\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_hctz}} \cdot \mathrm{Kp}_{\mathrm{hctz}} - \mathrm{Clu}_{\mathrm{hctz}}\right) \\[1ex]
v_{\mathrm{transport\_re\_hctz}} &= \frac{\mathrm{ftissue}_{\mathrm{hctz}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_hctz}} \cdot \mathrm{Kp}_{\mathrm{hctz}} - \mathrm{Cre}_{\mathrm{hctz}}\right) \\[1ex]
v_{\mathrm{iv\_hctz}} &= \frac{\mathrm{Ki}_{\mathrm{hctz}} \cdot \mathrm{IVDOSE}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_hctz}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_hctz}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_hctz}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_hctz}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_hctz}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_hctz}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_hctz}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_hctz}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_hctz}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_hctz}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_hctz}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_hctz}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_hctz}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_hctz}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_hctz}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_hctz}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_hctz}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{hctz}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_hctz}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_hctz}} \\[1ex]
v_{\mathrm{KI\_\_HCTZEX}} &= v_{\mathrm{HCTZEX}} \\[1ex]
v_{\mathrm{GU\_\_HCTZABS}} &= \mathrm{GU}_{\mathrm{\_F\_hctz\_abs}} \cdot \mathrm{GU}_{\mathrm{\_absorption}} \\[1ex]
v_{\mathrm{GU\_\_HCTZEXC}} &= \mathopen{}\left(1 - \mathrm{GU}_{\mathrm{\_F\_hctz\_abs}}\right) \cdot \mathrm{GU}_{\mathrm{\_absorption}} \\[1ex]
v_{\mathrm{GU\_\_dissolution\_hctz}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{GU}_{\mathrm{\_POSTOMACH\_hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}} \\[1ex]
v_{\mathrm{GU\_\_application\_solution\_hctz}} &= \frac{\frac{\mathrm{GU}_{\mathrm{\_Ka\_application\_hctz}}}{60} \cdot \mathrm{POSOLUTION}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{ECF}}{\mathrm{d} t} &= \mathrm{H2O}_{\mathrm{UPTAKE}} - \mathrm{vout}_{\mathrm{h2o}} - \mathrm{GFR} \cdot 0.001 + \mathrm{h2o}_{\mathrm{reabsorption}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Vloop}}{\mathrm{d} t} &= \mathrm{GFR} \cdot 0.001 - \mathrm{diuresis} - \mathrm{h2o}_{\mathrm{reabsorption}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Vurine}}{\mathrm{d} t} &= \mathrm{diuresis} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{na}}{\mathrm{d} t} &= \frac{v_{\mathrm{NA\_UPTAKE}} - v_{\mathrm{NA\_FILTRATION}} + v_{\mathrm{NA\_REABSORPTION}}}{\mathrm{ECF}} - \frac{\mathrm{na}}{\mathrm{ECF}} \cdot \frac{\mathrm{d} \,\mathrm{ECF}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{na}_{\mathrm{loop}}}{\mathrm{d} t} &= \frac{v_{\mathrm{NA\_FILTRATION}} - v_{\mathrm{NA\_EXCRETION}} - v_{\mathrm{NA\_REABSORPTION}}}{\mathrm{Vloop}} - \frac{\mathrm{na}_{\mathrm{loop}}}{\mathrm{Vloop}} \cdot \frac{\mathrm{d} \,\mathrm{Vloop}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{na}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{NA\_EXCRETION}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cl}}{\mathrm{d} t} &= \frac{v_{\mathrm{CL\_UPTAKE}} - v_{\mathrm{CL\_FILTRATION}} + v_{\mathrm{CL\_REABSORPTION}}}{\mathrm{ECF}} - \frac{\mathrm{cl}}{\mathrm{ECF}} \cdot \frac{\mathrm{d} \,\mathrm{ECF}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cl}_{\mathrm{loop}}}{\mathrm{d} t} &= \frac{v_{\mathrm{CL\_FILTRATION}} - v_{\mathrm{CL\_EXCRETION}} - v_{\mathrm{CL\_REABSORPTION}}}{\mathrm{Vloop}} - \frac{\mathrm{cl}_{\mathrm{loop}}}{\mathrm{Vloop}} \cdot \frac{\mathrm{d} \,\mathrm{Vloop}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cl}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{CL\_EXCRETION}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_hctz}} - v_{\mathrm{Flow\_ki\_ve\_hctz}} - v_{\mathrm{KI\_\_HCTZEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_hctz}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_li\_hctz}} + v_{\mathrm{Flow\_arli\_li\_hctz}} + v_{\mathrm{Flow\_po\_li\_hctz}} - v_{\mathrm{Flow\_li\_hv\_hctz}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_hctz}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_hctz}} + v_{\mathrm{Flow\_ve\_lu\_hctz}} - v_{\mathrm{Flow\_lu\_ar\_hctz}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_hctz}} - v_{\mathrm{Flow\_gu\_po\_hctz}} + v_{\mathrm{GU\_\_HCTZABS}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_hctz}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_hctz}} + v_{\mathrm{Flow\_ar\_re\_hctz}} - v_{\mathrm{Flow\_re\_ve\_hctz}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_hctz}} - v_{\mathrm{Flow\_arli\_li\_hctz}} - v_{\mathrm{Flow\_arli\_hv\_hctz}} + v_{\mathrm{Flow\_lu\_ar\_hctz}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_hctz}} - v_{\mathrm{Flow\_ar\_re\_hctz}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{iv\_hctz}} + v_{\mathrm{Flow\_ki\_ve\_hctz}} + v_{\mathrm{Flow\_hv\_ve\_hctz}} - v_{\mathrm{Flow\_ve\_lu\_hctz}} \\
&\quad {} + v_{\mathrm{Flow\_re\_ve\_hctz}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_hctz}} - v_{\mathrm{Flow\_po\_hv\_hctz}} + v_{\mathrm{Flow\_gu\_po\_hctz}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_hctz}} + v_{\mathrm{Flow\_po\_hv\_hctz}} + v_{\mathrm{Flow\_li\_hv\_hctz}} - v_{\mathrm{Flow\_hv\_ve\_hctz}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_li\_hctz}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_hctz}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_hctz}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{hctz}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_HCTZEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{hctz}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_HCTZEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{hctz}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{GU\_\_HCTZABS}} - v_{\mathrm{GU\_\_HCTZEXC}} + v_{\mathrm{GU\_\_dissolution\_hctz}} + v_{\mathrm{GU\_\_application\_solution\_hctz}}}{\mathrm{Vgu}_{\mathrm{lumen}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{hctz}}}{\mathrm{d} t} &= -\mathrm{GU}_{\mathrm{\_application\_hctz}} \cdot \mathrm{Mr}_{\mathrm{hctz}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{POSOLUTION}_{\mathrm{hctz}}}{\mathrm{d} t} &= -v_{\mathrm{GU\_\_application\_solution\_hctz}} \cdot \mathrm{Mr}_{\mathrm{hctz}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{IVDOSE}_{\mathrm{hctz}}}{\mathrm{d} t} &= -v_{\mathrm{iv\_hctz}} \cdot \mathrm{Mr}_{\mathrm{hctz}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_POSTOMACH\_hctz}}}{\mathrm{d} t} &= \mathopen{}\left(\mathrm{GU}_{\mathrm{\_application\_hctz}} - v_{\mathrm{GU\_\_dissolution\_hctz}}\right) \cdot \mathrm{Mr}_{\mathrm{hctz}} \qquad \text{(rate rule)}
\end{aligned}
$$

The concentration of a species in a compartment whose size changes is diluted by the rate of the size (SBML Level 3 Version 2, section 3.4.6), the amount it holds is kept.
