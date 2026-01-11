# VTK-to-DXF
Example of converting VTK to DXF with python

## Tools
- PyVista
- PyMeshLab

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command-Line Script

The repository includes a user-friendly command-line script `vtk_to_dxf.py` that makes it easy to convert STL files to DXF format.

#### Convert a single file:
```bash
python vtk_to_dxf.py input.stl
```

#### Convert all STL files in a directory:
```bash
python vtk_to_dxf.py /path/to/stl/directory/
```

#### Convert with custom output directory:
```bash
python vtk_to_dxf.py /path/to/stl/directory/ --output /path/to/output/
```

#### Convert without recursing into subdirectories:
```bash
python vtk_to_dxf.py /path/to/stl/directory/ --no-recursive
```

#### Show help:
```bash
python vtk_to_dxf.py --help
```

### Jupyter Notebook

For interactive exploration and development, see the `VTK-to-DXF.ipynb` notebook which demonstrates the conversion process step by step.

