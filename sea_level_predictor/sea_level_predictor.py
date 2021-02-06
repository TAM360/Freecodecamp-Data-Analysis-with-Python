import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():

    # Read data from file
    df = pd.read_csv("epa-sea-level.csv")
    df["CSIRO Adjusted Sea Level"] = df["CSIRO Adjusted Sea Level"].astype(float)
    df["Year"] = df["Year"].astype(int)

    # Create scatter plot
    y_data = df["CSIRO Adjusted Sea Level"]
    x_data = df["Year"]
    plt.scatter(x_data, y_data)

    # Create first line of best fit
    bf_line_1 = linregress(x_data, y_data)
    intercept_1 = bf_line_1.intercept
    slope_1 = bf_line_1.slope
    x1 = pd.Series([i for i in range(1880, 2050)])
    y1 = intercept_1 + (slope_1 * x1)

    # print(f"best fit 1 => slope: {slope_1} | y-intercept: {intercept_1}")

    plt.plot(
        x1,
        y1,
        "r",
        label="best fit line 1",
        color="green",
    )

    # Create second line of best fit
    df2 = df[df["Year"] >= 2000]
    y_data_2 = df2["CSIRO Adjusted Sea Level"]
    x_data_2 = df2["Year"]
    bf_line_2 = linregress(x_data_2, y_data_2)
    intercept_2 = bf_line_2.intercept
    slope_2 = bf_line_2.slope

    # print(f"best fit 2 => slope: {slope_2} | y-intercept: {intercept_2}")

    x2 = pd.Series([float(i) for i in range(2000, 2050)])
    y2 = intercept_2 + (slope_2 * x2)

    plt.plot(
        x2,
        y2,
        "r",
        label="best fit line 2",
        color="yellow",
    )

    # Add labels and title
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.title("Rise in Sea Level")
    # plt.show()

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig("sea_level_plot.png")

    return plt.gca()