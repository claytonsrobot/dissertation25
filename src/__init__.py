# src/__init__.py
"""
SOCEM Package
=============

The SOCEM (Sensor Operated Crop Evaluation Module) package is designed for use with the AgMEQ lab's research device onboard a Raspberry Pi. The device rolls through wheat crop plots, collecting force sensor data to determine flexural rigidity (EI). Flexural rigidity is calculated as Young's modulus multiplied by the mass moment of inertia, derived from crop density data.

The Python software powering SOCEM includes:
- A tkinter-based user interface for data entry.
- Controls to start and stop sampling processes.
- Real-time monitoring of force sensor readings.

The software ensures precise height calibration for accurate sensor contact, vital for the integrity of the research results. This tool aids in advancing agricultural research and crop analysis.

Module Features:
- Force sensor data collection.
- Flexural rigidity (EI) computation from physical and density data.
- User-friendly interface for input and sampling control.

For AgMEQ lab use, the SOCEM package provides a bridge between hardware and scientific analysis, enabling streamlined data collection and computation.
"""
__doc__ = """
SOCEM Package: Data Collection and Analysis Tool for Flexural Rigidity in Wheat

The SOCEM package powers the Raspberry Pi-based device used by the AgMEQ lab to collect force sensor data from wheat plots. It calculates flexural rigidity (EI) as Young's modulus multiplied by the mass moment of inertia, derived from density data. 

Key features include:
- A tkinter-based user interface for data entry and sampling control.
- Real-time force sensor monitoring.
- Support for precise height calibration, critical for accurate results.

This package bridges data collection and analysis, enabling research into crop flexibility and structural properties, with an emphasis on agricultural applications.
""" 