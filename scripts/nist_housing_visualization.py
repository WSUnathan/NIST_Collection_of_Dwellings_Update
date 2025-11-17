import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource, Legend, LegendItem
from bokeh.layouts import column, row
from bokeh.palettes import Category20, Set3
from bokeh.transform import cumsum, factor_cmap
from bokeh.models import Title
import math

# Read the Excel file
df = pd.read_excel('a_collection_of_homes_to_represent_the_us_housing_stock.xlsx')

# Add the 2025 reference manually
new_row = {
    'Year': 2025,
    'Title': 'A Collection of Dwellings to Represent the U.S. Housing Stock: 2024 Update',
    'Location': 'NIST Technical Note 2329',
    'Link': 'https://doi.org/10.6028/NIST.TN.2329',
    'Citation': 'Lima, N.M., Persily, A.K., Emmerich, S.J. (2025) A Collection of Dwellings to Represent the U.S. Housing Stock: 2024 Update. (National Institute of Standards and Technology, Gaithersburg, MD), NIST Technical Note (NIST TN) 2329.',
    'Type of Work': 'Report',
    'CONTAM modeled': 'Yes',
    '# of models used': 18,
    'usage category': 'energy/vent',
    'Database useage': '2024 update to the original collection with 18 new CONTAM models representing dwellings built after 2000'
}

# Add the new row to the dataframe
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Clean the data
df['Year'] = df['Year'].fillna(0).astype(int)
df = df[df['Year'] > 0]  # Remove invalid years

# Clean the 'Type of Work' column
df['Type of Work'] = df['Type of Work'].fillna('Unknown')

# Clean the 'usage category' column
df['usage category'] = df['usage category'].str.strip()
df['usage category'] = df['usage category'].fillna('Unknown')

# Clean CONTAM modeled column
df['CONTAM modeled'] = df['CONTAM modeled'].fillna('Unknown')

print(f"Total publications analyzed: {len(df)}")
print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")

# Create output HTML file
output_file("nist_housing_stock_impact.html")

# Color palettes
colors_type = Category20[8]
colors_category = Set3[12]

# 1. Publications over time with cumulative count
years_count = df.groupby('Year').size().reset_index(name='count')
years_count['cumulative'] = years_count['count'].cumsum()

p1 = figure(title="Publications Using NIST Housing Stock Collection Over Time", 
           x_axis_label="Year", y_axis_label="Number of Publications",
           width=800, height=400, toolbar_location="above")

# Bar chart for annual publications
source_yearly = ColumnDataSource(years_count)
bars = p1.vbar(x='Year', top='count', width=0.8, source=source_yearly,
               fill_color='steelblue', fill_alpha=0.7, line_color='navy')

# Line chart for cumulative publications
line = p1.line(x='Year', y='cumulative', source=source_yearly, 
               line_width=3, color='red', legend_label='Cumulative')
circles = p1.circle(x='Year', y='cumulative', source=source_yearly, 
                    size=8, color='red', legend_label='Cumulative')

# Add hover tool
hover1 = HoverTool(renderers=[bars], tooltips=[
    ("Year", "@Year"),
    ("Publications", "@count"),
    ("Cumulative", "@cumulative")
])
p1.add_tools(hover1)

p1.legend.location = "top_left"
p1.legend.click_policy = "hide"

# 2. Publication types breakdown
type_counts = df['Type of Work'].value_counts()
type_data = pd.DataFrame({
    'type': type_counts.index,
    'count': type_counts.values,
    'angle': [2*math.pi*count/type_counts.sum() for count in type_counts.values],
    'color': colors_type[:len(type_counts)]
})
type_data['percentage'] = (type_data['count'] / type_data['count'].sum() * 100).round(1)

p2 = figure(title="Distribution of Publication Types", 
           toolbar_location="above", width=400, height=400,
           x_range=(-1.2, 1.2), y_range=(-1.2, 1.2))

type_source = ColumnDataSource(type_data)
wedges = p2.annular_wedge(x=0, y=0, inner_radius=0.3, outer_radius=0.8,
                         start_angle=cumsum('angle', include_zero=True), 
                         end_angle=cumsum('angle'),
                         line_color="white", fill_color='color', source=type_source)

# Add labels for pie chart
p2.text(x=0.6*np.cos(cumsum(type_data['angle'], include_zero=True)[:-1] + type_data['angle']/2),
        y=0.6*np.sin(cumsum(type_data['angle'], include_zero=True)[:-1] + type_data['angle']/2),
        text=[f"{t}\n({p}%)" for t, p in zip(type_data['type'], type_data['percentage'])],
        text_align="center", text_baseline="middle", text_font_size="9pt")

