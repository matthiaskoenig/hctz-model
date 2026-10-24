#set page(paper: "a4", margin: 2cm)
#set text(size: 10pt)
#set heading(numbering: "1.1")
#set math.equation(numbering: "(1)")
// a table longer than a page continues on the next page, its
// caption above it and its header repeated
#show figure.where(kind: table): set block(breakable: true)
#show figure.where(kind: table): set figure.caption(position: top)

#align(center, text(size: 16pt, weight: "bold")[HCTZ PBPK\/PD model: fit PD])

= Methods: HCTZ PBPK\/PD model: fit PD

== Parameters and data

5 parameters were optimized: #raw("E50_hctz_nacl"), #raw("Emax_hctz_na"), #raw("Emax_hctz_cl"), #raw("k_na") and #raw("k_cl"). The parameters of the adopted fit PK\_20261017\_025702\_\_4167a were fixed at their fitted values.

A fit mapping is a curve of a study, the data and the observable of the model it is compared with. The fit has 77 fit mappings of training data with 166 data points, whose residuals enter the objective; and 8 fit mappings of validation data with 21 data points, which were simulated and evaluated with the fitted parameters but not fitted. The fit was set up and run with sbmlsim #cite(<Koenig2026_sbmlsim>).

== Objective function

The parameters were estimated by minimizing the objective function

$ F(arrow(p)) = 1/2 sum_k sum_i rho(w_(i,k) r_(i,k)(arrow(p))^2) $

where $k$ runs over the fit mappings of the training data and $i$ over their data points, $r_(i,k)$ is the residual, $w_(i,k) = w_k w^p_(i,k)$ the weight of the data point and $rho$ the loss function, applied to the squared weighted residual $z = w_(i,k) r_(i,k)^2$. The loss function is linear, $rho(z) = z$, i.e. a standard least squares problem.

The residuals are normalized by the mean $overline(y)_k$ of the data of their curve, which makes curves of different quantities and magnitudes comparable:

$ r_(i,k) = (y_(i,k) - f_k(x_(i,k), arrow(p))) / overline(y)_k $

The weight of curve $k$ is $w_k = n_k / N_k$, the weight $n_k$ of its fit mapping (the weight its fit mapping collection assigns, 1 by default, or, for a collection which uses the weights of its mappings, the weight of the mapping, by default the number of subjects of its data) divided by the number $N_k$ of its data points.

A data point is weighted with the inverse of its coefficient of variation, $w^p_(i,k) = |y_(i,k)| / sigma_(i,k)$, with $sigma_(i,k)$ the standard deviation of the data point, or its standard error for data without a standard deviation. An error of zero is missing, a missing error of a curve with errors is replaced by the largest error of the curve, and the data points of a curve without errors have the weight $w^p_(i,k) = 2$, the weight of a coefficient of variation of 0.5.

== Optimization

The optimizer searched the parameters in log10 space within their bounds; bounds, values and intervals are given in the units of the fit parameters, the units of the table of the parameters.

The objective was minimized in 3 runs with differential evolution #cite(<Storn1997>) of SciPy #cite(<Virtanen2020>) within the bounds of the parameters, with the strategy #raw("best1bin"), a population of 15 times the number of parameters, at most 1000 generations, the relative tolerance 0.01 of convergence, the recombination constant 0.7 and a mutation dithered between 0.5 and 1. The initial population of a run was drawn by latin hypercube sampling #cite(<McKay1979>), with a seed of every run derived from the seed 1234 of the fit. The best member of the final population was polished with the L-BFGS-B method of SciPy.

The convergence of the runs was assessed from the traces of their cost and the waterfall plot of their final costs, and the parameter set with the lowest cost was used.

The models were simulated with libRoadRunner #cite(<Welsh2023>) and its integrator CVODE #cite(<Hindmarsh2005>) with the relative tolerance $10^(-6)$ and the absolute tolerance $10^(-6)$, which for a species in a concentration is multiplied by the initial volume of its compartment. It ran with the variable step size of libRoadRunner, i.e. with an output at every step of the integrator. A data point at the time of a change after the start of a simulation, e.g. a dose or the reset of a collection, was compared with the state before the change, except the first data point of a curve with data at later times, which starts a collection and was compared with the state after the change.

== Goodness of fit

The goodness of fit is given per kind of data (training data and validation data) by metrics over its $n$ data points with the residuals $e_i = y_i - f(x_i, hat(arrow(p)))$ at the fitted parameters $hat(arrow(p))$, the mean squared error, its root and the root mean squared error normalized by the mean $overline(y)_(k(i))$ of the data of the curve of a point:

$ "MSE" = 1/n sum_(i=1)^n e_i^2, quad "RMSE" = sqrt("MSE"), quad "NRMSE" = sqrt(1/n sum_(i=1)^n (e_i / overline(y)_(k(i)))^2) $

The root mean square of the residuals of the objective, i.e. what the fit minimizes, and the coefficient of determination:

