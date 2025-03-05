#!/usr/bin/env python3
"""
Command-line interface for Verilog to DrawIO conversion.
"""

import sys
import os
import argparse
from parse_verilog import parse_verilog
import generate_drawio
import unittest
import glob

def run_tests():
    """Run the unit tests"""
    suite = unittest.TestLoader().discover('.', pattern='*.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1

def main():
    parser = argparse.ArgumentParser(description="Convert Verilog module to DrawIO diagram")
    parser.add_argument('verilog_file', nargs='?', help='Path to Verilog file')
    parser.add_argument('-o', '--output', help='Output DrawIO file name')
    parser.add_argument('--test', action='store_true', help='Run unit tests')
    args = parser.parse_args()
    
    if args.test:
        return run_tests()
    
    if not args.verilog_file:
        parser.error("Please provide a Verilog file or use --test to run unit tests")
    
    verilog_file = args.verilog_file
    
    if not os.path.exists(verilog_file):
        print(f"Error: File {verilog_file} not found")
        return 1
    
    parsed_data = parse_verilog(verilog_file)
    if not parsed_data:
        print(f"Error parsing file {verilog_file}")
        return 1
    
    if args.output:
        output_file = args.output
    else:
        base_name = os.path.basename(verilog_file)
        output_file = os.path.join('downloads', base_name.replace('.v', '.drawio'))
    
    os.makedirs('downloads', exist_ok=True)
    
    print(f"Parsed module: {parsed_data[0]['name']}")
    print(f"Found {len(parsed_data[0]['ports'])} ports and {len(parsed_data[0]['submodules'])} submodules")
    
    try:
        generate_drawio.generate_drawio(
            parsed_data[0]['name'],
            parsed_data[0]['ports'],
            parsed_data[0]['submodules'],
            [],  # no connections for command line version
            None,  # no port groups for command line version
            output_file
        )
        print(f"Successfully generated DrawIO file: {output_file}")
    except Exception as e:
        print(f"Error generating DrawIO file: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    sys.exit(main())