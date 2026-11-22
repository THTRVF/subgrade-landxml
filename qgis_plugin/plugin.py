# -*- coding: utf-8 -*-
"""
Main Plugin Class for Subgrade LandXML Bridge
Author: Peggy Foster | Terra Hydro Technologies
License: MIT
"""

import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import Qgis
from .dialog import SubgradeLandXMLDialog
from .export_core import export_point_layer_to_landxml

class SubgradeLandXMLPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None

    def initGui(self):
        """Create the menu items and toolbar buttons."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        if not os.path.exists(icon_path):
            icon = QIcon()  # Default fallback icon if image isn't loaded yet
        else:
            icon = QIcon(icon_path)

        self.action = QAction(icon, "Subgrade LandXML Bridge", self.iface.mainWindow())
        self.action.setStatusTip("Compile borehole/piezometer points into 3D LandXML 1.2 surfaces")
        self.action.triggered.connect(self.run)

        # Add to Vector menu and Plugin toolbar
        self.iface.addPluginToVectorMenu("&Terra Hydro Technologies", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        """Remove plugin menu and toolbar on disable."""
        self.iface.removePluginVectorMenu("&Terra Hydro Technologies", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        """Execute the dialog and process surface export."""
        dialog = SubgradeLandXMLDialog(self.iface.mainWindow())
        if dialog.exec_():
            params = dialog.get_parameters()
            layer = params['layer']
            field = params['field']
            surface_name = params['surface_name']
            output_path = params['output_path']

            if not layer:
                self.iface.messageBar().pushMessage(
                    "Error", "Please select a valid point layer.", level=Qgis.Warning
                )
                return

            if not output_path:
                self.iface.messageBar().pushMessage(
                    "Error", "Please specify an output file destination.", level=Qgis.Warning
                )
                return

            try:
                pts_count, faces_count = export_point_layer_to_landxml(
                    layer, field, surface_name, output_path
                )
                self.iface.messageBar().pushMessage(
                    "LandXML 1.2 Surface Created",
                    f"Successfully compiled {pts_count} points and {faces_count} TIN faces into '{surface_name}'. Exported to {output_path}",
                    level=Qgis.Success,
                    duration=6
                )
            except Exception as e:
                self.iface.messageBar().pushMessage(
                    "Export Error", str(e), level=Qgis.Critical, duration=10
                )