$ "RMSE"_w = sqrt(1/n sum_(i=1)^n rho(w_i r_i^2)), quad R^2 = 1 - (sum_i e_i^2) / (sum_i (y_i - overline(y))^2) $

The predictions of a non-linear model are no linear regression of the data, so $R^2$ can be negative: the prediction is worse than the mean of the data. The information criteria of Akaike #cite(<Akaike1974>) and Schwarz #cite(<Schwarz1978>) with the number $n_p$ of fitted parameters are those of a least squares fit with normally distributed residuals, up to an additive constant, so only differences between models fitted to the same data are meaningful:

$ "AIC" = n ln("MSE") + 2 n_p, quad "BIC" = n ln("MSE") + n_p ln(n) $

The percentage of the data points whose prediction $f_i = f(x_i, hat(arrow(p)))$ lies within twofold of the data is taken over the $n_(+)$ data points with positive data $y_i > 0$ and a positive prediction $f_i > 0$; the others have no ratio and are not counted, and a kind of data without such a point has no percentage:

$ P_2 = 100 / n_(+) abs(\{ i : 1/2 <= f_i / y_i <= 2 \}) $

The goodness of fit plot shows the predictions against the data on logarithmic axes, with the lines of twofold $f = 2y$ and $f = y/2$. The Bland-Altman plot #cite(<Bland1986>) shows the ratio of prediction and data as $d_i = log_10(f_i / y_i)$ against the geometric mean $sqrt(f_i y_i)$ for the data points with positive values, with the bias $overline(d)$ and the limits of agreement $overline(d) plus.minus 1.96 s_d$, with the sample standard deviation $s_d$ of $d_i$, of the training data; they are read as the fold factors $10^(overline(d))$ and $10^(overline(d) plus.minus 1.96 s_d)$.

== Identifiability

The identifiability of the parameters was analysed with the profile likelihood #cite(<Raue2009>) #cite(<Kreutz2013>). The profile of a parameter is the lowest objective with the parameter fixed:

$ "PL"(p_j) = min_(p_(l != j)) F(arrow(p)) $

At every point of a scan the other parameters were re-optimized from the previous point with the least squares optimizer of SciPy with the relative step 0.05. A scan ran from the optimum in both directions in the space of the optimizer, with steps in decades of the parameter, starting at 0.1. A step which raised the objective by more than 0.2 of the distance between the objective at the optimum and the threshold was reduced by the factor 2 and repeated, down to 0.01, and the step after one which raised it by less than that divided by the factor was enlarged by the factor, up to 1. A scan stopped at the threshold, at the bound of the parameter, at a point which failed or after 50 points.

The confidence intervals are the values at which the profile crosses the threshold of the likelihood ratio test

$ F_"thr" = F_"min" + chi^2_alpha ("df") / 2 $

with $F_"min"$ the lowest objective of the fit and of all profiles and $chi^2_alpha ("df")$ the quantile of the $chi^2$ distribution at the confidence level $alpha = 0.95$ with df \= 1 degrees of freedom, i.e. 1.92 above the lowest objective. The threshold has this confidence level if $F$ is the negative log-likelihood of the data up to a constant, i.e. if the weighted residuals are independent and normally distributed with unit variance; otherwise the level is approximate. A crossing is interpolated between two points of the profile, on the logarithm of a parameter on a logarithmic scale. A parameter is identifiable if its profile reaches the threshold within the scan on both sides of the optimum, i.e. its confidence interval is finite; practically non-identifiable towards the lower bound if its profile reaches the threshold above the optimum but not below it within the scan, which ends at the lower bound or after 50 points; practically non-identifiable towards the upper bound if its profile reaches the threshold below the optimum but not above it within the scan, which ends at the upper bound or after 50 points; practically non-identifiable if its profile reaches the threshold on neither side within the scans, which end at the bounds or after 50 points, and is not flat; and structurally non-identifiable if its profile is flat on both sides. A side of a profile is flat if it rises by less than 0.05 of the distance between the lowest objective and the threshold, and a profile with a point which failed or did not converge is not classified. The profile likelihood is preferred over the intervals of the Fisher information, its intervals are invariant under a transformation of the parameters and can be asymmetric #cite(<Wieland2021>).

The Fisher information is the local alternative to the profiles: it is the Gauss-Newton approximation of the curvature of the objective at the optimum, from the Jacobian $J$ of the weighted residuals of the training data with respect to the parameters $arrow(p)$ in the space of the optimizer, computed by central finite differences with the step $h_j = epsilon max(|p_j|, 1), space epsilon = 10^(-6)$ of the parameter $p_j$:

$ I = J^top J, quad "cov" = sigma^2 I^(-1), quad sigma^2 = (2 F) / (n - n_p) $

with the number $n$ of data points of the training data and the number $n_p$ of parameters. The information has rank 5 of 5, the number of its eigenvalues above $10^(-8)$ of the largest one, and the condition number 85.5; the covariance of an information of a lower rank is computed with the pseudo-inverse. The Wald intervals are $hat(p)_j plus.minus t_((1+alpha)/2, n-n_p) "SE"_j$ with the standard errors $"SE"_j = sqrt("cov"_(j j))$ at the confidence level $alpha = 0.95$, transformed back into the units of the fit parameters.

