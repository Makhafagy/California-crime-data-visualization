import california
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.ticker as mtick

summary = california.combined_data

with sns.axes_style("white"):
    g = sns.FacetGrid(summary, col="crime_report_year", margin_titles=True, height=2.5, col_wrap=3, hue='crime_report_year')

g.map(sns.regplot, "crime_rate", "price_avg_this_year", scatter=False, color='black', line_kws={"linewidth": 1})
g.map(sns.scatterplot, "crime_rate", "price_avg_this_year", edgecolor="w")

for ax in g.axes.flat:
    ax.set_ylabel("Average House Price")
    ax.set_xlabel("Crime Rate")
    
plt.ticklabel_format(style='plain', axis='y')

plt.show()
