# Model for hydrochlorothiazide absorption in the small intestine

Model `hctz_intestine`, SBML Level 3 Version 2, read from hctz\_intestine.xml, written by sbmlode 0.3.0.

Model for hydrochlorothiazide absorption

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
| $\mathrm{Vgu}$ | `Vgu` | intestine | $1.2825$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen | $1.2825$ | l |  |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{hctz}_{\mathrm{lumen}}$ | `hctz_lumen` | hydrochlorothiazide (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{hctz}_{\mathrm{ext}}$ | `hctz_ext` | hydrochlorothiazide (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{hctz}_{\mathrm{feces}}$ | `hctz_feces` | hydrochlorothiazide (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $F_{\mathrm{hctz\_abs}}$ | `F_hctz_abs` | fraction absorbed hydrochlorothiazide | $0.7$ | \- | ✓ |
| $\mathrm{HCTZABS}_{\mathrm{k}}$ | `HCTZABS_k` | rate of hydrochlorothiazide absorption | $0.00507166463188506$ | 1/min | ✓ |
| $\mathrm{PODOSE}_{\mathrm{hctz}}$ | `PODOSE_hctz` | oral dose hydrochlorothiazide \[mg\] | $0$ | mg |  |
| $\mathrm{POSOLUTION}_{\mathrm{hctz}}$ | `POSOLUTION_hctz` | oral dose as solution hydrochlorothiazide \[mg\] | $0$ | mg |  |
| $\mathrm{POSTOMACH}_{\mathrm{hctz}}$ | `POSTOMACH_hctz` | oral dose in stomach hydrochlorothiazide \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{application\_hctz}}$ | `Ka_application_hctz` | Ka \[1/hr\] application hydrochlorothiazide | $1000$ | 1/hr | ✓ |
| $\mathrm{application}_{\mathrm{hctz}}$ | `application_hctz` | PO application hydrochlorothiazide |  | mmol/min |  |
| $\mathrm{Ka}_{\mathrm{dis\_hctz}}$ | `Ka_dis_hctz` | Ka\_dis \[1/hr\] dissolution hydrochlorothiazide | $2$ | 1/hr | ✓ |
| $\mathrm{Mr}_{\mathrm{hctz}}$ | `Mr_hctz` | Molecular weight hydrochlorothiazide \[g/mole\] | $297.7$ | g/mol | ✓ |
| $\mathrm{absorption}$ | `absorption` | absorption hydrochlorothiazide |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{hctz}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{absorption} &= \mathrm{HCTZABS}_{\mathrm{k}} \cdot \mathrm{Vlumen} \cdot \mathrm{hctz}_{\mathrm{lumen}} \\[1ex]
\mathrm{application}_{\mathrm{hctz}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{application\_hctz}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{HCTZABS}}$ | `HCTZABS` | absorption hydrochlorothiazide | $\mathrm{hctz}_{\mathrm{lumen}} \longrightarrow \mathrm{hctz}_{\mathrm{ext}}$ |
| $v_{\mathrm{HCTZEXC}}$ | `HCTZEXC` | excretion hydrochlorothiazide (feces) | $\mathrm{hctz}_{\mathrm{lumen}} \longrightarrow \mathrm{hctz}_{\mathrm{feces}}$ |
| $v_{\mathrm{dissolution\_hctz}}$ | `dissolution_hctz` | dissolution hydrochlorothiazide | $\varnothing \longrightarrow \mathrm{hctz}_{\mathrm{lumen}}$ |
| $v_{\mathrm{application\_solution\_hctz}}$ | `application_solution_hctz` | application of the solution hydrochlorothiazide | $\varnothing \longrightarrow \mathrm{hctz}_{\mathrm{lumen}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{HCTZABS}} &= F_{\mathrm{hctz\_abs}} \cdot \mathrm{absorption} \\[1ex]
v_{\mathrm{HCTZEXC}} &= \mathopen{}\left(1 - F_{\mathrm{hctz\_abs}}\right) \cdot \mathrm{absorption} \\[1ex]
v_{\mathrm{dissolution\_hctz}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{dis\_hctz}}}{60} \cdot \mathrm{POSTOMACH}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}} \\[1ex]
v_{\mathrm{application\_solution\_hctz}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{application\_hctz}}}{60} \cdot \mathrm{POSOLUTION}_{\mathrm{hctz}}}{\mathrm{Mr}_{\mathrm{hctz}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{hctz}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{HCTZABS}} - v_{\mathrm{HCTZEXC}} + v_{\mathrm{dissolution\_hctz}} + v_{\mathrm{application\_solution\_hctz}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hctz}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{HCTZABS}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hctz}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{HCTZEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{hctz}}}{\mathrm{d} t} &= -\mathrm{application}_{\mathrm{hctz}} \cdot \mathrm{Mr}_{\mathrm{hctz}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{POSOLUTION}_{\mathrm{hctz}}}{\mathrm{d} t} &= -v_{\mathrm{application\_solution\_hctz}} \cdot \mathrm{Mr}_{\mathrm{hctz}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{POSTOMACH}_{\mathrm{hctz}}}{\mathrm{d} t} &= \mathopen{}\left(\mathrm{application}_{\mathrm{hctz}} - v_{\mathrm{dissolution\_hctz}}\right) \cdot \mathrm{Mr}_{\mathrm{hctz}} \qquad \text{(rate rule)}
\end{aligned}
$$