== Provenance

The fit PD\_20261017\_030352\_\_10c1d was run on 2026-10-17 01:03:57 UTC with sbmlsim 0.10.0 #cite(<Koenig2026_sbmlsim>), libRoadRunner 2.10.0 #cite(<Welsh2023>), SciPy 1.18.1 #cite(<Virtanen2020>), NumPy 2.5.3 #cite(<Harris2020>) and Python 3.14.8 (seed 1234). The models and data were those of commit #raw("02b4b5c535fd42d63a6e025f407656229ea2a747") of #raw("/home/mkoenig/git/pkdb_models") with uncommitted changes; their SHA-256 checksums are listed in #ref(<tab:checksums:PD_20261017_030352__10c1d>). The fit kept the values #raw("ftissue_hctz") \= 0.0637161, #raw("Kp_hctz") \= 2.36426, #raw("KI__HCTZEX_f") \= 3.23773, #raw("Ka_dis_hctz") \= 1.30141 and #raw("GU__HCTZABS_k") \= 0.00507166 of the model fixed.

#figure(
  table(
  columns: 2,
  align: (left, left,),
  table.header([File], [SHA-256]),
  raw("pkdb_models/models/hctz/data/aliskiren/Vaidyanathan2006/.Vaidyanathan2006_Fig2.tsv"),
  raw("4b882f62be16..."),
  raw("pkdb_models/models/hctz/data/aliskiren/Vaidyanathan2006/.Vaidyanathan2006_Fig3.tsv"),
  raw("b5395aea7661..."),
  raw("pkdb_models/models/hctz/data/aliskiren/Vaidyanathan2006/.Vaidyanathan2006_Fig4.tsv"),
  raw("a666a94594f2..."),
  raw("pkdb_models/models/hctz/data/aliskiren/Vaidyanathan2006/.Vaidyanathan2006_Tab2.tsv"),
  raw("e5b023387a7c..."),
  raw("pkdb_models/models/hctz/data/aliskiren/Vaidyanathan2006/.Vaidyanathan2006_Tab3.tsv"),
  raw("6415639e32b1..."),
  raw("pkdb_models/models/hctz/data/aliskiren/Vaidyanathan2006/.Vaidyanathan2006_TabGroups.tsv"),
  raw("e17dd76d2768..."),
  raw("pkdb_models/models/hctz/data/aliskiren/Vaidyanathan2006/.Vaidyanathan2006_TabInterventions.tsv"),
  raw("084628fe174a..."),
  raw("pkdb_models/models/hctz/data/canagliflozin/Devineni2014/.Devineni2014_Fig2.tsv"),
  raw("7ed32853872f..."),
  raw("pkdb_models/models/hctz/data/canagliflozin/Devineni2014/.Devineni2014_Fig3.tsv"),
  raw("ba3c236103c1..."),
  raw("pkdb_models/models/hctz/data/canagliflozin/Devineni2014/.Devineni2014_Tab1.tsv"),
  raw("096cbdc6db9e..."),
  raw("pkdb_models/models/hctz/data/canagliflozin/Devineni2014/.Devineni2014_Tab2.tsv"),
  raw("c5d09da767d6..."),
  raw("pkdb_models/models/hctz/data/canagliflozin/Devineni2014/.Devineni2014_Tab2A.tsv"),
  raw("c6dda93b2bbf..."),
  raw("pkdb_models/models/hctz/data/canagliflozin/Devineni2014/.Devineni2014_TabGroups.tsv"),
  raw("7b29e1f269b4..."),
  raw("pkdb_models/models/hctz/data/canagliflozin/Devineni2014/.Devineni2014_TabInterventions.tsv"),
  raw("e0063bf738d2..."),
  raw("pkdb_models/models/hctz/data/enalapril/Niopas2011/.Niopas2011_Fig1.tsv"),
  raw("a42bd89511f5..."),
  raw("pkdb_models/models/hctz/data/enalapril/Niopas2011/.Niopas2011_Fig2.tsv"),
  raw("d28da761910c..."),
  raw("pkdb_models/models/hctz/data/enalapril/Niopas2011/.Niopas2011_Tab2.tsv"),
  raw("083e057dd8d2..."),
  raw("pkdb_models/models/hctz/data/enalapril/Niopas2011/.Niopas2011_Tab3.tsv"),
  raw("8b7e9d21a561..."),
  raw("pkdb_models/models/hctz/data/enalapril/Niopas2011/.Niopas2011_TabGroups.tsv"),
  raw("0264a6f8c5c8..."),
  raw("pkdb_models/models/hctz/data/enalapril/Niopas2011/.Niopas2011_TabInterventions.tsv"),
  raw("7e44753b6aa6..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Anderson1961/.Anderson1961_Tab1.tsv"),
  raw("0b96662f4794..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Anderson1961/.Anderson1961_Tab1A.tsv"),
  raw("ddb7c92add6e..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Anderson1961/.Anderson1961_Tab1B.tsv"),
  raw("5dad76e537a1..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Anderson1961/.Anderson1961_TabGroups.tsv"),
  raw("1d517cac3d89..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Anderson1961/.Anderson1961_TabIndividuals.tsv"),
  raw("9468bc219f5e..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Anderson1961/.Anderson1961_TabInterventions.tsv"),
  raw("c3245d431e24..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Azumaya1990/.Azumaya1990_Fig3.tsv"),
  raw("ead505237a28..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Azumaya1990/.Azumaya1990_TabGroups.tsv"),
  raw("3d24752729ca..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Azumaya1990/.Azumaya1990_TabInterventions.tsv"),
  raw("9d6d47aeb522..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982/.Barbhaiya1982_Fig1.tsv"),
  raw("4f85c3948a47..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982/.Barbhaiya1982_Fig2.tsv"),
  raw("1a0c037cf194..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982/.Barbhaiya1982_Fig3.tsv"),
  raw("c5480ff6b536..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982/.Barbhaiya1982_Fig5.tsv"),
  raw("2367b86e69cb..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982/.Barbhaiya1982_Tab1.tsv"),
  raw("71d41f5bf888..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982/.Barbhaiya1982_TabGroups.tsv"),
  raw("1c678a4589a5..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982/.Barbhaiya1982_TabInterventions.tsv"),
  raw("069e892ea59b..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982a/.Barbhaiya1982a_Tab1.tsv"),
  raw("e910986f2e22..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982a/.Barbhaiya1982a_Tab2.tsv"),
  raw("3dbbeef29ba0..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982a/.Barbhaiya1982a_Tab3.tsv"),
  raw("e3183d391872..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982a/.Barbhaiya1982a_TabGroups.tsv"),
  raw("c227d8c7b0f8..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Barbhaiya1982a/.Barbhaiya1982a_TabInterventions.tsv"),
  raw("3c6fd578a468..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1976/.Beermann1976_Fig2.tsv"),
  raw("2807904243da..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1976/.Beermann1976_Fig3.tsv"),
  raw("d5ce6e1099f8..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1976/.Beermann1976_Tab1.tsv"),
  raw("fb16ac2a9245..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1976/.Beermann1976_Tab1A.tsv"),
  raw("d5a0f6178115..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1976/.Beermann1976_TabGroups.tsv"),
  raw("e1b9eecde8ab..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1976/.Beermann1976_TabIndividuals.tsv"),
  raw("7bdd5f3efc78..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1976/.Beermann1976_TabInterventions.tsv"),
  raw("756ad10cf430..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_Fig1_2.tsv"),
  raw("8135a1aef6a4..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_Fig3.tsv"),
  raw("9b8aecc3043d..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_Fig4.tsv"),
  raw("45eb63754276..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_Fig5.tsv"),
  raw("ce4223f8d147..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_Fig5tc.tsv"),
  raw("ef1a309635e7..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_Tab3.tsv"),
  raw("9ed1f48b705a..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_Tab4.tsv"),
  raw("64c35907cf12..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_Tab4mean.tsv"),
  raw("42a9478560e8..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_TabGroups.tsv"),
  raw("e1a2a61ff2cd..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_TabIndividuals.tsv"),
  raw("d02c16eca30a..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1977a/.Beermann1977a_TabInterventions.tsv"),
  raw("0dbb93f4c798..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1979/.Beermann1979_Fig1.tsv"),
  raw("77696706cdc8..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1979/.Beermann1979_Tab2.tsv"),
  raw("00ecc7bc09f2..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1979/.Beermann1979_Tab3.tsv"),
  raw("f08b3337f300..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1979/.Beermann1979_TabGroups.tsv"),
  raw("eb6901a5ec90..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1979/.Beermann1979_TabIndividuals.tsv"),
  raw("eae34c5a0b0e..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Beermann1979/.Beermann1979_TabInterventions.tsv"),
  raw("05987a4ccfb5..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Dussol2005/.Dussol2005_Tab2.tsv"),
  raw("75b8326b1131..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Dussol2005/.Dussol2005_Tab3.tsv"),
  raw("cd2268796116..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Dussol2005/.Dussol2005_TabGroups.tsv"),
  raw("68166df9b390..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Dussol2005/.Dussol2005_TabIndividuals.tsv"),
  raw("b7872677dd09..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Dussol2005/.Dussol2005_TabInterventions.tsv"),
  raw("02019f8d2382..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Ernst2006/.Ernst2006_Fig1.tsv"),
  raw("a994fecc105d..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_Fig1.tsv"),
  raw("a7441ff279b1..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_Fig2.tsv"),
  raw("eb43d99d1abf..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_Fig3.tsv"),
  raw("18912daaff30..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_Fig4.tsv"),
  raw("ff67b5f49cbc..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_Fig5.tsv"),
  raw("ee2adf35ff0b..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_Tab2.tsv"),
  raw("06b166899abe..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_Tab4.tsv"),
  raw("4b470bc80366..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_TabGroups.tsv"),
  raw("29d958be9670..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_TabIndividuals.tsv"),
  raw("ef74d1ac3e12..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Giudicelli1987/.Giudicelli1987_TabInterventions.tsv"),
  raw("9582c22f6643..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Heise2015/.Heise2015_Fig2.tsv"),
  raw("f4935dc54371..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Heise2015/.Heise2015_Fig3.tsv"),
  raw("3f208e2a31a5..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Heise2015/.Heise2015_Fig4.tsv"),
  raw("8a0cb6a070e5..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Heise2015/.Heise2015_Tab1.tsv"),
  raw("f1f21b9bf441..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Heise2015/.Heise2015_Tab3.tsv"),
  raw("b87e4c93ab81..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Heise2015/.Heise2015_Tab3A.tsv"),
  raw("0de829681d4f..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Heise2015/.Heise2015_Tab4.tsv"),
  raw("1f6fecb5eea0..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Heise2015/.Heise2015_TabGroups.tsv"),
  raw("d77f4251d594..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Heise2015/.Heise2015_TabInterventions.tsv"),
  raw("36a7fdc8e888..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Howes1991/.Howes1991_Fig1.tsv"),
  raw("87a1bcadd50e..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Howes1991/.Howes1991_Tab1.tsv"),
  raw("8a9ea4517461..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Howes1991/.Howes1991_Tab2.tsv"),
  raw("82f669940103..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Howes1991/.Howes1991_Tab3.tsv"),
  raw("5b8962c88ee3..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Howes1991/.Howes1991_TabGroups.tsv"),
  raw("67c05dd8e03d..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Howes1991/.Howes1991_TabInterventions.tsv"),
  raw("02941e5da0c2..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hsiao2015/.Hsiao2015_Fig1.tsv"),
  raw("64fd8ab77b40..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hsiao2015/.Hsiao2015_Tab1.tsv"),
  raw("00ce0500feca..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hsiao2015/.Hsiao2015_TabGroups.tsv"),
  raw("564ae62fbfd3..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hsiao2015/.Hsiao2015_TabInterventions.tsv"),
  raw("a5793f71d672..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hunninghake1986/.Hunninghake1986_Fig1.tsv"),
  raw("b784bcb3e9ad..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hunninghake1986/.Hunninghake1986_Fig2.tsv"),
  raw("c76172d843b0..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hunninghake1986/.Hunninghake1986_Fig3.tsv"),
  raw("394c3b42e8e4..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hunninghake1986/.Hunninghake1986_Tab2.tsv"),
  raw("0f92641bead3..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hunninghake1986/.Hunninghake1986_TabGroups.tsv"),
  raw("23883b9fb900..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Hunninghake1986/.Hunninghake1986_TabInterventions.tsv"),
  raw("68dde1a2a141..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Januszewicz1959/.Januszewicz1959_Fig2tc.tsv"),
  raw("44fc27e9b75f..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Januszewicz1959/.Januszewicz1959_Tab1.tsv"),
  raw("df66df0654ff..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Januszewicz1959/.Januszewicz1959_TabGroups.tsv"),
  raw("b432c9f59ea3..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Januszewicz1959/.Januszewicz1959_TabIndividuals.tsv"),
  raw("c6d9b60bbaa6..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Januszewicz1959/.Januszewicz1959_TabInterventions.tsv"),
  raw("fcb6d290080b..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jeon2012/.Jeon2012_Fig3.tsv"),
  raw("5d13f75a5a76..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jeon2012/.Jeon2012_Fig4.tsv"),
  raw("8041d6538ced..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jeon2012/.Jeon2012_Fig5.tsv"),
  raw("c98f449945e9..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jeon2012/.Jeon2012_Fig6.tsv"),
  raw("77ead1fbfcdd..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jeon2012/.Jeon2012_Tab2.tsv"),
  raw("4cb2bde69cc3..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jeon2012/.Jeon2012_TabGroups.tsv"),
  raw("4ed151ca9458..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jeon2012/.Jeon2012_TabInterventions.tsv"),
  raw("2743ddcea85b..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jordo1979/.Jordo1979_Fig1.tsv"),
  raw("eecd7245850d..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jordo1979/.Jordo1979_Fig2.tsv"),
  raw("f41b81f187f2..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jordo1979/.Jordo1979_Tab1.tsv"),
  raw("cddc1c86b8b9..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jordo1979/.Jordo1979_Tab2.tsv"),
  raw("0379d6aaaa5a..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jordo1979/.Jordo1979_Tab2Mean.tsv"),
  raw("8d876091a4eb..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jordo1979/.Jordo1979_TabGroups.tsv"),
  raw("9daa6d6555b0..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jordo1979/.Jordo1979_TabIndividuals.tsv"),
  raw("679da5cce1b0..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Jordo1979/.Jordo1979_TabInterventions.tsv"),
  raw("06d6eca836c2..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Knauf1995/.Knauf1995_Fig1.tsv"),
  raw("fbcd718e5f2c..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Knauf1995/.Knauf1995_Fig2.tsv"),
  raw("dc5617d97660..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Knauf1995/.Knauf1995_Fig3.tsv"),
  raw("5763164aec01..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Knauf1995/.Knauf1995_Fig4.tsv"),
  raw("911aa1a1e89d..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Knauf1995/.Knauf1995_Fig5.tsv"),
  raw("6141428da0e1..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Knauf1995/.Knauf1995_Tab2.tsv"),
  raw("a62e96697a27..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Knauf1995/.Knauf1995_TabGroups.tsv"),
  raw("cec858380cf8..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Knauf1995/.Knauf1995_TabIndividuals.tsv"),
  raw("7311c65ddbec..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Knauf1995/.Knauf1995_TabInterventions.tsv"),
  raw("65762172be82..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Niemeyer1983/.Niemeyer1983_Fig1.tsv"),
  raw("58c88431c8b8..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Niemeyer1983/.Niemeyer1983_Fig2.tsv"),
  raw("f730db99af80..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Niemeyer1983/.Niemeyer1983_Fig3.tsv"),
  raw("fe160c3a04cc..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Niemeyer1983/.Niemeyer1983_Tab3.tsv"),
  raw("36768c2c955c..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Niemeyer1983/.Niemeyer1983_TabGroups.tsv"),
  raw("17d5aa23ed83..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Niemeyer1983/.Niemeyer1983_TabIndividuals.tsv"),
  raw("9d95d6859878..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Niemeyer1983/.Niemeyer1983_TabInterventions.tsv"),
  raw("a9993f8762dd..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Nilsen1989/.Nilsen1989_Fig1.tsv"),
  raw("f9095f95471e..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Nilsen1989/.Nilsen1989_Fig2.tsv"),
  raw("71223ba3b02f..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Nilsen1989/.Nilsen1989_Fig3.tsv"),
  raw("e5c1f8ad9c2b..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Nilsen1989/.Nilsen1989_Fig4.tsv"),
  raw("b4be3f4c6da0..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Nilsen1989/.Nilsen1989_Fig5.tsv"),
  raw("f982121b79f6..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Nilsen1989/.Nilsen1989_Tab1.tsv"),
  raw("db3193becc56..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Nilsen1989/.Nilsen1989_TabGroups.tsv"),
  raw("4d9afd8ecc3c..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Nilsen1989/.Nilsen1989_TabInterventions.tsv"),
  raw("1ffefd2c38cf..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Patel1984/.Patel1984_Fig1.tsv"),
  raw("492138f96021..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Patel1984/.Patel1984_Fig2.tsv"),
  raw("146b2c18c2bd..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Patel1984/.Patel1984_Tab2.tsv"),
  raw("7007b5bbbe0e..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Patel1984/.Patel1984_Tab4.tsv"),
  raw("d6c5d9e1dee9..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Patel1984/.Patel1984_TabGroups.tsv"),
  raw("cf0bada6496e..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Patel1984/.Patel1984_TabInterventions.tsv"),
  raw("a7448276e496..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Ripley2000/.Ripley2000_Fig1_2.tsv"),
  raw("349ae182f694..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Ripley2000/.Ripley2000_Fig2.tsv"),
  raw("f944d94feb78..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Ripley2000/.Ripley2000_Fig3.tsv"),
  raw("20e3805d7769..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Ripley2000/.Ripley2000_Tab3.tsv"),
  raw("e3871f9fabdc..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Ripley2000/.Ripley2000_TabGroups.tsv"),
  raw("223f701288a6..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Ripley2000/.Ripley2000_TabInterventions.tsv"),
  raw("cf973e21bbcb..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Weir1998/.Weir1998_Fig2.tsv"),
  raw("4d781066aac0..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Weir1998/.Weir1998_Fig3.tsv"),
  raw("c3ba0214b53b..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Weir1998/.Weir1998_Tab3.tsv"),
  raw("65c6ff1c8c7a..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Weir1998/.Weir1998_Tab4.tsv"),
  raw("822c640eed5a..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Weir1998/.Weir1998_TabGroups.tsv"),
  raw("a52f9f3880a7..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Weir1998/.Weir1998_TabInterventions.tsv"),
  raw("9c3826e429da..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Fig2.tsv"),
  raw("cfda53e0bc71..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Fig2A.tsv"),
  raw("8d9332b11962..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Fig2B.tsv"),
  raw("2bc1ea3c8faa..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Fig2C.tsv"),
  raw("7f28e773d2dc..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Fig2sc.tsv"),
  raw("8d9332b11962..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Fig3.tsv"),
  raw("b7f69903770e..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Fig3A.tsv"),
  raw("2e4214b536ca..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Fig3B.tsv"),
  raw("c1a6d5b88f7a..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Tab1.tsv"),
  raw("7880d1048cd6..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_Tab2.tsv"),
  raw("142ccecd0aac..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_TabGroups.tsv"),
  raw("be5b1f862ad7..."),
  raw("pkdb_models/models/hctz/data/hydrochlorothiazide/Williams1982/.Williams1982_TabInterventions.tsv"),
  raw("bd50b21b1457..."),
  raw("pkdb_models/models/hctz/data/lisinopril/Koytchev2004/.Koytchev2004_Fig1.tsv"),
  raw("5ed8ba49e6dc..."),
  raw("pkdb_models/models/hctz/data/lisinopril/Koytchev2004/.Koytchev2004_Fig2.tsv"),
  raw("8d2e06479531..."),
  raw("pkdb_models/models/hctz/data/lisinopril/Koytchev2004/.Koytchev2004_Tab1.tsv"),
  raw("86e50f974b9f..."),
  raw("pkdb_models/models/hctz/data/lisinopril/Koytchev2004/.Koytchev2004_Tab3.tsv"),
  raw("742f83ae1f39..."),
  raw("pkdb_models/models/hctz/data/lisinopril/Koytchev2004/.Koytchev2004_TabGroups.tsv"),
  raw("9a4ff71bdd31..."),
  raw("pkdb_models/models/hctz/data/lisinopril/Koytchev2004/.Koytchev2004_TabInterventions.tsv"),
  raw("1b45614b4423..."),
  raw("pkdb_models/models/hctz/models/output/models/hctz_body_flat.xml"),
  raw("a8c0d649dbe1..."),
  ),
  caption: [SHA-256 checksums of the models and data of the fit PD\_20261017\_030352\_\_10c1d, their first 12 characters; the full checksums are in the provenance of the result (optimization\_result.json).],
) <tab:checksums:PD_20261017_030352__10c1d>

