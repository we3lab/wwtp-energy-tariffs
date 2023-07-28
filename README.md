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
-	**Existing Total Flow (MGD)**: operational flow rate in millions of gallons per day according to CWNS
-	**Design Flow (MGD)**: design flow rate in millions of gallons per day according to CWNS
-	**Existing Total Flow (m3/d)**: operational flow rate in cubic meters per day according to CWNS (using a conversion factor of 3785.41178 cubic meters / day = 1 million gallons / day)
-	**Design Flow (m3/d)**: design flow rate in cubic meters according to CWNS (using a conversion factor of 3785.41178 cubic meters / day = 1 million gallons / day)
-	**City**: city where the facility is located, e.g. “Syracuse”
-	**County**: county where the facility is located, e.g. “Onondaga”
-	**State**: two-letter code for the state where the facility is located, e.g. “NY”
-	**Latitude**: latitude decimal degree for a point. Positive values are used for both Northern and Southern hemisphere and have to be used in conjunction with the Latitude direction. The measure of the degree portion of a latitude measurement (0 to 90 degrees), indicating angular distance North or South of the equator. One degree of latitude equals 111.1 Kilometers or approximately 60 Nautical Miles. Includes the direction of the latitude measurement, being either: N - North, or S - South.
-	**Longitude**: longitude decimal degree for a point. Positive values are used for both Eastern and Western hemisphere and have to be used in conjunction with the Longitude direction. The measure of the degree portion of longitude (000 to 180 degrees), indicating angular distance West or East of the prime meridian drawn from pole to pole around the Earth and passing through Greenwich, England. Includes the direction of the longitude measurement being either: E - East, or W - West.
-   **Horizontal Collection Method**: text that describes the method used to determine the latitude and longitude coordinates for a point on the earth (taken directly from CWNS)
-   **Horizontal Coordinate Datum**: name of the reference datum used in determining latitude and longitude coordinates. The options are: North American Datum of 1927, North American Datum of 1983, World Geodetic System of 1984, and North American Datum of 1927
-   **Location Description**: name of the place where the coordinates were measured taken directly from CWNS. The options are: Lagoon or Settling Pond; Facility/Station Location; Intake/Release Point; Treatment/Storage Point; or Center/Centroid
-   **Location Source**: : indicates how the point was entered. “Manual” indicates that the state user entered the coordinate information. “NPDES Permit” indicates that the coordinates were sourced from the information provided on the NPDES permit
-   **Scale**: text that describes the geopositioning or Scale of a map, e.g. 1:1000
-	**Has Cogen**: whether the facility has co-generation capabilities (regardless of whether or not they are operating). Either “Yes” or “No”
-	**Est. Existing Electricity Demand (MW)**: estimated total electricity demand in MW. Calculated by multiplying Existing Total Flow by a typical energy intensity of wastewater treatment.
-	**Est. Existing Electric Grid Demand (MW)**: estimated electric grid demand in MW. Either equal to or half of Est. Existing Electricity Demand depending on whether or not a facility has co-generation.
-	**Est. Existing Natural Gas Demand (therms/hr)**: estimated natural gas demand in therms per hour. If a facility had co-generation, it was estimated that 50% of its electricity is produced by co-generation using a standard biogas mixture. If a facility did not have co-generation, gas demand was assumed to be zero.
-	**Est. Existing Natural Gas Demand (m3/hr)**: estimated natural gas demand in cubic meters per hour (using a conversion factor of 2.83168 cubic meters = 1 therm). If a facility had co-generation, it was estimated that 50% of its electricity is produced by co-generation using a standard biogas mixture. If a facility did not have co-generation, gas demand was assumed to be zero.
-	**Est. Design Electricity Demand (MW)**: estimated maximum total electricity demand in MW. Calculated by multiplying Design Flow by a typical energy intensity of wastewater treatment.
-	**Est. Design Electric Grid Demand (MW)**: estimated maximum electric grid demand in MW. Either equal to or half of Est. Design Electricity Demand depending on whether or not a facility has co-generation.
-	**Est. Design Natural Gas Demand (therms/hr)**: estimated maximum natural gas demand in therms per hour. If a facility had co-generation, it was estimated that 50% of its electricity is produced by co-generation using a standard biogas mixture. If a facility did not have co-generation, gas demand was assumed to be zero.
-	**Est. Design Natural Gas Demand (m3/hr)**: estimated maximum natural gas demand in cubic meters per hour (using a conversion factor of 2.83168 cubic meters = 1 therm). If a facility had co-generation, it was estimated that 50% of its electricity is produced by co-generation using a standard biogas mixture. If a facility did not have co-generation, gas demand was assumed to be zero.
-	**Electric Utility**: electric utility, e.g. “National Grid”
-	**Gas Utility**: natural gas utility, e.g. “National Grid”

The data on flow rate, city, state, and county was obtained by merging the CWNS with previously described procedure for determining if a facility has CHP. Description of utility service areas were used to determine the correct utility for each municipality.

## Billing Data
Each worksheet of `WWTP_Billing.xlsx` is given the name of the CWNS number corresponding to that facility. Each row of the tariff structure corresponds to a different tariff, so if a municipality with a flat electricity tariff would have only one row whereas a municipality with a complex tariff structure would have many rows. Gas tariffs are included only for facilities which have co-generation, since without co-generation natural gas costs are unaffected by energy flexibility for a typical wastewater treatment facility. The electricity and natural gas tariff data has the following columns:
-	**utility**: type of utility, i.e. “electric” or “gas”
-	**type**: type of charge. Options are “customer”, “demand”, and “energy”
-	**period**: name for the charge period. Only relevant for demand charges, since there can be multiple concurrent demand charges, i.e. a charge named “maximum” which is in effect 24 hours a day vs. a charge named “on-peak” which is only in effect during afternoon hours.
-	**basic_charge_limit**: limit above which the charge takes effect (default is 0). A limit is in effect until another limit supersedes it, e.g. if there are two charges, Charge 1 with basic_charge_limit = zero and Charge 2 with basic_charge_limit = 1000, Charge 1 will be in effect until 1000 units are consumed, and Charge 2 will be in effect thereafter.
-	**month_start**: first month during which this charge occurs (1-12)
- **month_end**: last month during which this charge occurs (1-12)
-	**hour_start**: hour at which this charge starts (0-24)
-	**hour_end**: hour at which this charge ends (0-24)
-	**weekday_start**: first weekday on which this charge occurs (0-6)
-	**weekday_end**: last weekday on which this charge occurs (0-6)
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
- **URL**: link to the original document in this repository in PDF, Excel, or Word format

If the referenced tariff included multiple sheets with different filed or effective dates, then the most recent date of the entire book was used. Date accessed is only included for non-static HTML pages, which were archived with the [Wayback Machine](https://archive.org/web/). All documents are available in the `references` folder.

## Dummy Energy Data
One week of sample energy data at 15-minute timescales is copied for a year to be used by `sample_usage.py`.
`sample_usage.py` demonstrates some simple analysis that can be conducted using this dataset.
-	**DateTime**: datetime of dummy energy data sample
- **grid_to_plant_kW**: electricity consumed from the grid in kW
- **natural_gas_therm_per_hr**: natural gas consumed by co-generation in therms/hr
