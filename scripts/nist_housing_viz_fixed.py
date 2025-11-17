#%%
#NOTE: the files have moved and the file location will needed to be updated if you are running this code.

#%%
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource, LegendItem, LinearAxis, Range1d
from bokeh.layouts import column, row
from bokeh.transform import cumsum
import math

# Read the Excel file
df = pd.read_excel('a_collection_of_homes_to_represent_the_us_housing_stock.xlsx')

# Clean the data (no need to add 2025 reference since that's this project)
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

# ASHRAE-themed color palettes - poster ready
ashrae_colors_main = ['#1f4e79', '#2e75b6', '#5b9bd5', '#8db4e2', '#c5d9f1', '#ddeaf6']
ashrae_colors_type = ['#1f4e79', '#2e75b6', '#5b9bd5', '#8db4e2', '#c5d9f1', '#ddeaf6', '#4472c4', '#70ad47']
ashrae_colors_category = ['#1f4e79', '#2e75b6', '#5b9bd5', '#70ad47', '#ffc000', '#c55a5a', '#4472c4', '#8db4e2', '#c5d9f1', '#ddeaf6', '#548235', '#bf8f00']

# Calculate yearly data for cumulative line
years_count = df.groupby('Year').size().reset_index(name='count')
years_count['cumulative'] = years_count['count'].cumsum()

# 1. Publication types breakdown - LARGER for poster with FIXED text positioning
type_counts = df['Type of Work'].value_counts()
type_data = pd.DataFrame({
    'type': type_counts.index,
    'count': type_counts.values,
    'angle': [2*math.pi*count/type_counts.sum() for count in type_counts.values],
    'color': ashrae_colors_type[:len(type_counts)]
})
type_data['percentage'] = (type_data['count'] / type_data['count'].sum() * 100).round(1)

p1 = figure(title="Distribution of Publication Types", 
           toolbar_location="above", width=700, height=700,  # Made larger to accommodate labels
           x_range=(-2, 2), y_range=(-2, 2))  # Expanded range for labels

# Make title larger for poster
p1.title.text_font_size = "28pt"
p1.title.text_color = "#1f4e79"

type_source = ColumnDataSource(type_data)
wedges = p1.annular_wedge(x=0, y=0, inner_radius=0.3, outer_radius=0.8,  # Smaller pie to make room for labels
                         start_angle=cumsum('angle', include_zero=True), 
                         end_angle=cumsum('angle'),
                         line_color="white", line_width=3, fill_color='color', source=type_source)

# FIXED: Better text positioning with smart placement to avoid overlap
angles_cumsum = np.concatenate([[0], np.cumsum(type_data['angle'])])
label_angles = angles_cumsum[:-1] + type_data['angle']/2

# Smarter label positioning - place labels at varying distances to avoid overlap
label_distances = []
for i, angle in enumerate(label_angles):
    # Alternate between closer and farther labels to reduce overlap
    base_distance = 1.1
    if i % 2 == 0:
        distance = base_distance
    else:
        distance = base_distance + 0.2
    label_distances.append(distance)

# Position labels with better spacing
for i, (angle, distance, type_name, percentage) in enumerate(zip(label_angles, label_distances, type_data['type'], type_data['percentage'])):
    # Shorten long labels to prevent overlap
    if len(type_name) > 12:
        display_name = type_name[:10] + "..."
    else:
        display_name = type_name
    
    p1.text(x=distance*np.cos(angle),
            y=distance*np.sin(angle),
            text=[f"{display_name}\n({percentage}%)"],
            text_align="center", text_baseline="middle", 
            text_font_size="18pt", text_color="black")  # FIXED: Back to black text

hover1 = HoverTool(renderers=[wedges], tooltips=[
    ("Type", "@type"),
    ("Count", "@count"),
    ("Percentage", "@percentage%")
])
p1.add_tools(hover1)
p1.axis.visible = False
p1.grid.visible = False

# 2. Research categories over time with cumulative line - FIXED Y-axis scaling
category_year = df.groupby(['Year', 'usage category']).size().unstack(fill_value=0)
category_colors = {cat: ashrae_colors_category[i % len(ashrae_colors_category)] for i, cat in enumerate(category_year.columns)}

p2 = figure(title="Research Categories Over Time",
           x_axis_label="Year", y_axis_label="Number of Publications",
           width=1200, height=600, toolbar_location="above")

# FIXED: Set explicit Y-axis range for the stacked bars (left axis)
max_stacked_height = category_year.sum(axis=1).max()
p2.y_range = Range1d(start=0, end=max_stacked_height * 1.1)  # Set left axis to appropriate range

# Make all text larger for poster but keep axis labels black
p2.title.text_font_size = "28pt"
p2.title.text_color = "#1f4e79"
p2.xaxis.axis_label_text_font_size = "24pt"
p2.yaxis.axis_label_text_font_size = "24pt"
p2.xaxis.major_label_text_font_size = "20pt"
p2.yaxis.major_label_text_font_size = "20pt"
# FIXED: Keep axis labels black (remove color overrides)