= Results: HCTZ PBPK\/PD model: fit PD

== Parameters

#figure(
  table(
  columns: 6,
  align: (left, left, right, left, right, left,),
  table.header([Parameter], [Description], [Value \[95% CI\]], [Unit], [Bounds], [Identifiable]),
  raw("E50_hctz_nacl"),
  [],
  [8.62e-05 \[2.86e-05, 0.000289\]],
  [mmol\/l],
  [\[1e-06, 0.01\]],
  [yes],
  raw("Emax_hctz_na"),
  [],
  [1.73 \[1.25, 2.6\]],
  [dimensionless],
  [\[0.1, 5\]],
  [yes],
  raw("Emax_hctz_cl"),
  [],
  [0.457 \[0.312, 0.768\]],
  [dimensionless],
  [\[0.1, 5\]],
  [yes],
  raw("k_na"),
  [],
  [0.000677 \[0.000584, 0.000788\]],
  [l\/min],
  [\[0.00025, 0.0015\]],
  [yes],
  raw("k_cl"),
  [],
  [0.00371 \[0.00252, 0.00512\]],
  [l\/min],
  [\[0.00034, 0.007\]],
  [yes],
  ),
  caption: [Parameters of the fit PD\_20261017\_030352\_\_10c1d, the parameter set PD\_20261017\_030352\_\_10c1d\_0, cost 65.1, with their bounds in the optimization. The 95% confidence intervals are those of the profile likelihood, LB and UB an interval which is open towards the lower or the upper bound, and the Wald intervals of the Fisher information for a parameter without a profile. Identifiable is the classification of the profile: yes, no (LB) or no (UB) if the profile does not reach the threshold towards the lower or the upper bound, no if it reaches it on neither side, structural if it is flat.],
) <tab:parameters:PD_20261017_030352__10c1d>

