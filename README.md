# Data Records
Data in this repository consists of two Excel spreadsheets and three CSV files:
- metadata.csv
- WWTP_Billing.xlsx
- WWTP_Billling_Assumptions.xlsx
- reference_list.csv
- synthetic_energy_data.csv

## Metadata
Metadata is stored in a single CSV files with each facility taking up one row and the following columns named in the header:
-	**Index**: Index assigned by authors (1-100)
-	**CWNS_No**: Clean Watershed Needs Survey (CWNS) ID number
-	**Existing Total Flow (MGD)**: operational flow rate in millions of gallons per day according to CWNS
-	**Design Flow (MGD)**: design flow rate in millions of gallons per day according to CWNS
-	**Existing Total Flow (m3/d)**: operational flow rate in cubic meters per day according to CWNS (using a conversion factor of 3785.41178 cubic meters = 1 million gallons)
-	**Design Flow (m3/d)**: design flow rate in cubic meters according to CWNS (using a conversion factor of 3785.41178 cubic meters = 1 million gallons)
-	**City**: city where the facility is located, e.g. “Syracuse”
-	**County**: county where the facility is located, e.g. “Onondaga”
-	**State**: two-letter code for the state where the facility is located, e.g. “NY”
-	**Latitude**: latitude decimal degree for a point. Positive values are used for both Northern and Southern hemisphere and have to be used in conjunction with the Latitude direction. The measure of the degree portion of a latitude measurement (0 to 90 degrees), indicating angular distance North or South of the equator. One degree of latitude equals 111.1 Kilometers or approximately 60 Nautical Miles. Includes the direction of the latitude measurement, being either: N - North, or S - South.
-	**Longitude**: longitude decimal degree for a point. Positive values are used for both Eastern and Western hemisphere and have to be used in conjunction with the Longitude direction. The measure of the degree portion of longitude (000 to 180 degrees), indicating angular distance West or East of the prime meridian drawn from pole to pole around the Earth and passing through Greenwich, England. Includes the direction of the longitude measurement being either: E - East, or W - West.
-   **Horizontal Collection Method**: text that describes the method used to determine the latitude and longitude coordinates for a point on the earth (taken directly from CWNS)
-   **Horizontal Coordinate Datum**: name of the reference datum used in determining latitude and longitude coordinates. The options are North American Datum of 1983 or World Geodetic System of 1984
-   **Location Description**: name of the place where the coordinates were measured taken directly from CWNS. The options are: Lagoon or Settling Pond; Facility/Station Location; Intake/Release Point; Treatment/Storage Point; or Center/Centroid
-   **Location Source**: : indicates how the point was entered. “Manual” indicates that the state user entered the coordinate information. “NPDES Permit” indicates that the coordinates were sourced from the information provided on the NPDES permit
-   **Scale**: text that describes the geopositioning or Scale of a map, e.g. 1:1000
-	**Has Cogen**: whether the facility has cogeneration capabilities (regardless of whether or not they are operating). Either “Yes” or “No”
-	**Est. Existing Electricity Demand (MW)**: estimated gross electricity demand in MW. Calculated by multiplying Existing Total Flow by a typical energy intensity of wastewater treatment.
-	**Est. Existing Electric Grid Demand (MW)**: estimated electric grid demand in MW. Either equal to or half of Est. Existing Electricity Demand depending on whether or not a facility has cogeneration.
-	**Est. Existing Natural Gas Demand (therms/hr)**: estimated average natural gas demand in therms per hour. If a facility had cogeneration, it was estimated that 50% of its electricity is produced by cogeneration using a standard biogas mixture. If a facility did not have cogeneration, gas demand was calculated with a 100% natural gas blend (as opposed to 10%).
-	**Est. Existing Natural Gas Demand (m3/hr)**: estimated average natural gas demand in cubic meters per hour (using a conversion factor of 2.83168 cubic meters = 1 therm). If a facility had cogeneration, it was estimated that 50% of its electricity is produced by cogeneration using a standard biogas mixture. If a facility did not have cogeneration, gas demand was calculated with a 100% natural gas blend (as opposed to 10%).
-	**Est. Design Electricity Demand (MW)**: estimated maximum gross electricity demand in MW. Calculated by multiplying Design Flow by a typical energy intensity of wastewater treatment.
-	**Est. Design Electric Grid Demand (MW)**: estimated maximum electric grid demand in MW. Either equal to or half of Est. Design Electricity Demand depending on whether or not a facility has cogeneration.
-	**Est. Design Natural Gas Demand (therms/hr)**: estimated maximum natural gas demand in therms per hour. If a facility had cogeneration, it was estimated that 50% of its electricity is produced by cogeneration using a standard biogas mixture. If a facility did not have cogeneration, gas demand was calculated with a 100% natural gas blend (as opposed to 10%).
-	**Est. Design Natural Gas Demand (m3/hr)**: estimated maximum natural gas demand in cubic meters per hour (using a conversion factor of 2.83168 cubic meters = 1 therm). If a facility had cogeneration, it was estimated that 50% of its electricity is produced by cogeneration using a standard biogas mixture. If a facility did not have cogeneration, gas demand was calculated with a 100% natural gas blend (as opposed to 10%).
-	**Electric Utility**: electric utility, e.g. “National Grid”
-	**Gas Utility**: natural gas utility, e.g. “National Grid”
-	**Electricity Energy Charge Temporality**: categorization of the temporality of electricity energy charges. “Flat” indicates charges are constant throughout the year; “Seasonal-TOU” indicates charges vary monthly (Seasonal) and daily and/or hourly (TOU); “Nonseasonal-TOU” indicates charges are consistent from month to month, but vary daily and/or hourly; and “Seasonal-NonTOU” indicates charges vary monthly, but are constant from day to day and hour to hour
-	**Electricity Demand Charge Temporality**: categorization of the temporality of electricity demand charges. “Flat” indicates charges are constant throughout the year; “Seasonal-TOU” indicates charges vary monthly (Seasonal) and daily and/or hourly (TOU); “Nonseasonal-TOU” indicates charges are consistent from month to month, but vary daily and/or hourly; and “Seasonal-NonTOU” indicates charges vary monthly, but are constant from day to day and hour to hour

