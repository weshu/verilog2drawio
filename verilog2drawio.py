import sys
import unittest
from pathlib import Path
from parse_verilog import parse_verilog
from generate_drawio import generate_drawio


def main(verilog_file_path):
    """
    主函数，读取 Verilog 文件并生成 Drawio 文件
    :param verilog_file_path: Verilog 文件路径
    """
    try:
        modules = parse_verilog(verilog_file_path)
        print(f"Parsed {len(modules)} modules from {verilog_file_path}")
        for module_name, (ports, submodules, connections) in modules.items():
            # 打印模块信息
            print(f"Module: {module_name}")
            print(f"  Ports: {ports}")
            print(f"  Submodules: {submodules}")
            print(f"  Connections: {connections}")
            generate_drawio(module_name, ports, submodules, connections)
    except Exception as e:
        print(f"Error processing file {verilog_file_path}: {e}")
        sys.exit(1)


def run_tests():
    """
    运行单元测试
    """
    suite1 = unittest.TestLoader().loadTestsFromModule(__import__('parse_verilog'))
    suite2 = unittest.TestLoader().loadTestsFromModule(__import__('generate_drawio'))
    all_tests = unittest.TestSuite([suite1, suite2])
    unittest.TextTestRunner().run(all_tests)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_tests()
    elif len(sys.argv) != 2:
        print("Usage: python verilog2drawio.py <verilog_file_path> or python verilog2drawio.py --test")
        sys.exit(1)
    else:
        verilog_file_path = sys.argv[1]
        if not Path(verilog_file_path).is_file():
            print(f"File not found: {verilog_file_path}")
            sys.exit(1)
        main(verilog_file_path)