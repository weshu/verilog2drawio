"""
Verilog parser wrapper for hdlparse.
This module serves as an adapter between hdlparse and the rest of the application.
"""

from hdlparse.hdlparse.verilog_parser import VerilogExtractor
import os
import re

# Create a global VerilogExtractor instance
_verilog_extractor = VerilogExtractor()

def verilog_module_to_dict(module):
    """
    将 VerilogModule 对象转换为可 JSON 序列化的字典
    
    Args:
        module: VerilogModule object from hdlparse
        
    Returns:
        dict: Dictionary representation of the module
    """
    return {
        'name': module.name,
        'ports': [{
            'name': port.name,
            'mode': port.mode,
            'type': port.data_type if port.data_type else 'wire'
        } for port in module.ports],
        'submodules': [{
            'name': instance.module_type,
            'module_name': instance.instance_name
        } for instance in module.submodules]
    }

def parse_verilog(file_path):
    """
    Parse a Verilog file using hdlparse and return module definitions.
    
    Args:
        file_path (str): Path to the Verilog file
        
    Returns:
        list: List of dictionaries representing Verilog modules, where each module contains:
              - name: Name of the module
              - ports: List of port dictionaries with attributes:
                      - name: Port name
                      - mode: Port direction (input/output/inout)
                      - type: Port data type with width information
              - submodules: List of module instances (submodules)
    """
    print(f"Attempting to parse file: {file_path}")
    try:
        objects = _verilog_extractor.extract_objects(file_path)
        print(f"Extracted {len(objects)} objects")
        
        # Convert VerilogModule objects to dictionaries
        modules = [verilog_module_to_dict(obj) for obj in objects]
        print(f"Converted {len(modules)} modules to dictionaries")
        
        return modules
    except Exception as e:
        print(f"Error parsing file: {str(e)}")
        return None

# Unit tests
import unittest
import glob
import os

class TestParseVerilog(unittest.TestCase):
    def setUp(self):
        # Get all test files from the test directory
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test')
        self.test_verilog_files = glob.glob(os.path.join(self.test_dir, '*.v'))
        print(f"\nFound {len(self.test_verilog_files)} test files in {self.test_dir}")

    def tearDown(self):
        pass

    def test_parse_verilog(self):
        """Test parsing of Verilog files"""
        for file_path in self.test_verilog_files:
            with self.subTest(file_path=file_path):
                print(f"\nTesting file: {os.path.basename(file_path)}")
                modules = parse_verilog(file_path)
                
                # Basic validation
                self.assertIsNotNone(modules, f"Failed to parse {file_path}")
                self.assertIsInstance(modules, list, f"Expected list of modules for {file_path}")
                
                # Check that we found at least one module
                self.assertGreater(len(modules), 0, f"No modules found in {file_path}")
                
                # Check each module's structure
                for module in modules:
                    # Check module has required attributes
                    self.assertIn('name', module, f"Module missing 'name' in {file_path}")
                    self.assertIn('ports', module, f"Module missing 'ports' in {file_path}")
                    self.assertIn('submodules', module, f"Module missing 'submodules' in {file_path}")
                    
                    # Check ports
                    for port in module['ports']:
                        self.assertIn('name', port, f"Port missing 'name' in {file_path}")
                        self.assertIn('mode', port, f"Port missing 'mode' in {file_path}")
                        self.assertIn('type', port, f"Port missing 'type' in {file_path}")
                        self.assertIn(port['mode'], ['input', 'output', 'inout'], 
                                    f"Invalid port direction '{port['mode']}' in {file_path}")
                        self.assertIsInstance(port['type'], str, f"Port type should be a string in {file_path}")
                    
                    # Check submodules
                    for submodule in module['submodules']:
                        self.assertIn('name', submodule, f"Submodule missing 'name' in {file_path}")
                        self.assertIn('module_name', submodule, f"Submodule missing 'instance' in {file_path}")
                
                # Print summary
                print(f"Successfully parsed {len(modules)} modules")
                for module in modules:
                    print(f"  Module: {module['name']}")
                    print(f"    Ports: {len(module['ports'])}")
                    print(f"    Submodules: {len(module['submodules'])}")

if __name__ == '__main__':
    unittest.main(verbosity=2)