#! /usr/bin/env python3

import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import seaborn as sns

# utility functions for colours https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s11.html
import math


def floatRgb(mag, cmin, cmax):
    """ Return a tuple of floats between 0 and 1 for R, G, and B. """
    # Normalize to 0-1
    try:
        x = float(mag - cmin) / (cmax - cmin)
    except ZeroDivisionError:
        x = 0.5  # cmax == cmin
    blue = min((max((4 * (0.75 - x), 0.)), 1.))
    red = min((max((4 * (x - 0.25), 0.)), 1.))
    green = min((max((4 * math.fabs(x - 0.5) - 1., 0.)), 1.))
    return red, green, blue


def rgb(mag, cmin, cmax):
    """ Return a tuple of integers, as used in AWT/Java plots. """
    red, green, blue = floatRgb(mag, cmin, cmax)
    return int(red * 255), int(green * 255), int(blue * 255)


def strRgb(mag, cmin, cmax):
    """ Return a hex string, as used in Tk plots. """
    return "#%02x%02x%02x" % rgb(mag, cmin, cmax)


df = pd.read_csv('analysis.csv')

# Output 1: Pretty print table of games by combined ACPL
# Cols = Year, Game #, White, Black, Comb. ACPl
cols_to_get = [1, 2, 3, 6, 9]
pretty_df = df[df.columns[cols_to_get]]
#print(pretty_df.sort_values('Combined ACPL', ascending=True))

# Output 2: Match ACPL violin plots vs. time


def unweighted_combined_acpls(df):
    df_copy = df.copy()
    grouped = df_copy.groupby('Year')
    df_copy['Combined Unweighted AVG ACPL'] = df_copy['White ACPL'] + df_copy['Black ACPL']
    return grouped['Combined Unweighted AVG ACPL'].mean().to_frame(name='acpl').reset_index()


def weighted_combined_acpls(df):
    df_copy = df.copy()
    grouped = df_copy.groupby('Event')
    df_copy['Combined Weighted AVG ACPL'] = \
        df_copy['White ACPL'] / grouped['White Num Moves'].transform('sum') * df_copy['White Num Moves'] + \
        df_copy['Black ACPL'] / grouped['Black Num Moves'].transform('sum') * df_copy['Black Num Moves']
    return grouped['Combined Weighted AVG ACPL'].sum(min_count=1)


# print(unweighted_combined_acpls(df))
# print(weighted_combined_acpls(df))


sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(figsize=(12, 9))
"""axes.set_title('Combined ACPL by WC Year')
axes.set_xlabel('Year')
axes.set_ylabel('Combined ACPL')
axes.yaxis.grid(True)

sns.boxenplot(x='Year', y='Combined ACPL', data=df, ax = axes)
axes.set_title('Combined ACPL by WC Year')
axes.set_xticklabels(axes.get_xticklabels(), rotation=60)
plt.savefig('boxenplot.png')
plt.cla()

color_df = unweighted_combined_acpls(df)
highest_acpl = color_df['acpl'].max()

color_df['color'] = color_df.apply(lambda row: strRgb(row['acpl'], 0, highest_acpl), axis=1)

palette = list(color_df.color)
"""

champs = pd.read_csv('champs.csv')
df = pd.merge(df, champs, how='left')
pd.options.display.width = 0

palette = {WC: color for (WC, color) in zip(df.WC.unique(), sns.color_palette() + sns.color_palette("pastel"))}
print(df)
axes.set_ylim(0, 150)
sns.boxplot(x='Year', y='Combined ACPL', data=df, ax=axes, hue="WC", palette=palette, dodge=False)
axes.set_title('Combined ACPL by WC Year')
axes.set_xticklabels(axes.get_xticklabels(), rotation=60)
plt.savefig('boxplot_color_champ.png')
plt.show()
plt.cla()
"""
sns.violinplot(x='Year', y='Combined ACPL', data=df, ax = axes, linewidth = 0.01)
axes.set_title('Combined ACPL by WC Year')
axes.set_xticklabels(axes.get_xticklabels(), rotation=60)
plt.savefig('violinplot.png')
plt.cla()

sns.stripplot(x='Year', y='Combined ACPL', data=df, ax=axes)
axes.set_title('Combined ACPL by WC Year')
axes.set_xticklabels(axes.get_xticklabels(), rotation=60)
plt.savefig('stripplot.png')
plt.cla()

sns.barplot(x='Year', y='Combined ACPL', data=df, ax=axes)
axes.set_title('Combined ACPL by WC Year')
axes.set_xticklabels(axes.get_xticklabels(), rotation=60)
plt.savefig('barplot.png')
plt.cla()

# Some graphs with scaled x-axes
sns.scatterplot(x='Year', y='Combined ACPL', data=df, ax=axes, hue='Year')
axes.set_title('Combined ACPL by WC Year')
plt.savefig('scatterplot.png')
plt.cla()

fig, axes = plt.subplots(figsize=(12, 9))
sns.regplot(x="Year", y="Combined ACPL", data=df)
axes.set_title('Combined ACPL by WC Year')
plt.savefig('regplot.png')
plt.cla()

fig, axes = plt.subplots(figsize=(12, 9))
sns.lmplot(x="Year", y="Combined ACPL", data=df)
axes.set_title('Combined ACPL by WC Year')
plt.savefig('lmplot.png')
plt.cla()

# Output 3: All WC games, plotted by combined ACPL vs. num moves
# To illustrate acpl isnt perfect and improves in long games
fig, axes = plt.subplots(figsize=(12, 9))
sns.scatterplot(x='White Num Moves', y='Combined ACPL', hue='Year', data=df)
axes.set_ylim((-5, 105))
plt.savefig('gamelengthscatterplot.png')

# In retrospect this plot is hard to read and not conclusive.
"""
