# -*- coding: utf-8 -*-
"""
Core LandXML 1.2 TIN Surface Generation Engine for QGIS
Author: Peggy Foster | Terra Hydro Technologies
License: MIT
"""

import math
from datetime import datetime
from qgis.core import QgsProject, QgsUnitTypes

def triangulate_points(points_2d):
    """
    Pure-Python Bowyer-Watson Delaunay Triangulation.
    Zero C-dependencies, runs in any QGIS Python environment out of the box.
    points_2d: list of tuples (x, y, id)
    returns: list of triangles [(p1_id, p2_id, p3_id), ...]
    """
    if len(points_2d) < 3:
        raise ValueError("A minimum of 3 points is required to generate a TIN surface.")

    # 1. Bounding Super-Triangle
    min_x = min(p[0] for p in points_2d)
    max_x = max(p[0] for p in points_2d)
    min_y = min(p[1] for p in points_2d)
    max_y = max(p[1] for p in points_2d)

    dx = (max_x - min_x) * 10
    dy = (max_y - min_y) * 10
    mid_x = (min_x + max_x) / 2.0
    mid_y = (min_y + max_y) / 2.0

    st_p1 = (mid_x - dx, mid_y - dy, -1)
    st_p2 = (mid_x, mid_y + dy, -2)
    st_p3 = (mid_x + dx, mid_y - dy, -3)

    triangles = [(st_p1, st_p2, st_p3)]

    # 2. Incremental Point Insertion
    for p in points_2d:
        bad_triangles = []
        for tri in triangles:
            ax, ay = tri[0][0], tri[0][1]
            bx, by = tri[1][0], tri[1][1]
            cx, cy = tri[2][0], tri[2][1]
            d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
            if abs(d) < 1e-10:
                continue
            ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
            uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
            r = math.hypot(ax - ux, ay - uy)

            # In circumcircle?
            if math.hypot(p[0] - ux, p[1] - uy) <= r:
                bad_triangles.append(tri)

        # 3. Find boundary polygon of bad triangles
        polygon = []
        for tri in bad_triangles:
            edges = [
                (tri[0], tri[1]),
                (tri[1], tri[2]),
                (tri[2], tri[0])
            ]
            for edge in edges:
                is_shared = False
                for other_tri in bad_triangles:
                    if other_tri == tri:
                        continue
                    other_edges = [
                        (other_tri[0], other_tri[1]),
                        (other_tri[1], other_tri[2]),
                        (other_tri[2], other_tri[0])
                    ]
                    for oe in other_edges:
                        if (edge[0] == oe[0] and edge[1] == oe[1]) or (edge[0] == oe[1] and edge[1] == oe[0]):
                            is_shared = True
                            break
                    if is_shared:
                        break
                if not is_shared:
                    polygon.append(edge)

        # 4. Remove bad triangles
        for tri in bad_triangles:
            triangles.remove(tri)

        # 5. Form new triangles with point
        for edge in polygon:
            triangles.append((edge[0], edge[1], p))

    # 6. Remove super-triangle vertices
    final_faces = []
    for tri in triangles:
        if tri[0][2] > 0 and tri[1][2] > 0 and tri[2][2] > 0:
            final_faces.append((tri[0][2], tri[1][2], tri[2][2]))

    return final_faces


def export_point_layer_to_landxml(layer, z_field_name, surface_name, output_path):
    """
    Extracts points from QgsVectorLayer, runs triangulation,
    and writes compliant 3D LandXML 1.2 file for Civil 3D import.
    """
    points = []      # (id, x, y, z)
    points_2d = []   # (x, y, id)
    pt_id = 1

    field_idx = layer.fields().indexOf(z_field_name)

    for feature in layer.getFeatures():
        geom = feature.geometry()
        if geom.isNull():
            continue

        point = geom.asPoint()
        x = point.x()
        y = point.y()

        # Extract elevation from attribute or geometry
        if field_idx != -1:
            val = feature.attribute(field_idx)
            try:
                z = float(val)
            except (ValueError, TypeError):
                continue
        elif geom.isMultipart() or geom.wkbType():
            z = point.z() if hasattr(point, 'z') else 0.0
        else:
            z = 0.0

        points.append((pt_id, x, y, z))
        points_2d.append((x, y, pt_id))
        pt_id += 1

    if len(points) < 3:
        raise ValueError(f"Insufficient valid points found in layer '{layer.name()}' (minimum 3 required).")

    # Run Triangulation
    faces = triangulate_points(points_2d)

    # Detect Project Units (Imperial vs Metric)
    crs = layer.crs()
    is_feet = crs.mapUnits() in [QgsUnitTypes.DistanceFeet, QgsUnitTypes.DistanceStandardFeet, QgsUnitTypes.DistanceUSSurveyFeet]
    linear_unit = "foot" if is_feet else "meter"

    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # Serialize LandXML 1.2
    xml_lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<LandXML xmlns="http://www.landxml.org/schema/LandXML-1.2"',
        '         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '         xsi:schemaLocation="http://www.landxml.org/schema/LandXML-1.2 http://www.landxml.org/schema/LandXML-1.2/LandXML-1.2.xsd"',
        f'         version="1.2" date="{timestamp}" time="{timestamp}">',
        f'  <Units>',
        f'    <Imperial linearUnit="{linear_unit}" areaUnit="squareFoot" volumeUnit="cubicYard" temperatureUnit="fahrenheit" pressureUnit="inHG"/>' if is_feet else
        f'    <Metric linearUnit="{linear_unit}" areaUnit="squareMeter" volumeUnit="cubicMeter" temperatureUnit="celsius" pressureUnit="HPA"/>',
        f'  </Units>',
        f'  <Application name="Subgrade LandXML Bridge (QGIS)" manufacturer="Terra Hydro Technologies" version="1.0.0" timeStamp="{timestamp}">',
        f'    <Author createdBy="Peggy Foster" company="Terra Hydro Technologies" companyURL="https://terrahydrotechnologies.com"/>',
        f'  </Application>',
        f'  <Surfaces>',
        f'    <Surface name="{surface_name}">',
        f'      <Definition surfType="TIN">',
        f'        <Pnts>'
    ]

    # LandXML coordinates are Northing(Y) Easting(X) Elevation(Z)
    for p in points:
        xml_lines.append(f'          <P id="{p[0]}">{p[2]:.4f} {p[1]:.4f} {p[3]:.4f}</P>')

    xml_lines.append('        </Pnts>')
    xml_lines.append('        <Faces>')

    for f in faces:
        xml_lines.append(f'          <F>{f[0]} {f[1]} {f[2]}</F>')

    xml_lines.append('        </Faces>')
    xml_lines.append('      </Definition>')
    xml_lines.append('    </Surface>')
    xml_lines.append('  </Surfaces>')
    xml_lines.append('</LandXML>')

    # Write File
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write('\n'.join(xml_lines))

    return len(points), len(faces)
