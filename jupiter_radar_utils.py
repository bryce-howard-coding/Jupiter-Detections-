import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
from datetime import datetime

def plot_day(df, date_str, show_plot=True, filename_out=False):
    day_df = df[df['Date'] == datetime.strptime(date_str, "%Y-%m-%d").date()].copy()
    if day_df.empty:
        print(f"No data found for {date_str}")
        return

    day_df['datetime'] = pd.to_datetime(day_df['datetime'])
    day_df = day_df.sort_values('datetime')
    freqs = sorted(day_df['Freq_MHz'].unique())

    fixed_num_rows = 3
    fixed_num_cols = 5

    fig, axes = plt.subplots(
        fixed_num_rows, fixed_num_cols,
        figsize=(15, fixed_num_rows * 3.5),
        sharex=False
    )
    axes_flat = axes.flatten()

    fig.suptitle(f"Jupiter Emission on {date_str}", fontsize=20, y=0.98)
    fig.text(0.5, 0.93, "Stokes I_Peak_Jy and V_Peak_Jy", ha='center', fontsize=14)

    hour_fmt = DateFormatter('%H')
    hour_locator = HourLocator(interval=1)

    day_start = datetime.strptime(date_str, "%Y-%m-%d").replace(hour=3, minute=0, second=0)
    day_end   = datetime.strptime(date_str, "%Y-%m-%d").replace(hour=12, minute=0, second=0)

    for i, freq in enumerate(freqs):
        if i >= len(axes_flat):
            print(f"Warning: More frequencies ({len(freqs)}) than available subplots.")
            break

        ax = axes_flat[i]
        sub = day_df[day_df['Freq_MHz'] == freq]

        ax.plot(sub['datetime'], sub['I_Peak_Jy'], label='Stokes I',
                color='tab:blue', marker='o', ms=4)
        ax.plot(sub['datetime'], sub['V_Peak_Jy'], label='Stokes V',
                color='tab:red', marker='o', ms=4)

        ax.set_ylabel(f"{freq} MHz (Jy)")
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', fontsize='small')

        ax.set_xlim(day_start, day_end)
        ax.xaxis.set_major_locator(hour_locator)
        ax.xaxis.set_major_formatter(hour_fmt)
        ax.tick_params(axis='x', labelrotation=0)

    for j in range(len(freqs), len(axes_flat)):
        axes_flat[j].set_visible(False)

    for ax in axes_flat:
        if ax.get_visible():
            ax.set_xlabel("Hour (UTC)")

    plt.tight_layout(rect=[0, 0, 1, 0.94])

    if show_plot:
        plt.show()
    if filename_out:
        plt.savefig(filename_out)

