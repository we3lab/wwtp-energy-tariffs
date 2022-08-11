import os
import pytest
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_continuity(df, charge_type):
    if charge_type == "customer" or "demand":
        return True

    month_start = 1
    day_start = 0
    hour_start = 0

    while month_start < 13:
        row = df[(df["month_start"] <= month_start) & (df["month_end"] >= month_start)
                 & (df["weekday_start"] <= day_start) & (df["month_end"] >= day_start)
                 & (df["hour_start"] <= hour_start) & (df["hour_end"] >= hour_start)]
        if len(df.columns) == 0:
            return False

        hour_start = row[0, "hour_end"]

        if hour_start == 24:
            hour_start = 0
            day_start += 1

        if day_start == 7:
            day_start = 0
            month_start += 1

    return True


metadata = pd.read_csv("data/Metadata.csv")
old_mgd = 50
max_mgd = 812
max_charges = {"electric_demand": 35, "electric_energy": 2, "gas_energy": 3,
               "gas_demand": 1.5, "gas_customer": 5000, "electric_customer": 5000}

for cwns_no in metadata["CWNS_No"]:
    row = metadata.loc[metadata["CWNS_No"] == cwns_no]
    rate_df = pd.read_excel("data/WWTP_Billing.xlsx", sheet_name=str(cwns_no))

    # Check that MGD is increasing with each sheet, within bounds of smallest/largest
    current_mgd = row["Total Flow (MGD)"].iloc[0]
    assert old_mgd <= current_mgd
    assert current_mgd <= max_mgd
    old_mgd = current_mgd

    # If facility has_cogen, need gas (otherwise just electric)
    utilities = rate_df["utility"].unique()
    if row["Has Cogen"].iloc[0] == "Yes":
        assert "gas" in utilities
    else:
        assert "gas" not in utilities

    for utility in utilities:
        for charge_type in rate_df.loc[rate_df["utility"] == utility]["type"].unique():
            # Check that all days of a year are included
            slice = rate_df.loc[(rate_df["utility"] == utility) & (rate_df["type"] == charge_type)]
            assert check_continuity(slice, charge_type)

            # Check prices are positive and below a threshold
            # Manually checked the outliers in the if statement are correct
            if not ((cwns_no == 42005016001 and charge_type == "customer")
                or ((cwns_no == 36002001007 or cwns_no == 36002001010 or cwns_no == 36002001004
                     or cwns_no == 36002001009 or cwns_no == 36002001006 or cwns_no == 36003169012
                     or cwns_no == 36002001005 or cwns_no == 36002001002 or cwns_no == 36002001003
                     or cwns_no == 36002001012 or cwns_no == 36002001001 or cwns_no == 36002001011)
                     and utility == "gas" and charge_type == "energy")):
                assert slice["charge"].min() >= 0
                assert slice["charge"].max() <= max_charges[utility + "_" + charge_type]

    # Check units (i.e. demand is in kW and energy in kWh)
    assert (rate_df.loc[rate_df["type"] == "customer"]["units"] == "$/month").all()
    assert (rate_df.loc[(rate_df["type"] == "demand") & (rate_df["utility"] == "electric")]["units"] == "$/kW").all()
    assert (rate_df.loc[(rate_df["type"] == "energy") & (rate_df["utility"] == "electric")]["units"] == "$/kWh").all()
    assert (rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] == "energy")]["units"] == "$/therm").all()
    assert (rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] == "demand")]["units"] == "$/therm/hr").all()

    # Check that energy demand is either equal to or twice that of electricity demand
    # and that natural gas demand is either 0 or electricity * conversion_factor
    conversion_factor = 3600 / (105.5 * 10) # see paper for details
    assert (row["Est. Energy Demand (MW)"].iloc[0] == pytest.approx(row["Est. Electric Grid Demand (MW)"].iloc[0])
        or (row["Est. Energy Demand (MW)"].iloc[0]  / 2 == pytest.approx(row["Est. Electric Grid Demand (MW)"].iloc[0])
            and row["Est. Electric Grid Demand (MW)"].iloc[0] == pytest.approx(row["Est. Natural Gas Demand (therms/hr)"].iloc[0] / conversion_factor)))
