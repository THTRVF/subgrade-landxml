# -*- coding: utf-8 -*-
"""
Dialog Interface for Subgrade LandXML Bridge
Author: Peggy Foster | Terra Hydro Technologies
"""

import os
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGroupBox, QFileDialog, QMessageBox, QLineEdit
)
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox
from qgis.core import QgsMapLayerProxyModel

class SubgradeLandXMLDialog(QDialog):
    def __init__(self, parent=None):
        super(SubgradeLandXMLDialog, self).__init__(parent)
        self.setWindowTitle("Subgrade LandXML Bridge — Terra Hydro Technologies")
        self.setMinimumWidth(480)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header Banner
        header = QLabel("<h3>Subgrade LandXML 1.2 Surface Generator</h3>"
                        "<p style='color: #64748b; font-size: 11px;'>"
                        "Terra Hydro Technologies &bull; Open Standards CAD Bridge</p>")
        layout.addWidget(header)

        # Group 1: Layer & Attribute Selection
        grp_input = QGroupBox("Geotechnical Point Source")
        layout_input = QVBoxLayout()

        layout_input.addWidget(QLabel("Select Point Layer (Boreholes / Piezometers):"))
        self.layer_combo = QgsMapLayerComboBox()
        self.layer_combo.setFilters(QgsMapLayerProxyModel.PointLayer)
        layout_input.addWidget(self.layer_combo)

        layout_input.addWidget(QLabel("Select Surface Elevation Field (Z / Piezometric Head):"))
        self.field_combo = QgsFieldComboBox()
        self.layer_combo.layerChanged.connect(self.field_combo.setLayer)
        if self.layer_combo.currentLayer():
            self.field_combo.setLayer(self.layer_combo.currentLayer())
        layout_input.addWidget(self.field_combo)

        grp_input.setLayout(layout_input)
        layout.addWidget(grp_input)

        # Group 2: Surface Naming & Output Destination
        grp_output = QGroupBox("Export Configuration")
        layout_output = QVBoxLayout()

        layout_output.addWidget(QLabel("Surface Name (as it appears in Civil 3D Prospector):"))
        self.txt_surface_name = QLineEdit("EG_GROUNDWATER_TIN")
        layout_output.addWidget(self.txt_surface_name)

        layout_output.addWidget(QLabel("Output LandXML 1.2 Destination File:"))
        h_file = QHBoxLayout()
        self.txt_out_path = QLineEdit()
        self.txt_out_path.setPlaceholderText("Select destination path (*.xml)...")
        btn_browse = QPushButton("Browse...")
        btn_browse.clicked.connect(self.browse_destination)
        h_file.addWidget(self.txt_out_path)
        h_file.addWidget(btn_browse)
        layout_output.addLayout(h_file)

        grp_output.setLayout(layout_output)
        layout.addWidget(grp_output)

        # Action Buttons
        h_actions = QHBoxLayout()
        self.btn_export = QPushButton("Generate LandXML 1.2 Surface")
        self.btn_export.setStyleSheet("background-color: #d9531e; color: white; font-weight: bold; padding: 8px;")
        self.btn_export.clicked.connect(self.accept)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)

        h_actions.addWidget(self.btn_cancel)
        h_actions.addWidget(self.btn_export)
        layout.addLayout(h_actions)

        # Footer Notice
        footer = QLabel("<p style='color: #94a3b8; font-size: 10px; text-align: center; margin-top: 10px;'>"
                        "Universal CAD Interoperability &bull; terrahydrotechnologies.com</p>")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.setLayout(layout)

    def browse_destination(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save LandXML Surface", "", "LandXML Files (*.xml);;All Files (*)"
        )
        if file_path:
            if not file_path.lower().endswith(".xml"):
                file_path += ".xml"
            self.txt_out_path.setText(file_path)

    def get_parameters(self):
        return {
            "layer": self.layer_combo.currentLayer(),
            "field": self.field_combo.currentField(),
            "surface_name": self.txt_surface_name.text().strip() or "GROUNDWATER_TIN",
            "output_path": self.txt_out_path.text().strip()
        }
