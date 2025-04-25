import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.patches as mpatches

# Data for countries: (name, population in millions, gini coefficient)
countries = [
    ("Sweden", 10.4, 0.27),
    ("Denmark", 5.8, 0.26),
    ("Finland", 5.5, 0.27),
    ("Norway", 5.4, 0.25),
    ("Germany", 83.2, 0.29),
    ("France", 67.4, 0.30),
    ("Japan", 125.8, 0.33),
    ("Canada", 38.0, 0.31),
    ("United Kingdom", 67.2, 0.35),
    ("Italy", 59.6, 0.33),
    ("Australia", 25.5, 0.32),
    ("United States", 331.0, 0.41),
    ("Russia", 144.1, 0.38),
    ("China", 1410.0, 0.38),
    ("Mexico", 128.9, 0.45),
    ("Brazil", 212.6, 0.53),
    ("India", 1380.0, 0.35),
    ("South Africa", 59.3, 0.63),
    ("Namibia", 2.5, 0.59),
    ("Haiti", 11.4, 0.61)
]

# Data for US cities: (name, population in millions, gini coefficient)
# Using more precise city-level Gini data
cities = [
    ("New York City", 8.80, 0.550),
    ("San Francisco", 0.87, 0.511),
    ("Palo Alto", 0.07, 0.522),
    ("Mountain View", 0.08, 0.494),
    ("Cupertino", 0.06, 0.457),
    ("Oakland", 0.43, 0.524),
    ("San Jose", 1.03, 0.485),
    ("Los Angeles", 3.97, 0.515),
    ("Chicago", 2.70, 0.485),
    ("Boston", 0.68, 0.519),
    ("Washington DC", 0.69, 0.542),
    ("Seattle", 0.74, 0.486),
    ("Miami", 0.45, 0.538),
    ("Las Vegas", 0.65, 0.475),
    ("Omaha", 0.48, 0.452),
    ("Topeka", 0.13, 0.446),
    ("Scranton", 0.08, 0.461),
    ("Detroit", 0.67, 0.480),
    ("Atlanta", 0.50, 0.572),
    ("San Diego", 1.39, 0.478),
    ("Austin", 0.95, 0.477)
]

# Create figure and axes
plt.figure(figsize=(14, 10))
ax = plt.subplot(111)

# Define categories for coloring
def get_category(gini):
    if gini < 0.30:
        return "Very Equal"
    elif gini < 0.35:
        return "Moderately Equal"
    elif gini < 0.45:
        return "Moderate Inequality"
    elif gini < 0.55:
        return "High Inequality"
    else:
        return "Extreme Inequality"

category_colors = {
    "Very Equal": "#2c7bb6",
    "Moderately Equal": "#abd9e9",
    "Moderate Inequality": "#ffffbf",
    "High Inequality": "#fdae61",
    "Extreme Inequality": "#d7191c"
}

# Process countries data
country_names = [c[0] for c in countries]
country_populations = np.array([c[1] for c in countries])
country_ginis = np.array([c[2] for c in countries])
country_categories = [get_category(g) for g in country_ginis]
country_colors = [category_colors[cat] for cat in country_categories]

# Process cities data
city_names = [c[0] for c in cities]
city_populations = np.array([c[1] for c in cities])
city_ginis = np.array([c[2] for c in cities])
city_categories = [get_category(g) for g in city_ginis]
city_colors = [category_colors[cat] for cat in city_categories]

# Create the scatter plot for countries
scatter_countries = ax.scatter(
    country_ginis, 
    country_populations, 
    s=np.sqrt(country_populations) * 5,  # Size points by sqrt of population
    c=country_colors, 
    alpha=0.7, 
    edgecolors='black', 
    linewidths=1,
    marker='o'
)

# Create the scatter plot for cities
scatter_cities = ax.scatter(
    city_ginis, 
    city_populations, 
    s=np.sqrt(city_populations) * 8,  # Size points by sqrt of population
    c=city_colors, 
    alpha=0.7, 
    edgecolors='black', 
    linewidths=1,
    marker='s'  # Square markers for cities
)

# Set log scale for y-axis
ax.set_yscale('log')

# Add labels for countries
for i, name in enumerate(country_names):
    # Only label selected countries to avoid crowding
    if name in ["United States", "China", "India", "Sweden", "South Africa", 
                "Germany", "Canada", "Mexico", "Brazil", "Japan", "United Kingdom"]:
        # Adjust text position
        y_offset = 0.1 if country_populations[i] < 20 else -0.1
        ha = 'center'
        
        ax.annotate(
            name, 
            (country_ginis[i], country_populations[i]),
            xytext=(0, y_offset),  # Offset text for readability
            textcoords='offset points',
            fontsize=9,
            ha=ha,
            fontweight='bold'
        )

