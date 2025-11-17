#%%
import numpy as np
from math import pi, cos, sin
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import LabelSet, ColumnDataSource, Legend, LegendItem
import textwrap

output_notebook()

# Define the text wrapping function
def textwrap_label(text, width):
    """Wrap text to a specified width."""
    return textwrap.fill(text, width)

# Define the data for each layer
layer_1_data = {
    'Category': ['Ventilation/IAQ', 'Energy', 'Fire/Other'],
    'Value': [55, 16, 3],  # Sum of values in layer 2 for each category
}

layer_2_data = {
    'Category': ['Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ', 
                 'Energy', 'Energy', 'Energy', 'Energy', 'Energy',
                 'Fire/Other', 'Fire/Other'],
    'Subcategory': ['Journal Article', 'Conference Paper', 'Dissertation', 'Report', 'Unknown', 'Book Section', 'Master Thesis', 
                    'Journal Article', 'Conference Paper', 'Dissertation', 'Report', 'Unknown', 
                    'Journal Article', 'Conference Paper'],
    'Value': [26, 14, 5, 4, 3, 2, 1, 6, 4, 3, 2, 1, 2, 1],
}

layer_3_data = {
    'Category': ['Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ', 'Ventilation/IAQ',
                 'Energy', 'Energy', 'Energy', 'Energy', 'Energy',
                 'Fire/Other', 'Fire/Other'],
    'Subcategory': ['209/33', '140/26', '4/1', '37/19', 'na/na', 'na/na', '0/0',
                    '209/26', '1/0', '0/0', '0/0', 'na/na',
                    '17/9', '17/17'],
    'Value': [26, 14, 5, 4, 3, 2, 1, 6, 4, 3, 2, 1, 2, 1],
}

# Calculate angles for each layer
def calculate_angles(data):
    total_value = sum(data['Value'])
    return [value / total_value * 2 * pi for value in data['Value']]

layer_1_data['Angle'] = calculate_angles(layer_1_data)
layer_2_data['Angle'] = calculate_angles(layer_2_data)
layer_3_data['Angle'] = calculate_angles(layer_3_data)

# Cumulative sums for angles
def cumulative_sums(angles):
    return np.cumsum([0] + angles[:-1])

layer_1_data['Cumsum'] = cumulative_sums(layer_1_data['Angle'])
layer_2_data['Cumsum'] = cumulative_sums(layer_2_data['Angle'])
layer_3_data['Cumsum'] = cumulative_sums(layer_3_data['Angle'])

# Color map for categories
color_map = {
    'Ventilation/IAQ': '#1f77b4',
    'Energy': '#ff7f0e',
    'Fire/Other': '#7f7f7f'
}

# Create Bokeh figure
p = figure(height=600, width=600, title="NIST Collection of Dwelling Citation / Usage",
           x_range=(-1.5, 1.5), y_range=(-1.5, 1.5), tools="hover", toolbar_location=None)

# Hide grid and axes
p.grid.visible = False
p.axis.visible = False

# Draw Layer 1 (Categories)
layer_1_wedges = p.annular_wedge(x=0, y=0, inner_radius=0.3, outer_radius=0.6,
                start_angle=layer_1_data['Cumsum'], end_angle=layer_1_data['Cumsum'] + layer_1_data['Angle'],
                color=[color_map[cat] for cat in layer_1_data['Category']], line_color="white")

# Draw Layer 2 (Subcategories)
colors_layer_2 = [color_map[cat] for cat in layer_2_data['Category']]
layer_2_wedges = p.annular_wedge(x=0, y=0, inner_radius=0.6, outer_radius=0.9,
                start_angle=layer_2_data['Cumsum'], end_angle=layer_2_data['Cumsum'] + layer_2_data['Angle'],
                color=colors_layer_2, direction="anticlock", line_color="white")

# Draw Layer 3 (Detailed Breakdown)
colors_layer_3 = [color_map[cat] for cat in layer_3_data['Category']]
layer_3_wedges = p.annular_wedge(x=0, y=0, inner_radius=0.9, outer_radius=1.2,
                start_angle=layer_3_data['Cumsum'], end_angle=layer_3_data['Cumsum'] + layer_3_data['Angle'],
                color=colors_layer_3, direction="anticlock", line_color="white")

# Function to calculate label positions and rotation angles
def calculate_label_positions_angles(data, radius):
    return {
        'x': [radius * cos((start + end) / 2) for start, end in zip(data['Cumsum'], np.array(data['Cumsum']) + np.array(data['Angle']))],
        'y': [radius * sin((start + end) / 2) for start, end in zip(data['Cumsum'], np.array(data['Cumsum']) + np.array(data['Angle']))],
        'angle': [(start + end) / 2 for start, end in zip(data['Cumsum'], np.array(data['Cumsum']) + np.array(data['Angle']))]
    }

# Add labels for Layer 1
positions_angles_layer_1 = calculate_label_positions_angles(layer_1_data, 0.45)
labels_layer_1 = ColumnDataSource(data=dict(
    x=positions_angles_layer_1['x'],
    y=positions_angles_layer_1['y'],
    labels=[textwrap_label(cat, 10) for cat in layer_1_data['Category']],
    angle=positions_angles_layer_1['angle']
))
p.add_layout(LabelSet(x='x', y='y', text='labels', source=labels_layer_1, text_align='center', text_baseline='middle',
                      text_font_size='10pt', text_font='Calibri',
                      angle={'field': 'angle', 'units': 'rad'}))

# Add labels for Layer 2
positions_angles_layer_2 = calculate_label_positions_angles(layer_2_data, 0.75)
labels_layer_2 = ColumnDataSource(data=dict(
    x=positions_angles_layer_2['x'],
    y=positions_angles_layer_2['y'],
    labels=[textwrap_label(text, 10) for text in layer_2_data['Subcategory']],
    angle=positions_angles_layer_2['angle']
))
p.add_layout(LabelSet(x='x', y='y', text='labels', source=labels_layer_2, text_align='center', text_baseline='middle',
                      text_font_size='10pt', text_font='Calibri',
                      angle={'field': 'angle', 'units': 'rad'}))

# Add labels for Layer 3
positions_angles_layer_3 = calculate_label_positions_angles(layer_3_data, 1.05)
labels_layer_3 = ColumnDataSource(data=dict(
    x=positions_angles_layer_3['x'],
    y=positions_angles_layer_3['y'],
    labels=[textwrap_label(text, 10) for text in layer_3_data['Subcategory']],
    angle=positions_angles_layer_3['angle']
))
p.add_layout(LabelSet(x='x', y='y', text='labels', source=labels_layer_3, text_align='center', text_baseline='middle',
                      text_font_size='10pt', text_font='Calibri',
                      angle={'field': 'angle', 'units': 'rad'}))

# Add legend for Layer 1
legend_items = [LegendItem(label=cat, renderers=[layer_1_wedges], index=i) for i, cat in enumerate(layer_1_data['Category'])]
legend = Legend(items=legend_items, location='center')
p.add_layout(legend, 'above')

show(p)

# %%