The data on flow rate, city, state, and county was obtained by merging the CWNS with previously described procedure for determining if a facility has CHP. Description of utility service areas were used to determine the correct utility for each municipality.

## Billing Data
Each worksheet of `WWTP_Billing.xlsx` is given the name of the CWNS number corresponding to that facility. Each row of the tariff structure corresponds to a different tariff, so if a municipality with a flat electricity tariff would have only one row whereas a municipality with a complex tariff structure would have many rows. Gas tariffs are included only for facilities which have cogeneration, since without cogeneration natural gas costs are unaffected by energy flexibility for a typical wastewater treatment facility. The electricity and natural gas tariff data has the following columns:
-	**utility**: type of utility, i.e. “electric” or “gas”
-	**type**: type of charge. Options are “customer”, “demand”, and “energy”
-	**period**: name for the charge period. Only relevant for demand charges, since there can be multiple concurrent demand charges, i.e. a charge named “maximum” which is in effect 24 hours a day vs. a charge named “on-peak” which is only in effect during afternoon hours.
-	**basic_charge_limit (imperial)**: consumption limit above which the charge takes effect in imperial units (i.e., kWh of electricity and therms of natural gas). Default is 0. A limit is in effect until another limit supersedes it, e.g. if there are two charges, Charge 1 with basic_charge_limit = 0 and Charge 2 with basic_charge_limit = 1000, Charge 1 will be in effect until 1000 units are delivered, and Charge 2 will be in effect thereafter.
-	**basic_charge_limit (metric)**: consumption limit above which the charge takes effect in metric units (i.e., kWh of electricity and cubic meters of natural gas). Default is 0.  A limit is in effect until another limit supersedes it, e.g. if there are two charges, Charge 1 with basic_charge_limit = 0 and Charge 2 with basic_charge_limit = 1000, Charge 1 will be in effect until 1000 units are delivered, and Charge 2 will be in effect thereafter.
-	**month_start**: first month during which this charge occurs (1-12)
- **month_end**: last month during which this charge occurs (1-12)
-	**hour_start**: hour at which this charge starts (0-24)
-	**hour_end**: hour at which this charge ends (0-24)
-	**weekday_start**: first weekday on which this charge occurs (0 = Monday to 6 = Sunday)
-	**weekday_end**: last weekday on which this charge occurs (0 = Monday to 6 = Sunday)
-	**charge (imperial)**: cost represented as a float in imperial units. I.e., "$/month", "$/kWh", "$/kW", "$/therm", and "$/therm/hr" for customer charges, electric energy charges, electric demand charges, natural gas energy charges, and natural gas demand charges, respectively
-   **charge (metric)**: cost represented as a float in metric units. I.e., "$/month", "$/kWh", "$/kW", "$/m3", and "$/m3/hr" for customer charges, electric energy charges, electric demand charges, natural gas energy charges, and natural gas demand charges, respectively. A conversion factor of 2.83168 cubic meters to 1 therm was used.
-	**units**: units of the charge, e.g. “$/kWh”. If units are different between imperial and metric then imperial is listed followed by metric. E.g., "$/therm or $/m3".
-	**Notes**: any comments the authors felt would help explain unintuitive decisions in data collection or formatting