hover2 = HoverTool(renderers=[wedges], tooltips=[
    ("Type", "@type"),
    ("Count", "@count"),
    ("Percentage", "@percentage%")
])
p2.add_tools(hover2)
p2.axis.visible = False
p2.grid.visible = False

# 3. Usage categories over time
category_year = df.groupby(['Year', 'usage category']).size().unstack(fill_value=0)
category_colors = {cat: colors_category[i] for i, cat in enumerate(category_year.columns)}

p3 = figure(title="Research Categories Over Time",
           x_axis_label="Year", y_axis_label="Number of Publications",
           width=800, height=400, toolbar_location="above")

# Stacked bar chart
bottom = np.zeros(len(category_year))
legend_items = []

for i, category in enumerate(category_year.columns):
    color = category_colors[category]
    bars = p3.vbar(x=category_year.index, top=category_year[category], 
                   bottom=bottom, width=0.8, color=color, alpha=0.8,
                   legend_label=category)
    legend_items.append(LegendItem(label=category, renderers=[bars]))
    bottom += category_year[category].values

p3.legend.location = "top_left"
p3.legend.click_policy = "hide"

# 4. CONTAM usage analysis
contam_counts = df['CONTAM modeled'].value_counts()
contam_data = pd.DataFrame({
    'used': contam_counts.index,
    'count': contam_counts.values,
    'percentage': (contam_counts.values / contam_counts.sum() * 100).round(1)
})

p4 = figure(x_range=contam_data['used'], title="CONTAM Model Usage",
           toolbar_location="above", width=400, height=400)

contam_source = ColumnDataSource(contam_data)
bars4 = p4.vbar(x='used', top='count', width=0.6, source=contam_source,
                color=['green' if x == 'Yes' else 'orange' if x == 'No' else 'gray' 
                       for x in contam_data['used']])

# Add percentage labels on bars
p4.text(x='used', y='count', text=[f"{c}\n({p}%)" for c, p in zip(contam_data['count'], contam_data['percentage'])],
        source=contam_source, text_align="center", text_baseline="bottom", text_font_size="10pt")

hover4 = HoverTool(renderers=[bars4], tooltips=[
    ("CONTAM Used", "@used"),
    ("Count", "@count"),
    ("Percentage", "@percentage%")
])
p4.add_tools(hover4)

p4.y_range.start = 0
p4.xaxis.major_label_orientation = 45

# 5. Research impact summary statistics
total_pubs = len(df)
contam_yes = len(df[df['CONTAM modeled'] == 'Yes'])
years_span = df['Year'].max() - df['Year'].min()
peak_year = df['Year'].value_counts().index[0]
peak_count = df['Year'].value_counts().iloc[0]

# Create a summary statistics plot
summary_stats = [
    f"Total Publications: {total_pubs}",
    f"Years Span: {df['Year'].min()}-{df['Year'].max()} ({years_span} years)",
    f"CONTAM Models Used: {contam_yes} ({(contam_yes/total_pubs*100):.1f}%)",
    f"Peak Year: {peak_year} ({peak_count} publications)",
    f"Most Common Type: {df['Type of Work'].value_counts().index[0]}",
    f"Most Common Category: {df['usage category'].value_counts().index[0]}"
]

p5 = figure(title="NIST IR 7330 Impact Summary", width=800, height=300,
           toolbar_location=None, x_range=(0, 10), y_range=(0, 10))

for i, stat in enumerate(summary_stats):
    p5.text(x=1, y=9-i*1.3, text=[stat], text_font_size="12pt", 
           text_color="darkblue", text_font_style="bold")

p5.axis.visible = False
p5.grid.visible = False

# Create the layout
title_div = Title(text="Research Impact Analysis: NIST Collection of Homes to Represent U.S. Housing Stock (2007-2022)",
                 text_font_size="16pt", text_color="darkblue")

layout = column(
    p5,  # Summary stats at top
    p1,  # Time series
    row(p2, p4),  # Pie charts side by side
    p3   # Stacked bar chart
)

# Add main title
layout.children.insert(0, title_div)

# Show the plot
show(layout)

print("\nVisualization complete! The HTML file 'nist_housing_stock_impact.html' has been generated.")
print("\nKey findings:")
print(f"- The NIST housing stock collection has been cited in {total_pubs} publications from {df['Year'].min()} to {df['Year'].max()}")
print(f"- Peak usage was in {peak_year} with {peak_count} publications")
print(f"- {contam_yes} publications ({(contam_yes/total_pubs*100):.1f}%) used CONTAM modeling")
print(f"- Most publications focus on ventilation research ({df['usage category'].value_counts().iloc[0]} category)")
print(f"- Journal articles are the most common publication type ({df['Type of Work'].value_counts().iloc[0]})")
