# Model for renal body fluid system for blood pressure regulation.

Model `hctz_fluid`, SBML Level 3 Version 2, read from hctz\_fluid.xml, written by sbmlode 0.3.0.

Model for blood pressure regulation based on extracellular fluid (ECF) volume and ion balance.

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
| $\mathrm{Vurine}$ | `Vurine` | urine | $10^{-6}$ | l |  |
| $\mathrm{Vki}$ | `Vki` | kidney | $\mathrm{NaN}$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{hctz}$ | `hctz` | hydrochlorothiazide | $\mathrm{ECF}$ | $0$ | mmol/l | concentration |
| $\mathrm{na}$ | `na` | Sodium (Na+) (ECF) | $\mathrm{ECF}$ | $140$ | mmol/l | concentration |
| $\mathrm{na}_{\mathrm{loop}}$ | `na_loop` | Sodium (Na+) (renal tubule) | $\mathrm{Vloop}$ | $140$ | mmol/l | concentration |
| $\mathrm{na}_{\mathrm{urine}}$ | `na_urine` | Sodium (Na+) (urine) | $\mathrm{Vurine}$ | $0$ | mmol | amount |
| $\mathrm{cl}$ | `cl` | Chloride (Cl-) (ECF) | $\mathrm{ECF}$ | $102$ | mmol/l | concentration |
| $\mathrm{cl}_{\mathrm{loop}}$ | `cl_loop` | Chloride (Cl-) (renal tubule) | $\mathrm{Vloop}$ | $102$ | mmol/l | concentration |
| $\mathrm{cl}_{\mathrm{urine}}$ | `cl_urine` | Chloride (Cl-) (urine) | $\mathrm{Vurine}$ | $0$ | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{BW}$ | `BW` | body weight | $75$ | kg | ✓ |
| $f_{\mathrm{renal\_function}}$ | `f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (base) | $100$ | ml/min | ✓ |
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
| $\mathrm{GFR}$ | `GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{vout}_{\mathrm{na}}$ | `vout_na` |  |  | mg/min |  |
| $\mathrm{vout}_{\mathrm{cl}}$ | `vout_cl` |  |  | mg/min |  |
| $\mathrm{H2O}_{\mathrm{UPTAKE}}$ | `H2O_UPTAKE` |  |  | l/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{na} &= \mathrm{na}_{\mathrm{ref}} \\[1ex]
\mathrm{cl} &= \mathrm{cl}_{\mathrm{ref}} \\[1ex]
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
\mathrm{GFR} &= f_{\mathrm{renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
\mathrm{H2O}_{\mathrm{UPTAKE}} &= \frac{\mathrm{vin}_{\mathrm{h2o}} \cdot \mathrm{ECF}_{\mathrm{ref}}^{\mathrm{counter}_{\mathrm{gamma}}}}{\mathrm{ECF}^{\mathrm{counter}_{\mathrm{gamma}}}} \\[1ex]
\mathrm{vout}_{\mathrm{na}} &= v_{\mathrm{NA\_EXCRETION}} \cdot \mathrm{Mr}_{\mathrm{na}} \\[1ex]
\mathrm{diuresis} &= \min\mathopen{}\left(\frac{\frac{k_{\mathrm{h2o}} \cdot \mathrm{GFR} \cdot \mathrm{ECF}^{\mathrm{counter}_{\mathrm{gamma}}}}{\mathrm{ECF}_{\mathrm{ref}}^{\mathrm{counter}_{\mathrm{gamma}}}} \cdot v_{\mathrm{NA\_EXCRETION}}}{\mathrm{vin}_{\mathrm{na}}}, f_{\mathrm{h2o\_max}} \cdot \mathrm{GFR} \cdot 0.001\right) \\[1ex]
\mathrm{h2o}_{\mathrm{reabsorption}} &= \mathrm{GFR} \cdot 0.001 - \mathrm{diuresis} \\[1ex]
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
v_{\mathrm{CL\_REABSORPTION}} &= \mathrm{h2o}_{\mathrm{reabsorption}} \cdot \mathrm{cl}_{\mathrm{loop}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{ECF}}{\mathrm{d} t} &= \mathrm{H2O}_{\mathrm{UPTAKE}} - \mathrm{vout}_{\mathrm{h2o}} - \mathrm{GFR} \cdot 0.001 + \mathrm{h2o}_{\mathrm{reabsorption}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Vloop}}{\mathrm{d} t} &= \mathrm{GFR} \cdot 0.001 - \mathrm{diuresis} - \mathrm{h2o}_{\mathrm{reabsorption}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Vurine}}{\mathrm{d} t} &= \mathrm{diuresis} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hctz}}{\mathrm{d} t} &= -\frac{\mathrm{hctz}}{\mathrm{ECF}} \cdot \frac{\mathrm{d} \,\mathrm{ECF}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{na}}{\mathrm{d} t} &= \frac{v_{\mathrm{NA\_UPTAKE}} - v_{\mathrm{NA\_FILTRATION}} + v_{\mathrm{NA\_REABSORPTION}}}{\mathrm{ECF}} - \frac{\mathrm{na}}{\mathrm{ECF}} \cdot \frac{\mathrm{d} \,\mathrm{ECF}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{na}_{\mathrm{loop}}}{\mathrm{d} t} &= \frac{v_{\mathrm{NA\_FILTRATION}} - v_{\mathrm{NA\_EXCRETION}} - v_{\mathrm{NA\_REABSORPTION}}}{\mathrm{Vloop}} - \frac{\mathrm{na}_{\mathrm{loop}}}{\mathrm{Vloop}} \cdot \frac{\mathrm{d} \,\mathrm{Vloop}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{na}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{NA\_EXCRETION}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cl}}{\mathrm{d} t} &= \frac{v_{\mathrm{CL\_UPTAKE}} - v_{\mathrm{CL\_FILTRATION}} + v_{\mathrm{CL\_REABSORPTION}}}{\mathrm{ECF}} - \frac{\mathrm{cl}}{\mathrm{ECF}} \cdot \frac{\mathrm{d} \,\mathrm{ECF}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cl}_{\mathrm{loop}}}{\mathrm{d} t} &= \frac{v_{\mathrm{CL\_FILTRATION}} - v_{\mathrm{CL\_EXCRETION}} - v_{\mathrm{CL\_REABSORPTION}}}{\mathrm{Vloop}} - \frac{\mathrm{cl}_{\mathrm{loop}}}{\mathrm{Vloop}} \cdot \frac{\mathrm{d} \,\mathrm{Vloop}}{\mathrm{d} t} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cl}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{CL\_EXCRETION}}
\end{aligned}
$$

The concentration of a species in a compartment whose size changes is diluted by the rate of the size (SBML Level 3 Version 2, section 3.4.6), the amount it holds is kept.
