from numpy.lib.function_base import quantile
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
# NOTE: height values in CSV file are in centemeters not meters.
df["overweight"] = df["weight"] / (df["height"] / 100) ** 2  # calculate BMI 1st
# print("overweight stats =>\n", df["overweight"])
df["overweight"] = np.where(
    df["overweight"] > 25, 1, 0
)  # if BMI is > 25 then person is overweight else not

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["gluc"] = np.where(df["gluc"] > 1, 1, 0)
df["cholesterol"] = np.where(df["cholesterol"] > 1, 1, 0)

# print("normalized data =>\n", df)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df[
        ["active", "alco", "cholesterol", "gluc", "overweight", "smoke", "cardio"]
    ].melt(
        id_vars=["cardio"],
    )

    # print("unpivoted dataframe =>\n", df_cat)

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    # NOTE: catploy can be generated without reformating the un-pivoted dataframe.
    # df_cat = None

    # Draw the catplot with 'sns.catplot()'
    # NOTE: Since I haven't reformatted the df_cat dataframe, I need to explictly label y axis of graph 'total'.
    #       Also, use sns.catplot().fig to extract figure type object which contains get_children() & get_xlabel()
    #       methods. If you don't then the test module will throw the following exception:
    """     AttributeError: 'numpy.ndarray' object has no attribute 'get_children' """
    fig = (
        sns.catplot(
            data=df_cat,
            kind="count",
            x="variable",
            hue="value",
            col="cardio",
        )
        .set_ylabels("total")
        .fig
    )

    # plt.show()

    # Do not modify the next two lines
    fig.savefig("catplot.png")
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    blood_pressure_filter = df["ap_lo"] <= df["ap_hi"]
    height_filter = (df["height"] >= df["height"].quantile(2.5 / 100)) & (
        df["height"] <= df["height"].quantile(97.5 / 100)
    )
    weight_filter = (df["weight"] >= df["weight"].quantile(2.5 / 100)) & (
        df["weight"] <= df["weight"].quantile(97.5 / 100)
    )

    df_heat = df[(blood_pressure_filter) & (height_filter) & (weight_filter)]

    # print("df_heat result =>\n", df_heat)

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # print("correlation matrix =>\n", corr)

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the heatmap with 'sns.heatmap()'

    ax = sns.heatmap(corr, mask=mask, annot=True, fmt=".1f")

    # plt.show()

    # Do not modify the next two lines
    fig.savefig("heatmap.png")
    return fig
