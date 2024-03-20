import os
import warnings
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

# change to repo parent directory and suppress superfluous openpyxl warnings
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def get_charge_array(consumption_data, rate_data, charge_type, utility="electric"):
    """Gets an array with customer, demand, or energy charges (i.e. `charge_type`)
    specific to each day/time

    Parameters
    ----------
    consumption_data : DataFrame
        Baseline electrical usage data. Determines which dates and times
        to gather rate information. Column headers omitted due to size.
        See 'data/baseline_noCHP.csv' for an example.

    rate_data : DataFrame
        Electric and gas billing information

        ==================  ===========================================================
        utility             type of utility {'electric', 'gas'}
        type                type of charge {'customer', 'demand', 'energy'}
        period              period used to calculate demand charge (as `str`)
        basic_charge_limit (imperial)  the limit in imperial units at which the charge comes into effect (as `int`)
        basic_charge_limit (metric)  the limit in metric units at which the charge comes into effect (as `int`)
        month_start         first month for which the charge applies {1-12}
        month_end           last month for which the charge applies {1-12}
        hour_start          hour at which the charge begins {0-24}
        hour_end            hour at which the charge ends {0-24}
        weekday_start       first day on which the charge applies {0-6}
        weekday_end         last day for which the charge applies {0-6}
        charge (imperial)   cost of service per unit gas (therm, therm/hr) or electricity (kW, kWh) (as `int`)
        charge (metric)     cost of service per unit gas (m3, m3/hr) or electricity (kW, kWh)(as `int`)
        units               units of `basic_charge_limit` and `charge` (as `str`)
        ==================  ===========================================================

    charge_type : {'customer', 'demand', 'energy'}
        Type of charge to look up

    utility : {'electric', 'gas'}
        Type of utility to look up

    Raises
    ------
    ValueError
        When invalid `charge_type` is entered

    KeyError
        When `consumption_data` does not have 'DateTime' column

    Returns
    -------
    array
        A structured array of arrays with the name of each array corresponding
        to the basic charge limit which applies to the array of charges
        corresponding to the given utility and charge type and
        for each hour, day, and month
    """
    ndays = int(consumption_data.shape[0] / 96)
    # first search for the correct charge type, then correct utility
    charges = rate_data.loc[(rate_data["type"] == charge_type), :]
    charges = charges.loc[charges["utility"] == utility, :]
    if charge_type == "customer":
        return charges["charge (imperial)"].values
    periods = charges["period"].values
    charge_limits = charges["basic_charge_limit (imperial)"]
    weekdays = consumption_data["DateTime"].dt.weekday.values
    months = consumption_data["DateTime"].dt.month.values
    hours = consumption_data["DateTime"].dt.hour.astype(float).values
    # Make sure hours are being incremented by 15-minute increments
    hours += np.tile(np.arange(4) / 4, 24 * ndays)

    # if no charge was listed for this utility and charge_type, return 0
    if charge_type == "demand":
        if charges.shape[0] == 0:
            data = np.zeros((ndays * 96, 1))
            return np.array(data, dtype=[("0.0", float)])
    elif charge_type == "energy":
        if charges.shape[0] == 0:
            data = np.zeros(ndays * 96)
            return np.array(data, dtype=[("0.0", float)])
    else:
        raise ValueError("Invalid charge_type: " + charge_type)

    charge_array = np.array([])
    for limit in np.unique(charge_limits):
        limit_charges = charges.loc[charges["basic_charge_limit (imperial)"] == limit, :]
        if charge_type == "demand":
            data = np.zeros((ndays * 96, limit_charges.shape[0]))
        else:
            data = np.zeros(ndays * 96)
        periods_seen = {}
        for idx in limit_charges.index:
            charge = limit_charges.loc[idx, :]
            idx_np = idx - min(limit_charges.index.values)
            period = periods[idx_np]
            apply_charge = (
                (months >= charge["month_start"])
                & (months <= charge["month_end"])
                & (weekdays >= charge["weekday_start"])
                & (weekdays <= charge["weekday_end"])
                & (hours >= charge["hour_start"])
                & (hours < charge["hour_end"])
            )
            if charge_type == "demand":
                # Need to make sure to add DR charges for a non-contigious period to the same column!
                if period not in periods_seen:
                    periods_seen[period] = (idx_np, apply_charge)
                else:
                    idx_np = periods_seen[period][0]
                    apply_charge = apply_charge | periods_seen[period][1]
                data[:, idx_np] = apply_charge * charge["charge (imperial)"]
            else:
                data += apply_charge * charge["charge (imperial)"]
        if charge_array.size == 0:
            charge_array = np.array(data, dtype=[(str(limit), float)])
        else:
            new_charge_array = np.empty(
                charge_array.shape, charge_array.dtype.descr + [(str(limit), float)]
            )
            for n in charge_array.dtype.names:
                new_charge_array[n] = charge_array[n]
            new_charge_array[str(limit)] = data

            charge_array = new_charge_array

    return charge_array



