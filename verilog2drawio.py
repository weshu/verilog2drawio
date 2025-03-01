from parse_verilog import parse_verilog
from generate_drawio import generate_drawio


def main(verilog_file_path):
    """
    主函数，读取 Verilog 文件并生成 Drawio 文件
    :param verilog_file_path: Verilog 文件路径
    """
    modules = parse_verilog(verilog_file_path)
    for module_name, (ports, submodules, connections) in modules.items():
        generate_drawio(module_name, ports, submodules, connections)


if __name__ == "__main__":
    import sys
    import unittest

    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # 运行单元测试
        suite1 = unittest.TestLoader().loadTestsFromModule(__import__('parse_verilog'))
        suite2 = unittest.TestLoader().loadTestsFromModule(__import__('generate_drawio'))
        all_tests = unittest.TestSuite([suite1, suite2])
        unittest.TextTestRunner().run(all_tests)
    elif len(sys.argv) != 2:
        print("Usage: python verilog2drawio.py <verilog_file_path> or python verilog2drawio.py --test")
        sys.exit(1)
    else:
        verilog_file_path = sys.argv[1]
        main(verilog_file_path)