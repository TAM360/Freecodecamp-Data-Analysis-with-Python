import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date")

# Clean data
df = df[
    (df["value"].quantile(0.025) < df["value"])
    & (df["value"] < df["value"].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig = df.plot.line(rot="30").figure

    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.reset_index()
    df_bar["year"] = pd.to_datetime(df_bar["date"]).dt.year
    df_bar["month"] = pd.to_datetime(df_bar["date"]).dt.strftime("%B")

    df_bar = df_bar.groupby(by=["year", "month"]).mean().unstack(1)
    df_bar = df_bar.fillna(0)

    months = (
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    )

    # print("years =>\n", df_bar)
    # print("months =>\n", months)

    # Draw bar plot
    fig = df_bar.plot.bar().figure

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Month", labels=months)

    # plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.sort_values(by="date").copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = pd.to_datetime(df_box["date"]).dt.year
    df_box["month"] = pd.to_datetime(df_box["date"]).dt.strftime("%b")

    months = (
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    )

    # Create a pyplot having 2 different charts and get there axes.
    _, (ax1, ax2) = plt.subplots(1, 2)

    # Draw box plots (using Seaborn)
    # Assign each axis to the seaborn's boxplot method with relevent
    # columns.
    ax = sns.boxplot(ax=ax1, x="year", y="value", data=df_box)
    ax.set(xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)")
    ax = sns.boxplot(ax=ax2, x="month", y="value", order=months, data=df_box)
    ax.set(
        xlabel="Month",
        ylabel="Page Views",
        title="Month-wise Box Plot (Seasonality)",
    )

    plt.show()

    # Save image and return fig (don't change this part)
    ax.figure.savefig("box_plot.png")
    return ax.figure