def last_day_of_month(any_day):
    """From: https://stackoverflow.com/questions/42950/how-to-get-the-last-day-of-the-month"""
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + dt.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - dt.timedelta(days=next_month.day)


elec_col = "grid_to_plant_kW"
ng_col = "natural_gas_therm_per_hr"

# Load energy consumption and rates
energy_df = pd.read_csv("data/synthetic_energy_data.csv")
metadata = pd.read_csv("data/metadata.csv")
metrics_df = pd.DataFrame(columns = ["cwns", "month", "mean_energy", "peak_energy_ratio", "num_energy_tiers", "max_demand", "peak_demand_ratio", "num_demand_tiers"])

# Use the helper functions above to get charge arrays
for cwns_no in metadata["CWNS_No"]:
    print(cwns_no)
    rate_df = pd.read_excel("data/WWTP_Billing.xlsx", sheet_name=str(cwns_no))
    months = [7, 12]
    for month in months:
        case_metrics = {}
    # Find start and end index of this month
        energy_df["DateTime"] = pd.to_datetime(energy_df["DateTime"])
        month_start = dt.datetime(2021, month, 1, 0, 0, 0)
        start_idx = (energy_df["DateTime"] == month_start).idxmax()
        month_end = last_day_of_month(dt.datetime(2021, month, 1, 0, 0, 0)) + dt.timedelta(hours=23, minutes=45)
        end_idx = (energy_df["DateTime"] == month_end).idxmax()

        # collect the charge arrays
        electric_demand_charges = get_charge_array(
            consumption_data = energy_df.loc[start_idx:end_idx],
            rate_data = rate_df,
            charge_type = "demand",
            utility = "electric"
        )
        electric_energy_charges = get_charge_array(
            consumption_data = energy_df.loc[start_idx:end_idx],
            rate_data = rate_df,
            charge_type = "energy",
            utility="electric"
        )
        mean_baseload = energy_df[elec_col].loc[start_idx:end_idx].mean()
        max_baseload = energy_df[elec_col].loc[start_idx:end_idx].max()

        # find the number of tiers
        num_energy_tiers = len(electric_energy_charges.dtype.names)
        num_demand_tiers = len(electric_demand_charges.dtype.names)            
        
        # find the mean electric_energy_charges
        name = electric_energy_charges.dtype.names[-1]
        mean_energy = electric_energy_charges[name].mean()
        max_energy = electric_energy_charges[name].max()
        min_energy = electric_energy_charges[name].min()
        if min_energy == 0 and max_energy == 0:
            peak_energy_ratio = 1
        elif min_energy == 0:
            peak_energy_ratio = 0
        else:
            peak_energy_ratio = max_energy / min_energy

        name = electric_demand_charges.dtype.names[-1]
        
        # find the mean demand + peak demand ratio
        accumulated_demand = np.sum(electric_demand_charges[name], axis=1)
        max_demand = accumulated_demand.max()
        min_demand = accumulated_demand.min()
        if min_demand == 0 and max_demand == 0:
            peak_demand_ratio = 1
        elif min_demand == 0:
            peak_demand_ratio = 0
        else:
            peak_demand_ratio = max_demand / min_demand

        case_metrics = pd.DataFrame({
            "cwns": cwns_no,
            "month": month,
            "mean_energy": mean_energy,
            "peak_energy_ratio": peak_energy_ratio,
            "num_energy_tiers": num_energy_tiers,
            "max_demand": max_demand,
            "peak_demand_ratio": peak_demand_ratio,
            "num_demand_tiers": num_demand_tiers
        }, index=[0])

        # save results in metrics_df
        metrics_df = pd.concat([metrics_df, case_metrics], ignore_index=True)

