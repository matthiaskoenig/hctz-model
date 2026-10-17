# Model for hydrochlorothiazide excretion into the urine

Model `hctz_kidney`, SBML Level 3 Version 2, read from hctz\_kidney.xml, written by sbmlode 0.3.0.

Model for hydrochlorothiazide renal excretion

"Renal dysfunction in patients with heart failure (HF) has traditionally been attributed to declining cardiac output and renal hypoperfusion. However, other central haemodynamic aberrations may contribute to impaired kidney function."\[Bobbio2022\]

"Diuresis (urine output) is closely linked to sodium (Na+) and chloride (Cl-) excretion, as these ions drive osmotic water reabsorption in the nephron; higher electrolyte excretion reduces reabsorption, increasing urine volume."

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
| $\mathrm{Vext}$ | `Vext` | plasma | $1$ | l | ✓ |
| $\mathrm{Vki}$ | `Vki` | kidney | $0.3$ | l | ✓ |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{hctz}_{\mathrm{ext}}$ | `hctz_ext` | hydrochlorothiazide (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{hctz}_{\mathrm{urine}}$ | `hctz_urine` | hydrochlorothiazide (urine) | $\mathrm{Vurine}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{renal\_function}}$ | `f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (base) | $100$ | ml/min | ✓ |
| $\mathrm{HCTZEX}_{\mathrm{f}}$ | `HCTZEX_f` | intrinsic renal clearance of hydrochlorothiazide relative to the GFR | $3.23772819218966$ | \- | ✓ |
| $v_{\mathrm{HCTZEX}}$ | `v_HCTZEX` | rate of HCTZ excretion |  | mmol/min |  |
| $\mathrm{GFR}$ | `GFR` | glomerular filtration rate |  | ml/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{hctz}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{GFR} &= f_{\mathrm{renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
v_{\mathrm{HCTZEX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{HCTZEX}_{\mathrm{f}} \cdot \mathrm{hctz}_{\mathrm{ext}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $\mathrm{HCTZEX}$ | `HCTZEX` | hydrochlorothiazide renal excretion | $\mathrm{hctz}_{\mathrm{ext}} \longrightarrow \mathrm{hctz}_{\mathrm{urine}}$ |

The rates of the reactions are:

$$
\begin{aligned}
\mathrm{HCTZEX} &= v_{\mathrm{HCTZEX}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{hctz}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-\mathrm{HCTZEX}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hctz}_{\mathrm{urine}}}{\mathrm{d} t} &= \mathrm{HCTZEX}
\end{aligned}
$$