== Data

#figure(
  table(
  columns: 5,
  align: (left, right, right, right, right,),
  table.header([Study], [Training], [Validation], [Outlier], [Total]),
  [Beermann1977a],
  [5 (5)],
  [5 (5)],
  [-],
  [10 (10)],
  [Jeon2012],
  [3 (17)],
  [-],
  [-],
  [3 (17)],
  [Knauf1995],
  [48 (48)],
  [1 (14)],
  [-],
  [49 (62)],
  [Nilsen1989],
  [1 (6)],
  [-],
  [-],
  [1 (6)],
  [Patel1984],
  [10 (10)],
  [2 (2)],
  [-],
  [12 (12)],
  [Ripley2000],
  [4 (8)],
  [-],
  [-],
  [4 (8)],
  [Williams1982],
  [6 (72)],
  [-],
  [-],
  [6 (72)],
  [Total],
  [77 (166)],
  [8 (21)],
  [-],
  [85 (187)],
  ),
  caption: [Data of the fit PD\_20261017\_030352\_\_10c1d: the number of fit mappings and, in parentheses, of data points per study and kind. The training data enters the cost, the validation data and the outliers are evaluated only.],
) <tab:data:PD_20261017_030352__10c1d>

== Goodness of fit

#figure(
  table(
  columns: 11,
  align: (left, right, right, right, right, right, right, right, right, right, right,),
  table.header([Kind], [n], [cost], [MSE], [RMSE], [NRMSE], [RMSE\_w], [R²], [2-fold \[%\]], [AIC], [BIC]),
  [training],
  [166],
  [65.1],
  [996],
  [31.6],
  [0.514],
  [0.886],
  [0.785],
  [88.8],
  [1156.0],
  [1171.5],
  [validation],
  [21],
  [-],
  [2.33e+03],
  [48.3],
  [0.275],
  [1.29],
  [0.875],
  [100.0],
  [172.8],
  [178.0],
  ),
  caption: [Goodness of fit of the fit PD\_20261017\_030352\_\_10c1d per kind of data, the parameter set PD\_20261017\_030352\_\_10c1d\_0. The cost is defined on the training data only, 2-fold is the percentage of the data points with a positive value and prediction whose prediction is within twofold of the data.],
) <tab:metrics:PD_20261017_030352__10c1d>

