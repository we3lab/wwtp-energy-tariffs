import pandas as pd

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

chp_info = pd.read_csv("CHP_Info.csv")
old_mgd = 50
max_mgd = 812
max_charges = {"electric_demand": 35, "electric_energy": 2, "gas_energy": 3,
               "gas_demand": 1.5, "gas_customer": 5000, "electric_customer": 5000}

for cwns_no in chp_info["CWNS_No"]:
    # 1) Check CWNS number is valid and CHP info is correct
    info_df = pd.read_excel("WWTP_Billing.xls", sheet_name=str(cwns_no), nrows=7, header=None)
    rate_df = pd.read_excel("WWTP_Billing.xls", sheet_name=str(cwns_no), header=8)

    assert info_df.iloc[0, 1] == cwns_no
    assert (info_df.iloc[4, 1] == chp_info[chp_info["CWNS_No"] == cwns_no]["Has CHP"]).all()

    # 2) Check that MGD is increasing with each sheet, within bounds of smallest/largest
    current_mgd = info_df.iloc[3, 1]
    assert old_mgd <= current_mgd
    assert current_mgd <= max_mgd
    old_mgd = current_mgd

    utilities = rate_df["utility"].unique()
    # 3) If has_chp, need gas (otherwise just electric)
    if info_df.iloc[4, 1] == "Yes":
        assert "gas" in utilities

    for utility in utilities:
        for charge_type in rate_df.loc[rate_df["utility"] == utility]["type"].unique():
            # 4) Check that all days of a year are included
            slice = rate_df.loc[(rate_df["utility"] == utility) & (rate_df["type"] == charge_type)]
            assert check_continuity(slice, charge_type)

            # 5) prices are positive and below a threshold
            # Many checked the outliers in the if statement are correct
            if not ((cwns_no == 42005016001 and charge_type == "customer")
                or ((cwns_no == 36002001007 or cwns_no == 36002001010 or cwns_no == 36002001004
                     or cwns_no == 36002001009 or cwns_no == 36002001006 or cwns_no == 36003169012
                     or cwns_no == 36002001005 or cwns_no == 36002001002 or cwns_no == 36002001003
                     or cwns_no == 36002001012 or cwns_no == 36002001001 or cwns_no == 36002001011)
                     and utility == "gas" and charge_type == "energy")):
                assert slice["charge"].min() >= 0
                assert slice["charge"].max() <= max_charges[utility + "_" + charge_type]

    # 6) units (i.e. demand is in kW and energy in kWh)
    assert (rate_df.loc[rate_df["type"] == "customer"]["units"] == "$/month").all()
    assert (rate_df.loc[(rate_df["type"] == "demand") & (rate_df["utility"] == "electric")]["units"] == "$/kW").all()
    assert (rate_df.loc[(rate_df["type"] == "energy") & (rate_df["utility"] == "electric")]["units"] == "$/kWh").all()
    assert (rate_df.loc[(rate_df["utility"] == "gas") & (rate_df["type"] != "customer")]["units"] == "$/therm").all()

    # 7) estimate costs and compare to known values (use SVCW energy demand)
