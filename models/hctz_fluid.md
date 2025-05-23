# model: hctz_fluid
Autogenerated ODE System from SBML with [sbmlutils](https://github.com/matthiaskoenig/sbmlutils).
```
time: [min]
substance: [mmol]
extent: [mmol]
volume: [l]
area: [m^2]
length: [m]
```

## Parameters `p`
```
BW = 75.0  # [kg] body weight [kg]  
Mr_cl = 35.45  # [g/mol] Molecular weight chloride  
Mr_na = 22.99  # [g/mol] Molecular weight sodium  
Mr_nacl = 58.44  # [g/mol] Molecular weight sodium chloride  
Pdia_ref = 80.0  # [133.32239 N/m^2] Reference diastolic blood pressure  
Psys_ref = 120.0  # [133.32239 N/m^2] Reference systolic blood pressure  
Vki = nan  # [l] kidney  
f_ECF = 0.33  # [-] ECF fraction of TBW  
f_TBW = 0.55  # [l/kg] Total body water (TBW) fraction of bodyweight (male)  
k_cl = 0.000233  # [l/min]   
k_h2o = 0.000117334965819814  # [1/min]   
k_na = 0.000169757142857143  # [l/min]   
vin_h2o = 0.00159722222222222  # [l/min] H2O uptake via food  
vin_nacl = 0.023766  # [mmol/min] NaCl uptake via food  
```

## Initial conditions `x0`
```
ECF = 13.6125  # [l] extracellular fluid (ECF)  
Vurine = 1e-12  # [l] urine  
cl = 102.0  # [mmol/l] Chloride (Cl-) (ECF) in ECF  
cl_urine = 0.0  # [mmol] Chloride (Cl-) (urine) in Vurine  
na = 140.0  # [mmol/l] Sodium (Na+) (ECF) in ECF  
na_urine = 0.0  # [mmol] Sodium (Na+) (urine) in Vurine  
```

## ODE system
```
# y
CL_EXCRETION = k_cl * cl  # [mmol/min] Cl excretion urine  
ECF_ref = f_ECF * f_TBW * BW  # [l] Reference extracellular fluid volume (ECF)  
NACL_UPTAKE = vin_nacl  # [mmol/min] Na/Cl uptake via food  
NA_EXCRETION = k_na * na  # [mmol/min] Na excretion urine  
diuresis = k_h2o * ECF  # [l/min]   
Pdia = Pdia_ref * ECF / ECF_ref  # [133.32239 N/m^2] Diastolic blood pressure  
Psys = Psys_ref * ECF / ECF_ref  # [133.32239 N/m^2] Systolic blood pressure  
vin_cl = NACL_UPTAKE * Mr_nacl  # [mg/min]   
vin_na = NACL_UPTAKE * Mr_nacl  # [mg/min]   
vout_cl = CL_EXCRETION * Mr_cl  # [mg/min]   
vout_na = NA_EXCRETION * Mr_na  # [mg/min]   

# odes
d ECF/dt = vin_h2o - diuresis  # [l/min] extracellular fluid (ECF)  
d Vurine/dt = diuresis  # [l/min] urine  
d cl/dt = NACL_UPTAKE / ECF - CL_EXCRETION / ECF  # [mmol/l/min] Chloride (Cl-) (ECF)  
d cl_urine/dt = CL_EXCRETION  # [mmol/min] Chloride (Cl-) (urine)  
d na/dt = NACL_UPTAKE / ECF - NA_EXCRETION / ECF  # [mmol/l/min] Sodium (Na+) (ECF)  
d na_urine/dt = NA_EXCRETION  # [mmol/min] Sodium (Na+) (urine)  
```