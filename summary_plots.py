import california
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.ticker as mtick

summary = california.combined_data


# plt.bar(summary['crime_report_year'], summary['price_avg_this_year'])
# plt.xlabel('Year')
# plt.ylabel('House Prices')
# plt.title('Crime Rate over the Years')
# plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

# Create a facet grid with multiple histograms of sepal_width

with sns.axes_style("white"):
    g = sns.FacetGrid(summary, col="crime_report_year", margin_titles=True, height=2.5, col_wrap=3, hue='crime_report_year')
    
g.map(sns.scatterplot, "crime_rate", "price_avg_this_year")

for ax in g.axes.flat:
    ax.set_ylabel("Average House Price")
    ax.set_xlabel("Crime Rate")
    
plt.ticklabel_format(style='plain', axis='y')

plt.show()
