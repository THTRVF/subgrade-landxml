# -*- coding: utf-8 -*-
"""
Subgrade LandXML Bridge - QGIS Plugin
Author: Peggy Foster | Terra Hydro Technologies
License: MIT
"""

def classFactory(iface):
    """Load SubgradeLandXMLPlugin class from file plugin.py."""
    from .plugin import SubgradeLandXMLPlugin
    return SubgradeLandXMLPlugin(iface)
