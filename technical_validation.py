import pandas as pd

chp_info = pd.read_csv("CHP_Info.csv")
old_mgd = 50

for cwns_no in chp_info["CWNS_No"]:
    # 1) Check CWNS number is valid and CHP info is correct
    info_df = pd.read_excel("WWTP_Billing.xls", sheet_name=str(cwns_no), nrows=7, header=None)
    rate_df = pd.read_excel("WWTP_Billing.xls", sheet_name=str(cwns_no), header=8)

    if not old_mgd <= current_mgd:
        print(cwns_no)
        print(info_df.iloc[0, 1])
    assert info_df.iloc[0, 1] == cwns_no
    assert (info_df.iloc[4, 1] == chp_info[chp_info["CWNS_No"] == cwns_no]["Has CHP"]).all()

    # 2) Check that MGD is increasing with each sheet, within bounds of smallest/largest
    current_mgd = info_df.iloc[3, 1]
    assert old_mgd <= current_mgd
    old_mgd = current_mgd

    # 3) Check that all days of a year are included

    # 4) prices are positive and below a threshold

    # 5) units (i.e. demand is in kW and energy in kWh)

    # 6) something with "on-peak" in name is more expensive than "off-peak"

    # 7) estimate costs and compare to known values (use SVCW energy demand)

    # 8) gas data YES / NO (quality flag?)
