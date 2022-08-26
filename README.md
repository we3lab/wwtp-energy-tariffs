# Data Records
Data in this repository consists of two Excel spreadsheets and three CSV files:
- metadata.csv
-	WWTP_Billing.xlsx
-	WWTP_Billling_Assumptions.xlsx
- reference_list.csv
- dummy_energy_data.csv

## Metadata
Metadata is stored in a single CSV files with each facility taking up one row and the following columns named in the header:
-	**Index**: Index assigned by authors (1-100)
-	**CWNS_No**: Clean Watershed Needs Survey (CWNS) ID number
-	**Existing Total Flow (MGD)**: operational flow rate in MGD according to CWNS
-	**Design Flow (MGD)**: design flow rate in MGD according to CWNS
-	**City**: city where the facility is located, e.g. “Syracuse”
-	**County**: county where the facility is located, e.g. “Onondaga”
-	**State**: two-letter code for the state where the facility is located, e.g. “NY”
-	**Has Cogen**: whether the facility has co-generation capabilities (regardless of whether or not they are operating). Either “Yes” or “No”
-	**Est. Existing Energy Demand (MW)**: estimated energy demand in MW. Calculated by multiplying Existing Total Flow by a typical energy intensity of wastewater treatment
-	**Est. Existing Electric Grid Demand (MW)**: estimated electricity demand in MW. Either equal to or half of Est. Existing Energy Demand depending on whether or not a facility has co-generation.
-	**Est. Existing Natural Gas Demand (therms/hr)**: estimated natural gas demand in therms/hr. If a facility had co-generation, it was estimated that 50% of its electricity is produced by co-generation using a standard biogas mixture. If a facility did not have co-generation, gas demand was assumed to be zero.
-	**Est. Design Energy Demand (MW)**: estimated maximum electricity demand in MW. Calculated by multiplying Design Flow by a typical energy intensity of wastewater treatment
-	**Est. Design Electric Grid Demand (MW)**: estimated maximum electricity demand in MW. Either equal to or half of Est. Design Energy Demand depending on whether or not a facility has co-generation.
-	**Est. Design Natural Gas Demand (therms/hr)**: estimated maximum natural gas demand in therms/hr. If a facility had co-generation, it was estimated that 50% of its electricity is produced by co-generation using a standard biogas mixture. If a facility did not have co-generation, gas demand was assumed to be zero.
-	**Electric Utility**: electric utility, e.g. “National Grid”
-	**Gas Utility**: natural gas utility, e.g. “National Grid”

The data on flow rate, city, state, and county was obtained by merging the CWNS with previously described procedure for determining if a facility has CHP. Description of utility service areas were used to determine the correct utility for each municipality.

## Billing Data
Each worksheet of `WWTP_Billing.xlsx` is given the name of the CWNS number corresponding to that facility. Each row of the tariff structure corresponds to a different rate, so if a municipality with a flat electricity rate would have only one row whereas a municipality with a complex rate structure would have many rows. Gas rates are included only for facilities which have co-generation, since without co-generation natural gas costs are negligible for a typical wastewater treatment facility. The energy tariff data has the following columns:
-	**utility**: type of utility, i.e. “electric” or “gas”
-	**type**: type of energy charge. Options are “customer”, “demand”, and “energy”
-	**period**: name for the charge period. Only relevant for demand charges, since there can be multiple concurrent demand charges, i.e. a charge named “maximum” which is in effect 24 hours a day vs. a charge named “on-peak” which is only in effect during afternoon hours.
-	**basic_charge_limit**: limit above which the charge takes effect (default is 0). A limit is in effect until another limit supersedes it, e.g. if there are two charges, Charge 1 with basic_charge_limit = zero and Charge 2 with basic_charge_limit = 1000, Charge 1 will be in effect until 1000 units are consumed, and Charge 2 will be in effect thereafter.
-	**month_start**: first month during which this charge occurs (1-12)
- **month_end**: last month during which this charge occurs (1-12)
-	**hour_start**: hour at which this charge starts (0-24)
-	**hour_end**: hour at which this charge ends (0-24)
-	**weekday_start**: first weekday on which this charge occurs (0-6)
-	**weekday_end**: last weekday on which this charge occurs (0-6)
-	**charge**: cost represented as a float
-	**units**: units of the charge, e.g. “$/kWh”
-	**Notes**: any comments the authors felt would help explain unintuitive decisions in data collection or formatting

## Billing Assumptions
Besides the assumptions made for every facility laid out in the Methods section, many utilities had nuanced rates which required further simplifying assumptions. These assumptions are cataloged in `WWTP_Billing_Assumptions.xlsx`, which has two worksheets: `Electric` and `Gas`. Both have a new assumption on each row and identical columns:
-	**Assumptions**: explanation of the assumption the authors made in determining the correct rate structure for these facilities
-	**CWNS_No_1, CWNS_No_2, …, CWNS_No_14**: list of facilities for which this assumption applies. “ALL” indicates the assumption was applied to all facilities.

## Reference List
There is a list of all the original rate schedules and tariffs used to compile this dataset, which includes the following information:
- **Document Title**: Name of the document being referenced
- **Utility**: Utility which published this tariff
- **Day Filed**: Day on which this tariff was filed (if known)
- **Month Filed**: Month in which this tariff was filed (if known)
- **Year Filed**: Year in which this tariff was filed (if known)
- **Day Effective**: Day on which this tariff became effective (if known)
- **Month Effective**: Month in which this tariff became effective (if known)
- **Year Effective**: Year in which this tariff became effective (if known)
- **Day Accessed**: Day on which this tariff was downloaded (if known)
- **Month Accessed**: Month in which this tariff was downloaded (if known)
- **Year Accessed**: Year in which this tariff was downloaded (if known)
- **Relevant CWNS Numbers**: List of facilities to which this tariff applies
- **URL**: Link to the original document in this repository in PDF, Excel, or Word format

If the referenced tariff included multiple sheets with different filed or effective dates, then the most recent date of the entire book was used. Date accessed is only included for non-static HTML pages, which were archived with the [Wayback Machine](https://archive.org/web/). All documents are available in the `references` folder.

## Dummy Energy Data
One week of sample energy data at 15-minute timescales is copied for a year to be used by `sample_usage.py`.
`sample_usage.py` demonstrates some simple analysis that can be conducted using this dataset.
-	**DateTime**: Datetime of dummy energy data sample
- **grid_to_plant_kW**: electricity consumed from the grid in kW
- **natural_gas_therm_per_hr**: natural gas consumed by co-generation in therms/hr
