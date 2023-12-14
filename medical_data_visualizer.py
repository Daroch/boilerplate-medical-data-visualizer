import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['bmi']= df['weight']/(df['height']/100)**2
df['overweight']= np.where(df['bmi']>25, 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['gluc'] = np.where(df['gluc']<=1, 0, 1)
df['cholesterol'] = np.where(df['cholesterol']<=1, 0, 1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_long=pd.melt(df,
                id_vars=["id","cardio"],
                value_vars=["active","alco","cholesterol","gluc","overweight","smoke"])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.


    # Draw the catplot with 'sns.catplot()'
    grid = sns.catplot(x="variable",hue="value",
                kind="count", legend=True,col="cardio",
                data=df_long)
    grid.set(xlabel="variable", ylabel="total",title="")
    # Get the figure for the output
    fig=grid.figure
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    condition = df['ap_lo'] <= df['ap_hi']
    df_clean = df[condition]

    condition = df_clean['height'] >= df_clean['height'].quantile(0.025)
    df_clean = df_clean[condition]

    condition = df_clean['height'] <= df_clean['height'].quantile(0.975)
    df_clean = df_clean[condition]

    condition = df_clean['weight'] >= df_clean['weight'].quantile(0.025)
    df_clean = df_clean[condition]

    condition = df_clean['weight'] <= df_clean['weight'].quantile(0.975)
    df_clean = df_clean[condition]

    df_clean = df_clean.drop("bmi", axis=1)

    # Calculate the correlation matrix
    corr = df_clean.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))




    # Set up the matplotlib figure
    fig = plt.figure(figsize=(15,15))
    
    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(df_clean.corr(), annot=True, mask=mask, fmt=".2f")
    sns.set(font_scale=.8)


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
