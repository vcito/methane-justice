import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os

os.chdir(os.path.expanduser('~/methane-justice'))

# Load merged data
merged = pd.read_csv('data/emissions-gain-vulnerability-merged.csv')

# Country coordinates (centroids)
country_coords = {
    'China': (35.8617, 104.1954),
    'India': (20.5937, 78.9629),
    'United States': (37.0902, -95.7129),
    'Brazil': (-14.2350, -51.9253),
    'Russian Federation': (61.5240, 105.3188),
    'Indonesia': (-0.7893, 113.9213),
    'Pakistan': (30.3753, 69.3451),
    'Nigeria': (9.0820, 8.6753),
    'Iran, Islamic Republic of': (32.4279, 53.6880),
    'Mexico': (23.6345, -102.5528),
    'Iraq': (33.2232, 43.6793),
    'Bangladesh': (23.6850, 90.3563),
    'Argentina': (-38.4161, -63.6167),
    'Australia': (-25.2744, 133.7751),
    'Thailand': (15.8700, 100.9925),
    'Viet Nam': (14.0583, 108.2772),
    'Canada': (56.1304, -106.3468),
    'Saudi Arabia': (23.8859, 45.0792),
    'Turkey': (38.9637, 35.2433),
    'Ethiopia': (9.1450, 40.4897),
}

# Create base map
m = folium.Map(location=[20, 0], zoom_start=2, tiles='OpenStreetMap')

# Add circles for each country
for idx, row in merged.iterrows():
    country = row['Country']
    
    if country not in country_coords:
        continue
    
    lat, lon = country_coords[country]
    emissions = row['CH4_emissions_Gg_2018']
    vulnerability = row['GAIN_Vulnerability_2018']
    
    # Circle size = emissions (log scale so small emitters visible)
    radius = max(10, min(40, 10 + 5 * pd.np.log10(max(1, emissions))))
    
    # Color = vulnerability (red = vulnerable, green = not vulnerable)
    if pd.isna(vulnerability):
        color = 'gray'
    elif vulnerability > 60:
        color = 'red'
    elif vulnerability > 50:
        color = 'orange'
    elif vulnerability > 40:
        color = 'yellow'
    else:
        color = 'green'
    
    # Popup with info
    popup_text = f"""
    <b>{country}</b><br>
    Emissions: {emissions:,.0f} Gg CH4/year<br>
    Vulnerability: {vulnerability:.1f}/100<br>
    <br>
    <i>Circle size = emissions (log scale)<br>
    Circle color = vulnerability</i>
    """
    
    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        popup=folium.Popup(popup_text, max_width=250),
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.7,
        weight=2,
        opacity=0.9
    ).add_to(m)

# Add legend
legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; width: 320px; 
background-color: white; border:2px solid grey; z-index:9999; 
font-size:12px; padding:15px; border-radius:5px; line-height: 1.5;">

<b style="font-size: 14px;">Climate Justice Map</b><br>
<b>Methane Emissions vs Climate Vulnerability</b><br>
<br>

<b>Circle Size = Emissions (log scale)</b><br>
Bigger circles = more methane emitted<br>
<br>

<b>Circle Color = Vulnerability</b><br>
<span style="color:red;">●</span> Red (>60) = Highly vulnerable<br>
<span style="color:orange;">●</span> Orange (50-60) = Very vulnerable<br>
<span style="color:yellow;">●</span> Yellow (40-50) = Moderately vulnerable<br>
<span style="color:green;">●</span> Green (<40) = Low vulnerability<br>
<br>

<b>The Story:</b><br>
🔴 <b>RED + BIG</b> = Victims (high emissions nearby, vulnerable)<br>
🟢 <b>GREEN + BIG</b> = Free Riders (high emissions, safe)<br>
<br>

<i>Hover over circles for details</i>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

# Save map
m.save('outputs/climate-justice-interactive-map.html')
print("✓ Saved: outputs/climate-justice-interactive-map.html")
print("\nOpen this file in your browser to explore the map interactively!")