# Stacked bar chart
bottom = np.zeros(len(category_year))
legend_items = []

for i, category in enumerate(category_year.columns):
    color = category_colors[category]
    bars = p2.vbar(x=category_year.index, top=category_year[category], 
                   bottom=bottom, width=0.8, color=color, alpha=0.8,
                   legend_label=category)
    legend_items.append(LegendItem(label=category, renderers=[bars]))
    bottom += category_year[category].values

# Add cumulative line with right Y-axis
# Create cumulative data aligned with category_year index
cumulative_by_year = years_count.set_index('Year').reindex(category_year.index, fill_value=0)['cumulative']

# Set up extra y range for cumulative line
p2.extra_y_ranges = {"cumulative": Range1d(start=0, end=cumulative_by_year.max()*1.1)}

# Add cumulative line
line = p2.line(x=category_year.index, y=cumulative_by_year.values, 
               line_width=6, color='#c55a5a', y_range_name="cumulative")
circles = p2.scatter(x=category_year.index, y=cumulative_by_year.values, 
                    size=12, color='#c55a5a', y_range_name="cumulative")

# Add second y-axis for cumulative
p2.add_layout(LinearAxis(y_range_name="cumulative", axis_label="Cumulative Publications",
                        axis_label_text_font_size="24pt", major_label_text_font_size="20pt"), 'right')

p2.legend.location = "top_left"
p2.legend.click_policy = "hide"
p2.legend.label_text_font_size = "20pt"

# 3. CONTAM usage analysis - LARGER for poster and fix Y-axis
contam_counts = df['CONTAM modeled'].value_counts()
contam_data = pd.DataFrame({
    'used': contam_counts.index,
    'count': contam_counts.values,
    'percentage': (contam_counts.values / contam_counts.sum() * 100).round(1)
})

# Add color column and text labels to the dataframe
contam_data['color'] = ['#70ad47' if x == 'Yes' else '#ffc000' if x == 'No' else '#5b9bd5' for x in contam_data['used']]
contam_data['labels'] = [f"{c}\n({p}%)" for c, p in zip(contam_data['count'], contam_data['percentage'])]

p3 = figure(x_range=contam_data['used'], title="CONTAM Model Usage",
           toolbar_location="above", width=600, height=600)

# Make all text larger for poster
p3.title.text_font_size = "28pt"
p3.title.text_color = "#1f4e79"
p3.xaxis.major_label_text_font_size = "24pt"
p3.yaxis.major_label_text_font_size = "20pt"
p3.yaxis.axis_label_text_font_size = "24pt"

contam_source = ColumnDataSource(contam_data)
bars3 = p3.vbar(x='used', top='count', width=0.6, source=contam_source,
                color='color')

# Add percentage labels on bars - now referencing the labels column
p3.text(x='used', y='count', text='labels', source=contam_source, 
        text_align="center", text_baseline="bottom", text_font_size="24pt", text_color="black")

hover3 = HoverTool(renderers=[bars3], tooltips=[
    ("CONTAM Used", "@used"),
    ("Count", "@count"),
    ("Percentage", "@percentage%")
])
p3.add_tools(hover3)

# Fix Y-axis range to accommodate text labels
max_count = contam_data['count'].max()
p3.y_range.start = 0
p3.y_range.end = max_count * 1.3  # Add 30% space for labels

p3.xaxis.major_label_orientation = 45

# 4. Research impact summary statistics - LARGER for poster
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

p4 = figure(width=1200, height=400, toolbar_location=None, x_range=(0, 10), y_range=(0, 10))

# Make title and text much larger for poster
p4.title.text = "NIST IR 7330 Impact Summary - Presented at ASHRAE IAQ 2025 Conference"
p4.title.text_font_size = "32pt"
p4.title.text_color = "#1f4e79"

for i, stat in enumerate(summary_stats):
    p4.text(x=1, y=8.5-i*1.2, text=[stat], text_font_size="28pt", 
           text_color="#1f4e79", text_font_style="bold")

p4.axis.visible = False
p4.grid.visible = False

# Create the layout - poster ready
layout = column(
    p4,  # Summary stats at top
    p2,  # Research categories over time with cumulative line
    row(p1, p3),  # Pie chart and CONTAM usage side by side
)

# Show the plot
show(layout)

print("\nPoster-ready visualization complete! The HTML file 'nist_housing_stock_impact.html' has been generated.")
print("Optimized for ASHRAE IAQ 2025 Conference poster presentation.")
print("\nKey findings:")
print(f"- The NIST housing stock collection has been cited in {total_pubs} publications from {df['Year'].min()} to {df['Year'].max()}")
print(f"- Peak usage was in {peak_year} with {peak_count} publications")
print(f"- {contam_yes} publications ({(contam_yes/total_pubs*100):.1f}%) used CONTAM modeling")
print(f"- Most publications focus on {df['usage category'].value_counts().index[0]} research")
print(f"- {df['Type of Work'].value_counts().index[0]} are the most common publication ty")