## Billing Assumptions
Besides the assumptions made for every facility laid out in the Methods section, many utilities had nuanced tariffs which required further simplifying assumptions. These assumptions are cataloged in `WWTP_Billing_Assumptions.xlsx`, which has two worksheets: `Electric` and `Gas`. Both have a new assumption on each row and identical columns:
-	**Assumptions**: explanation of the assumption the authors made in determining the correct tariff for these facilities
-	**CWNS_No_1, CWNS_No_2, …, CWNS_No_14**: list of facilities for which this assumption applies. “ALL” indicates the assumption was applied to all facilities.

## Reference List
There is a list of all the original tariffs used to compile this dataset, which includes the following information:
- **Document Title**: name of the document being referenced
- **Utility**: utility which published this tariff
- **Day Filed**: day on which this tariff was filed (if known)
- **Month Filed**: month in which this tariff was filed (if known)
- **Year Filed**: year in which this tariff was filed (if known)
- **Day Effective**: day on which this tariff became effective (if known)
- **Month Effective**: month in which this tariff became effective (if known)
- **Year Effective**: year in which this tariff became effective (if known)
- **Day Accessed**: day on which this tariff was downloaded (if known)
- **Month Accessed**: month in which this tariff was downloaded (if known)
- **Year Accessed**: year in which this tariff was downloaded (if known)
- **Relevant CWNS Numbers**: list of facilities to which this tariff applies

If the referenced tariff included multiple sheets with different filed or effective dates, then the most recent date of the entire book was used. Date accessed is only included for non-static HTML pages.

## Synthetic Energy Data
One week of sample energy data at a 15-minute timescale is copied for a year to be used by `sample_usage.py`.
`sample_usage.py` demonstrates some simple analysis that can be conducted using this dataset.
- **DateTime**: date and time of synthetic energy data sample
- **grid_to_plant_kW**: electricity delivered from the grid in kW
- **natural_gas_therm_per_hr**: natural gas delivered to the cogenerator in therms/hr

## Attribution & Acknowledgements
If this dataset has been useful in your research, we encourage you to cite the following data descriptor from Nature Scientific Data:

&nbsp; Chapin, F.T., Bolorinos, J. & Mauter, M.S. Electricity and natural gas tariffs at United States wastewater treatment plants. *Sci Data* **11**, 113 (2024). DOI: [10.1038/s41597-023-02886-6](https://doi.org/10.1038/s41597-023-02886-6)

The raw data can also be cited directly from Figshare:

&nbsp; Chapin, F.T., Bolorinos, J., & Mauter, M. S. Electricity and natural gas tariffs at United States wastewater treatment plants. *figshare* https://doi.org/10.6084/m9.figshare.c.6435578.v1 (2024).

In `bibtex` format:

```
@Article{Chapin2024,
author={Chapin, Fletcher T.
and Bolorinos, Jose
and Mauter, Meagan S.},
title={Electricity and natural gas tariffs at United States wastewater treatment plants},
journal={Scientific Data},
year={2024},
month={Jan},
day={23},
volume={11},
number={1},
pages={113},
abstract={Wastewater treatment plants (WWTPs) are large electricity and natural gas consumers with untapped potential to recover carbon-neutral biogas and provide energy services for the grid. Techno-economic analysis of emerging energy recovery and management technologies is critical to understanding their commercial viability, but quantifying their energy cost savings potential is stymied by a lack of well curated, nationally representative electricity and natural gas tariff data. We present a dataset of electricity tariffs for the 100 largest WWTPs in the Clean Watershed Needs Survey (CWNS) and natural gas tariffs for the 54 of 100 WWTPs with on-site cogeneration. We manually collected tariffs from each utility's website and implemented data checks to ensure their validity. The dataset includes facility metadata, electricity tariffs, and natural gas tariffs (where cogeneration is present). Tariffs are current as of November 2021. We provide code for technical validation along with a sample simulation.},
issn={2052-4463},
doi={10.1038/s41597-023-02886-6},
url={https://doi.org/10.1038/s41597-023-02886-6}
}

@misc{chapin_bolorinos_mauter_2024, 
author={Chapin, Fletcher T. 
and Bolorinos, Jose 
and Mauter, Meagan S.}, 
title={Electricity and natural gas rate schedules at U.S. wastewater treatment plants}, 
url={https://springernature.figshare.com/collections/Electricity_and_natural_gas_rate_schedules_at_U_S_wastewater_treatment_plants/6435578/1}, 
DOI={10.6084/m9.figshare.c.6435578.v1}, 
abstractNote={Electricity and natural gas tariffs of the 100 largest wastewater treatment plants in the United States}, 
publisher={figshare}, 
year={2024}, 
month={Jan}
}
```

This work was funded by the United States Department of Energy (DOE), EERE Advanced Manufacturing Office (AMO) as a part of the project ENERGY Services for INtegrated FLexible Operation of Wastewater Systems (Award No. DE-EE0009499). We would like to thank Lonita Brewer from EPB of Chattanooga for obtaining archived fuel cost adjustments for 2021.