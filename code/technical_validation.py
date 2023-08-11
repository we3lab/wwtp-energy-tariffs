import os
import pytest
import warnings
import openpyxl
import pandas as pd

# change to repo parent directory and suppress superfluous openpyxl warnings
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

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


metadata = pd.read_csv("data/metadata.csv")
old_mgd = 50
max_mgd = 812
max_charges = {"electric_demand": 35, "electric_energy": 2, "gas_energy": 3,
               "gas_demand": 1.5, "gas_customer": 5000, "electric_customer": 5000}

for cwns_no in metadata["CWNS_No"]:
    row = metadata.loc[metadata["CWNS_No"] == cwns_no]
    rate_df = pd.read_excel("data/WWTP_Billing.xlsx", sheet_name=str(cwns_no))

    # Check that MGD is increasing with each sheet, within bounds of smallest/largest
    current_mgd = row["Existing Total Flow (MGD)"].iloc[0]
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
                assert slice["charge (imperial)"].min() >= 0
                assert slice["charge (metric)"].min() >= 0
                assert slice["charge (imperial)"].max() <= max_charges[utility + "_" + charge_type]
                if utility == "gas":
                    assert slice["charge (metric)"].max() <= max_charges[utility + "_" + charge_type] / 2.83168
                elif utility == "electric":
                    assert slice["charge (metric)"].max() <= max_charges[utility + "_" + charge_type] 
                else:
                    raise ValueError("utility must be 'gas' or 'electric'")


    # Check units (i.e. demand is in kW and energy in kWh)
    assert (rate_df.loc[rate_df["type"] == "customer"]["units"] == "$/month").all()
    assert (rate_df.loc[(rate_df["type"] == "demand") & (rate_df["utility"] == "electric")]["units"] == "$/kW").all()
    assert (rate_df.loc[(rate_df["type"] == "energy") & (rate_df["utility"] == "electric")]["units"] == "$/kWh").all()
    assert (rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] == "energy")]["units"] == "$/therm or $/m3").all()
    assert (rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] == "demand")]["units"] == "$/therm/hr or $/m3/hr").all()
    
    # Check that month_start <= month_end, weekday_start <= weekday_end, and hour_start < hour_end
    assert (rate_df.loc[rate_df["type"] != "customer"]["month_start"] <= rate_df.loc[rate_df["type"] != "customer"]["month_end"]).all() 
    assert (rate_df.loc[rate_df["type"] != "customer"]["weekday_start"] <= rate_df.loc[rate_df["type"] != "customer"]["weekday_end"]).all() 
    assert (rate_df.loc[rate_df["type"] != "customer"]["hour_start"] < rate_df.loc[rate_df["type"] != "customer"]["hour_end"]).all() 

    # Check that conversion between metric and imperial units is correct
    assert (rate_df.loc[rate_df["utility"] == "electric"]["charge (imperial)"] 
        == rate_df.loc[rate_df["utility"] == "electric"]["charge (metric)"]
    ).all()
    assert (rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] != "customer")]["charge (imperial)"] / 2.83168
        ==  rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] != "customer")]["charge (metric)"] 
    ).all()
    assert (rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] == "customer")]["charge (imperial)"] 
        == rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] == "customer")]["charge (metric)"]
    ).all()
    assert (rate_df.loc[(rate_df["utility"] == "electric") & (rate_df["type"] != "customer")]["basic_charge_limit (imperial)"] 
        == rate_df.loc[(rate_df["utility"] == "electric") & (rate_df["type"] != "customer")]["basic_charge_limit (metric)"]
    ).all()
    assert (rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] != "customer")]["basic_charge_limit (imperial)"] * 2.83168
        == rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] != "customer")]["basic_charge_limit (metric)"]
    ).all() 


    # Check that gross electricity demand is either equal to or twice that of electric grid demand
    # and that natural gas demand is either 0 or electricity * conversion_factor
    conversion_factor = 3600 / (105.5 * 10) # see paper for details
    assert (
        row["Est. Design Electricity Demand (MW)"].iloc[0] == pytest.approx(row["Est. Design Electric Grid Demand (MW)"].iloc[0])
        or (
            row["Est. Design Electricity Demand (MW)"].iloc[0] / 2 == pytest.approx(row["Est. Design Electric Grid Demand (MW)"].iloc[0])
            and (
                row["Est. Design Electric Grid Demand (MW)"].iloc[0] 
                == pytest.approx(row["Est. Design Natural Gas Demand (therms/hr)"].iloc[0] / conversion_factor)
            )
        )
    )
    
    assert (
        row["Est. Existing Electricity Demand (MW)"].iloc[0] == pytest.approx(row["Est. Existing Electric Grid Demand (MW)"].iloc[0])
        or (
            row["Est. Existing Electricity Demand (MW)"].iloc[0] / 2 == pytest.approx(row["Est. Existing Electric Grid Demand (MW)"].iloc[0])
            and (
                row["Est. Existing Electric Grid Demand (MW)"].iloc[0] 
                == pytest.approx(row["Est. Existing Natural Gas Demand (therms/hr)"].iloc[0] / conversion_factor)
            )
        )
    )

    # Check that treatment flow and natural gas demand conversions are correct
    row["Est. Existing Natural Gas Demand (m3/hr)"].iloc[0] == pytest.approx(row["Est. Existing Natural Gas Demand (therms/hr)"].iloc[0] * 2.83168)
    row["Est. Design Natural Gas Demand (m3/hr)"].iloc[0] == pytest.approx(row["Est. Design Natural Gas Demand (therms/hr)"].iloc[0] * 2.83168)
    row["Existing Total Flow (m3/d)"].iloc[0] == pytest.approx(row["Existing Total Flow (MGD)"].iloc[0] * 3785.41178)
    row["Design Flow (m3/d)"].iloc[0] == pytest.approx(row["Design Flow (MGD)"].iloc[0] * 3785.41178)