== Figures

#figure(
  image("plots/traces.svg", width: 100%),
  caption: [Cost of the optimizers over their steps, fit PD\_20261017\_030352\_\_10c1d. The cost of every optimization run over its steps. Runs which end at the same cost found the same optimum; a run which stops much higher is stuck in a local minimum.],
) <fig:traces:PD_20261017_030352__10c1d>

#figure(
  image("plots/waterfall.svg", width: 100%),
  caption: [Cost of the optimization runs, ordered, fit PD\_20261017\_030352\_\_10c1d. The final cost of the runs, ordered. A flat plateau at the left is the global optimum found repeatedly, which is the evidence that the multistart converged; steps to the right are local minima.],
) <fig:waterfall:PD_20261017_030352__10c1d>

#figure(
  image("plots/goodness_of_fit.svg", width: 100%),
  caption: [Prediction against the measured data points, per kind of fit mapping, with the agreement of the training data, the lines of twofold and the metrics of the panel, fit PD\_20261017\_030352\_\_10c1d. Within twofold of the data are 143 of the 161 training data points (88.8%) and 21 of the 21 validation data points (100.0%); only the data points with a positive value and prediction are counted. Prediction against measurement, one point per data point, with a panel per kind of fit mapping. The points scatter around the diagonal when the model describes the data; a systematic deviation from it is a systematic error of the model. The band is the agreement of the training data, i.e. the same band the Bland-Altman plot draws, here as lines parallel to the diagonal. The dark red dotted lines are twofold, prediction \= 2 x measurement and prediction \= measurement \/ 2; the caption states the points between them of every kind. A point which is zero or negative is not drawn on the logarithmic axes and not counted, the title of a panel then states the points drawn of all. The validation panel shows how the fit describes data it was not fitted on, the outlier panel the data the fit dropped. The box of a panel carries its R², its normalized RMSE, the RMSE of the residuals of the cost, its fold errors GMFE and AFE and the percentages of its points within twofold and within two standard deviations of the data.],
) <fig:goodness_of_fit:PD_20261017_030352__10c1d>