# Add labels for cities
highlighted_cities = ["New York City", "San Francisco", "Palo Alto", "Omaha", 
                     "Topeka", "Scranton", "Las Vegas", "San Jose", "Mountain View", 
                     "Cupertino", "Oakland", "Atlanta"]

for i, name in enumerate(city_names):
    if name in highlighted_cities:
        # Create a shorter display name to save space
        display_name = name
        if name == "New York City":
            display_name = "NYC"
        elif name == "San Francisco":
            display_name = "SF"
            
        ax.annotate(
            display_name, 
            (city_ginis[i], city_populations[i]),
            xytext=(5, 0),  
            textcoords='offset points',
            fontsize=8,
            color='darkblue'
        )

# Add a title and labels
plt.title('Income Inequality (Gini) vs Population Size: Countries and US Cities', 
          fontsize=14, fontweight='bold')
plt.xlabel('Gini Coefficient (higher = more inequality)', fontsize=12)
plt.ylabel('Population (log scale)', fontsize=12)

# Format y-axis to show population in millions/thousands
def pop_formatter(x, pos):
    if x < 0.1:
        return f'{int(x*1000)}K'
    elif x < 1:
        return f'{int(x*1000)/10:.1f}K'
    else:
        return f'{x:.1f}M'

ax.yaxis.set_major_formatter(FuncFormatter(pop_formatter))

# Add US national average line
us_gini = 0.481  # US national average Gini
plt.axvline(x=us_gini, color='darkred', linestyle='--', alpha=0.5)
plt.text(us_gini+0.005, 0.06, 'US Avg', rotation=90, color='darkred')

# Create a legend for the inequality categories
from matplotlib.lines import Line2D
inequality_legend = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=category_colors["Very Equal"], 
           markersize=10, label='Very Equal (< 0.30)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=category_colors["Moderately Equal"], 
           markersize=10, label='Moderately Equal (0.30-0.35)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=category_colors["Moderate Inequality"], 
           markersize=10, label='Moderate Inequality (0.35-0.45)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=category_colors["High Inequality"], 
           markersize=10, label='High Inequality (0.45-0.55)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=category_colors["Extreme Inequality"], 
           markersize=10, label='Extreme Inequality (> 0.55)')
]

# Create a legend for entity type
type_legend = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
           markersize=10, label='Countries'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', 
           markersize=10, label='US Cities')
]

# Add both legends
ax.legend(handles=inequality_legend, loc='upper left', title='Inequality Categories')
ax.add_artist(plt.legend(handles=type_legend, loc='lower right', title='Entity Type'))

# Add grid for better readability
plt.grid(True, alpha=0.3)

# Set axis limits
plt.xlim(0.23, 0.65)
plt.ylim(0.05, 2000)

# Add Silicon Valley bounding box
silicon_valley_cities = ["San Francisco", "Palo Alto", "Mountain View", "Cupertino", "San Jose"]
sv_ginis = [city_ginis[city_names.index(city)] for city in silicon_valley_cities]
sv_pops = [city_populations[city_names.index(city)] for city in silicon_valley_cities]
min_gini_sv = min(sv_ginis) - 0.02
max_gini_sv = max(sv_ginis) + 0.02
min_pop_sv = min(sv_pops) * 0.7
max_pop_sv = max(sv_pops) * 1.5

rect = mpatches.Rectangle((min_gini_sv, min_pop_sv), max_gini_sv-min_gini_sv, max_pop_sv-min_pop_sv,
                          linewidth=2, edgecolor='green', facecolor='none', alpha=0.5, linestyle=':')
ax.add_patch(rect)
plt.text(min_gini_sv+0.005, max_pop_sv*1.1, "Silicon Valley Region", color='green', fontweight='bold')

# Add annotations
observations = [
    "US cities have significantly higher inequality than the US national average",
    "Silicon Valley cities show high inequality despite varying sizes",
    "Midwestern cities like Omaha and Topeka have lower inequality than coastal tech hubs",
    "Atlanta has the highest inequality among US cities in this dataset",
    "Tech hubs (SF, NYC) have comparable inequality to developing nations with much larger populations"
]

# Add a text box with observations
props = dict(boxstyle='round', facecolor='white', alpha=0.7)
ax.text(0.23, 0.13, '\n'.join(f"• {obs}" for obs in observations), transform=ax.transAxes, 
        fontsize=9, verticalalignment='top', bbox=props)

# Show the plot
plt.tight_layout()
plt.show()
