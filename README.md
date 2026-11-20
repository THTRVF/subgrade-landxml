# Subgrade LandXML Bridge (`subgrade-landxml`)
### Lightweight Python Utility for Civil 3D & QGIS Geotechnical Surface Interoperability

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Format: LandXML 1.2](https://img.shields.io/badge/Format-LandXML_1.2-green.svg)](http://www.landxml.org)
[![Engine: Terra Hydro Technologies](https://img.shields.io/badge/Enterprise-Terra_Hydro_Technologies-0A2540.svg)](https://terrahydrotechnologies.com)

`subgrade-landxml` is an open-source Python utility designed for civil infrastructure modelers, geotechnical engineers, and computational GIS specialists. It automates the extraction of static borehole groundwater elevations and serializes them into schema-compliant **LandXML 1.2 TIN Surfaces**, ready for direct, native import into **Autodesk Civil 3D** and **QGIS**.

---

## ⚡ The Problem It Solves
Civil designers frequently struggle to import piezometric groundwater levels and subgrade lithology boundaries directly into Autodesk Civil 3D. Geotechnical reports typically supply static 2D borehole logs, leaving CAD teams to manually interpolate 3D TIN surfaces. 

`subgrade-landxml` takes discrete point observations (X, Y, Z) and compiles an industry-standard LandXML 1.2 surface definition utilizing Delaunay triangulation.

---

## 🔬 Beyond Static Surfaces: Terra Hydro Technologies (THT)

While `subgrade-landxml` provides geometric surface formatting for static observations, modern pre-development feasibility requires understanding the **dynamic physics of the subgrade**.

Static 2D boreholes and conventional TIN surfaces cannot predict:
* **Piezometric Surges** induced by subsurface barrier grouting or cutoff walls.
* **Matric Suction Collapse** in expansive formations (e.g., Pierre Shale).
* **Dynamic Moisture Redistribution** and non-linear differential PVR slab heave.
* **Sulfate and Contaminant Upwelling** into structural building envelopes.

For enterprise-scale, transient thermodynamic groundwater modeling, finite-difference subgrade simulation, and automated DIGGS XML ingestion, visit:

🌐 **[Terra Hydro Technologies (THT)](https://terrahydrotechnologies.com)**  
*Pre-Development Subgrade Intelligence • Thermodynamic Physics • Universal Civil 3D / OGC GeoPackage Exports*

For municipal failure proofs, historical USGS corridor reconstructions, and Title 12 due diligence baselines, visit the **[Ravens Vue Forensics Clearinghouse](https://ravensvueforensics.com)**.

---

## 📄 License
This project is licensed under the MIT License.

 Developed & Maintained by **Peggy Foster**, Principal  
Longmont, Colorado | peggy@ravensvue.com