#figure(
  image("plots/bland_altman.svg", width: 100%),
  caption: [Agreement of prediction and measurement as a ratio, per kind of fit mapping, with the agreement of the training data and the agreement of the panel, fit PD\_20261017\_030352\_\_10c1d. The ratio of prediction and measurement over the geometric mean of the two, i.e. the goodness of fit with the diagonal turned into the horizontal. The band is the same, the bias and the limits of agreement #raw("bias ± 1.96 SD") of the training data as fold factors. A bias away from 1 is a systematic over- or underprediction, wide limits are a large scatter, and a trend over the mean is a model which describes the large or the small values better. The box of a panel carries the bias and the SD of its own points as fold factors and the share of them inside the limits of agreement of the training data.],
) <fig:bland_altman:PD_20261017_030352__10c1d>

#figure(
  image("plots/profiles.svg", width: 100%),
  caption: [Profile likelihood of every parameter: the cost with the parameter fixed and the other parameters optimized, the threshold of the confidence level and the confidence interval, fit PD\_20261017\_030352\_\_10c1d. One profile per parameter. A profile which crosses the dashed threshold on both sides gives a finite confidence interval; one which stays below it up to a bound is practically non-identifiable; a flat profile is structurally non-identifiable, the parameter is compensated by the others.],
) <fig:profiles:PD_20261017_030352__10c1d>

== Provenance

#figure(
  table(
  columns: 2,
  align: (left, left,),
  table.header([Item], [Value]),
  [Fit],
  raw("PD_20261017_030352__10c1d"),
  [Created],
  [2026-10-17 01:03:57 UTC],
  [Seed],
  [1234],
  [Python],
  [3.14.8],
  [sbmlsim],
  [0.10.0],
  [libRoadRunner],
  [2.10.0],
  [SciPy],
  [1.18.1],
  [NumPy],
  [2.5.3],
  [Repository],
  raw("/home/mkoenig/git/pkdb_models"),
  [Commit],
  raw("02b4b5c535fd42d63a6e025f407656229ea2a747"),
  [Uncommitted changes],
  [yes],
  ),
  caption: [Provenance of the fit PD\_20261017\_030352\_\_10c1d: the versions it ran with and the revision of its models and data; the SHA-256 checksums of the models and data are listed in #ref(<tab:checksums:PD_20261017_030352__10c1d>).],
) <tab:provenance:PD_20261017_030352__10c1d>

#bibliography("references.bib", style: "references.csl")
