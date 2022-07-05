# Data Records
Data in this repository consists of two Excel spreadsheets and two CSV files:
- Metadata.csv
-	WWTP_Billing.xls
-	WWTP_Billling_Assumptions.xlsx
- dummy_energy_data.csv

## Metadata
Metadata is stored in a single CSV files with each facility taking up one row and the following columns named in the header:
-	Index: Index assigned by authors (1-100)
-	CWNS_No: CWNS ID number
-	Total Flow (MGD): operational flow rate in MGD according to CWNS represented as a float
-	City: city where the facility is located, e.g. “Syracuse”
-	County: county where the facility is located, e.g. “Onondaga”
-	State: two-letter code for the state where the facility is located, e.g. “NY”
-	Has Cogen: whether the facility has co-generation capabilities (regardless of whether or not they are operating). Either “Yes” or “No”
-	Est. Energy Demand (MW): estimated maximum electricity demand in MW. Calculated by multiplying the flow rate from the CWNS dataset by a typical energy intensity of wastewater treatment
-	Est. Electric Grid Demand (MW): estimated maximum natural gas demand in MW. Either equal to or half of Est. Energy Demand depending on whether or not a facility has co-generation.
-	Est. Natural Gas Demand (therms/hr): estimated maximum natural gas demand in therms/hr. If a facility had co-generation, it was estimated that 50% of its electricity is produced by co-generation using a standard biogas mixture. If a facility did not have co-generation, gas demand was assumed to be zero.
-	Electric Utility: electric utility, e.g. “National Grid”
-	Gas Utility: natural gas utility, e.g. “National Grid”

The data on flow rate, city, state, and county was obtained by merging the CWNS [Data Citation 1] with previously described procedure for determining if a facility has CHP. Description of utility service areas were used to determine the correct utility for each municipality Whenever possible static URLs were used, but that was not always feasible. In those cases, the tariffs may have been updated since 2021 and the online information may no longer match the dataset.

## Billing Data
Each worksheet of WWTP_Billing.xls is given the name of the CWNS number corresponding to that facility. Each row of the tariff structure corresponds to a different rate, so if a municipality with a flat electricity rate would have only one row whereas a municipality with a complex rate structure would have many rows. Gas rates are included only for facilities which have co-generation, since without co-generation natural gas costs are negligible for a typical wastewater treatment facility. The energy tariff data has the following columns:
-	utility: type of utility, i.e. “electric” or “gas”
-	type: type of energy charge. Options are “customer”, “demand”, and “energy”
-	period: name for the charge period. Only relevant for demand charges, since there can be multiple concurrent demand charges, i.e. a charge named “maximum” which is in effect 24 hours a day vs. a charge named “on-peak” which is only in effect during afternoon hours.
-	basic_charge_limit: limit above which the charge takes effect (default is 0). A limit is in effect until another limit supersedes it, e.g. if there are two charges, Charge 1 with basic_charge_limit = zero and Charge 2 with basic_charge_limit = 1000, Charge 1 will be in effect until 1000 units are consumed, and Charge 2 will be in effect thereafter.
-	month_start: first month during which this charge occurs (1-12)
-	month_end: last month during which this charge occurs (1-12)
-	hour_start: hour at which this charge starts (0-24)
-	hour_end: hour at which this charge ends (0-24)
-	weekday_start: first weekday on which this charge occurs (0-6)
-	weekday_end: last weekday on which this charge occurs (0-6)
-	charge: cost represented as a float
-	units: units of the charge, e.g. “$/kWh”
-	Notes: any comments the authors felt would help explain unintuitive decisions in data collection or formatting

## Billing Assumptions
Besides the assumptions made for every facility laid out in the Methods section, many utilities had nuanced rates which required further simplifying assumptions. These assumptions are cataloged in WWTP_Billing_Assumptions.xlsx, which has two worksheets: ‘Electric’ and ‘Gas’. Both have a new assumption on each row and identical columns:
-	Assumptions: explanation of the assumption the authors made in determining the correct rate structure for these facilities
-	CWNS_No_1, CWNS_No_2, …, CWNS_No_14: list of facilities for which this assumption applies. “ALL” indicates the assumption was applied to all facilities.

## Dummy Energy Data
One week of sample energy data at 15-minute timescales is copied for a year to be used by `sample_usage.py`.
`sample_usage.py` demonstrates some simple analysis that can be conducted using this dataset.
-	DateTime: Datetime of dummy energy data sample
- grid_to_plant_kW: electricity consumed from the grid in kW
- natural_gas_therm_per_hr: natural gas consumed by co-generation in therms/hr