# save metrics_df as a csv
metrics_df.to_csv("data/metrics.csv", index=False)

metrics_df_7 = metrics_df.loc[metrics_df["month"] == 7].loc[metrics_df["cwns"] > 3]
metrics_df_12 = metrics_df.loc[metrics_df["month"] == 12].loc[metrics_df["cwns"] > 3]
metrics_df_sce_7 = metrics_df.loc[metrics_df["month"] == 7].loc[metrics_df["cwns"] == 1]
metrics_df_sbce_7 = metrics_df.loc[metrics_df["month"] == 7].loc[metrics_df["cwns"] == 2]
metrics_df_sce_12 = metrics_df.loc[metrics_df["month"] == 12].loc[metrics_df["cwns"] == 1]
metrics_df_sbce_12 = metrics_df.loc[metrics_df["month"] == 12].loc[metrics_df["cwns"] == 2]

# plot the results
plt.rcParams.update({'axes.labelsize': 18,
                    'xtick.labelsize': 16,
                    'xtick.major.width': 1,
                    'ytick.labelsize': 16,
                    'ytick.major.width': 1,
                    'legend.fontsize': 16,
                    'font.size': 16,
                    'font.family': 'sans-serif',
                    'font.sans-serif': 'Arial',
                    'mathtext.fontset': 'dejavusans',
                    'axes.linewidth': 1,
                    'lines.linewidth': 1.,
                    'lines.markersize': 1.})


fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(metrics_df_7["mean_energy"], 
           metrics_df_7["peak_energy_ratio"], 
           label="July", 
           color = 'C2', alpha = 0.5,
           marker = 'o', s = 30)
ax.scatter(metrics_df_12["mean_energy"], 
           metrics_df_12["peak_energy_ratio"], 
           label="December", 
           color = 'C0', alpha = 0.5,
           marker = 'o', s = 30)
ax.scatter(metrics_df_sbce_7["mean_energy"],
              metrics_df_sbce_7["peak_energy_ratio"],
              color = 'C2', alpha = 0.9,
              marker = '*', s = 125)
ax.scatter(metrics_df_sce_7["mean_energy"],
                metrics_df_sce_7["peak_energy_ratio"],
                color = 'C2', alpha = 0.9,
                marker = 'D', s = 75)
ax.scatter(metrics_df_sbce_12["mean_energy"],
                metrics_df_sbce_12["peak_energy_ratio"],
                color = 'C0', alpha = 0.9,
                marker = '*', s = 125)
ax.scatter(metrics_df_sce_12["mean_energy"],
                metrics_df_sce_12["peak_energy_ratio"],
                color = 'C0', alpha = 0.9,
                marker = 'D', s = 75)
