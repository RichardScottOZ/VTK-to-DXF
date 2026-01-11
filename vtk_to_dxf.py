#!/usr/bin/env python3
"""
VTK to DXF Converter

This script converts STL files to DXF format using PyMeshLab.
It can process a single file or all STL files in a directory.

Example usage:
    python vtk_to_dxf.py input.stl
    python vtk_to_dxf.py /path/to/directory/
    python vtk_to_dxf.py /path/to/directory/ --output /output/path/
"""

import argparse
import os
import sys
from pathlib import Path


def convert_stl_to_dxf(input_path, output_path=None):
    """
    Convert a single STL file to DXF format.
    
    Args:
        input_path (str): Path to the input STL file
        output_path (str, optional): Path for the output DXF file. 
                                    If None, saves in the same directory as input.
    
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        import pymeshlab
    except ImportError:
        print("Error: pymeshlab is not installed. Please install it using:")
        print("    pip install pymeshlab")
        sys.exit(1)
    
    try:
        ms = pymeshlab.MeshSet()
        
        # Load the STL file
        print(f"Loading: {input_path}")
        ms.load_new_mesh(input_path)
        
        # Determine output path
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.dxf'))
        
        # Save as DXF
        print(f"Saving to: {output_path}")
        ms.save_current_mesh(output_path)
        
        print(f"✓ Successfully converted: {os.path.basename(input_path)}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {input_path}: {str(e)}")
        return False


def process_directory(input_dir, output_dir=None, recursive=True):
    """
    Process all STL files in a directory.
    
    Args:
        input_dir (str): Path to the input directory
        output_dir (str, optional): Path to the output directory. 
                                   If None, saves DXF files next to STL files.
        recursive (bool): Whether to search subdirectories recursively
    
    Returns:
        tuple: (successful_count, failed_count)
    """
    input_path = Path(input_dir)
    
    if not input_path.is_dir():
        print(f"Error: {input_dir} is not a valid directory")
        return 0, 0
    
    # Find all STL files
    if recursive:
        stl_files = list(input_path.rglob('*.stl'))
    else:
        stl_files = list(input_path.glob('*.stl'))
    
    if not stl_files:
        print(f"No STL files found in {input_dir}")
        return 0, 0
    
    print(f"\nFound {len(stl_files)} STL file(s) to convert")
    print("-" * 60)
    
    successful = 0
    failed = 0
    
    for i, stl_file in enumerate(stl_files, 1):
        print(f"\n[{i}/{len(stl_files)}]")
        
        # Determine output path
        if output_dir:
            output_path = Path(output_dir) / stl_file.relative_to(input_path).with_suffix('.dxf')
            output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path = None
        
        if convert_stl_to_dxf(str(stl_file), str(output_path) if output_path else None):
            successful += 1
        else:
            failed += 1
    
    return successful, failed


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Convert VTK/STL files to DXF format using PyMeshLab',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Convert a single file:
    %(prog)s input.stl
    
  Convert all STL files in a directory:
    %(prog)s /path/to/stl/directory/
    
  Convert with custom output directory:
    %(prog)s /path/to/stl/directory/ --output /path/to/output/
    
  Convert without recursing into subdirectories:
    %(prog)s /path/to/stl/directory/ --no-recursive
        """
    )
    
    parser.add_argument(
        'input',
        help='Input STL file or directory containing STL files'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output directory for DXF files (default: same as input)',
        default=None
    )
    
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Do not search subdirectories for STL files'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Validate input path
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    # Process based on whether input is a file or directory
    if input_path.is_file():
        if not input_path.suffix.lower() == '.stl':
            print("Error: Input file must be an STL file")
            sys.exit(1)
        
        output_path = args.output
        if output_path and Path(output_path).is_dir():
            output_path = str(Path(output_path) / input_path.with_suffix('.dxf').name)
        
        success = convert_stl_to_dxf(str(input_path), output_path)
        sys.exit(0 if success else 1)
        
    elif input_path.is_dir():
        successful, failed = process_directory(
            str(input_path),
            args.output,
            recursive=not args.no_recursive
        )
        
        print("\n" + "=" * 60)
        print(f"Conversion complete!")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Total: {successful + failed}")
        print("=" * 60)
        
        sys.exit(0 if failed == 0 else 1)
    
    else:
        print(f"Error: '{args.input}' is neither a file nor a directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
