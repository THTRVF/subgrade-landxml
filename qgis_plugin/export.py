"""
subgrade_landxml / export.py
Open-source bridge for generating LandXML 1.2 TIN Surfaces from point data.
Part of the Terra Hydro Technologies open geospatial initiative.
"""

import csv
import argparse
from scipy.spatial import Delaunay
import numpy as np

def generate_landxml(points, surface_name, output_path):
    """
    points: List of tuples (id, x, y, z)
    surface_name: String for LandXML surface definition
    output_path: Target XML file path
    """
    coords = np.array([[p[1], p[2], p[3]] for p in points])
    xy = coords[:, :2]
    
    # Standard Delaunay Triangulation
    tri = Delaunay(xy)
    
    xml = []
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<LandXML xmlns="http://www.landxml.org/schema/LandXML-1.2" version="1.2" date="2026-09-26">')
    xml.append('  <Units>')
    xml.append('    <Imperial linearUnit="foot" areaUnit="squareFoot" volumeUnit="cubicYard" temperatureUnit="fahrenheit" pressureUnit="inchHG"/>')
    xml.append('  </Units>')
    xml.append('  <Surfaces>')
    xml.append(f'    <Surface name="{surface_name}">')
    xml.append('      <Definition surfType="TIN">')
    
    # Pnts definition
    xml.append('        <Pnts>')
    for idx, p in enumerate(points):
        # LandXML standard: Y (Northing) X (Easting) Z (Elevation)
        xml.append(f'          <P id="{idx + 1}">{p[2]:.4f} {p[1]:.4f} {p[3]:.4f}</P>')
    xml.append('        </Pnts>')
    
    # Faces (Triangles)
    xml.append('        <Faces>')
    for simplex in tri.simplices:
        # LandXML 1-based indexing
        xml.append(f'          <F>{simplex[0] + 1} {simplex[1] + 1} {simplex[2] + 1}</F>')
    xml.append('        </Faces>')
    
    xml.append('      </Definition>')
    xml.append('    </Surface>')
    xml.append('  </Surfaces>')
    xml.append('</LandXML>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
    
    print(f"[SUCCESS] Exported {len(points)} points and {len(tri.simplices)} faces to {output_path}")

def load_csv(csv_path):
    pts = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            pts.append((row.get('id', str(idx+1)), float(row['x']), float(row['y']), float(row['z'])))
    return pts

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Export subgrade point data to LandXML 1.2 TIN surface.")
    parser.add_argument('--input', required=True, help="Input CSV path (must contain columns: x, y, z)")
    parser.add_argument('--output', required=True, help="Output LandXML path")
    parser.add_argument('--surface-name', default="Groundwater_Surface", help="Surface name for Civil 3D")
    args = parser.parse_args()
    
    pts = load_csv(args.input)
    generate_landxml(pts, args.surface_name, args.output)