ax.hlines(1, 0, 0.25, linestyles='dashed', colors='k')
ax.set_xlabel("Mean Energy Charge ($/kWh)")
ax.set_ylabel("Peak : Off-Peak Energy Ratio")
# set ticks
ax.set_xlim(0, 0.25)
ax.set_ylim(-0.1, 5)
ax.set_xticks(np.arange(0, 0.3, 0.05))
ax.set_yticks(np.arange(0, 6, 1))
ax.set_title("Energy Charges")
fig.tight_layout()
# save in all formats
fig.savefig("figures/energy_charges.png", dpi=300)
fig.savefig("figures/energy_charges.svg", dpi=300)
fig.savefig("figures/energy_charges.pdf", dpi=300)


# plot the results for demand charges
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(metrics_df_7["max_demand"], 
           metrics_df_7["peak_demand_ratio"], 
           label="July", 
           color = 'C2', alpha = 0.5,
           marker = 'o', s = 30)
ax.scatter(metrics_df_12["max_demand"],
              metrics_df_12["peak_demand_ratio"],
              label="December",
              color = 'C0', alpha = 0.5,
              marker = 'o', s = 30)
ax.scatter(metrics_df_sbce_7["max_demand"],
                metrics_df_sbce_7["peak_demand_ratio"],
                color = 'C2', alpha = 0.9,
                marker = '*', s = 125)
ax.scatter(metrics_df_sce_7["max_demand"],
                metrics_df_sce_7["peak_demand_ratio"],
                color = 'C2', alpha = 0.9,
                marker = 'D', s = 75)
ax.scatter(metrics_df_sbce_12["max_demand"],
                metrics_df_sbce_12["peak_demand_ratio"],
                color = 'C0', alpha = 0.9,
                marker = '*', s = 125)
ax.scatter(metrics_df_sce_12["max_demand"],
                metrics_df_sce_12["peak_demand_ratio"],
                color = 'C0', alpha = 0.9,
                marker = 'D', s = 75)
ax.hlines(1, 0, 60, linestyles='dashed', colors='k')
ax.set_xlabel("Max Demand Charge ($/kW)")
ax.set_ylabel("Peak : Off-Peak Demand Ratio")
# # set ticks
ax.set_xlim(0, 50)
ax.set_ylim(-0.1, 20)
ax.set_xticks(np.arange(0, 60, 10))
ax.set_yticks(np.arange(0, 25, 5))
ax.set_title("Demand Charges")
fig.tight_layout()
# save in all formats
fig.savefig("figures/demand_charges.png", dpi=300)
fig.savefig("figures/demand_charges.svg", dpi=300)
fig.savefig("figures/demand_charges.pdf", dpi=300)


from matplotlib import dates as mdates
fmt = mdates.DateFormatter('%d')

fig, ax = plt.subplots(figsize=(6, 5), nrows=2)
ax[0].set_title("Energy Charges ($/kWh)")
ax[0].plot(energy_df.loc[start_idx:end_idx]["DateTime"], electric_energy_charges)
ax[0].set_xlim(energy_df.loc[start_idx:end_idx]["DateTime"].min(), energy_df.loc[start_idx:end_idx]["DateTime"].max())
ax[0].set_ylim(0, 0.3)
ax[0].set_yticks(np.arange(0, 0.4, 0.1))
ax[0].set_xlabel("Day of the Month")
ax[0].xaxis.set_major_formatter(fmt)
ax[0].set_xticks(energy_df.loc[start_idx:end_idx]["DateTime"][::96*2])

ax[1].set_title("Demand Charges ($/kW)")
ax[1].plot(energy_df.loc[start_idx:end_idx]["DateTime"], electric_demand_charges)
ax[1].set_xlim(energy_df.loc[start_idx:end_idx]["DateTime"].min(), energy_df.loc[start_idx:end_idx]["DateTime"].max())
ax[1].set_ylim(0, 10)
ax[1].set_yticks(np.arange(0, 12.5, 2.5))
ax[1].set_xlabel("Day of the Month")
ax[1].xaxis.set_major_formatter(fmt)
ax[1].set_xticks(energy_df.loc[start_idx:end_idx]["DateTime"][::96*2])

fig.tight_layout()
fig