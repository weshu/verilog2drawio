import re
import os

# 全局定义正则表达式模式
module_pattern = re.compile(r'module\s+(\w+)(?:\s*#\s*\((.*?)\))?\s*\((.*?)\)\s*;(.*?)endmodule', re.DOTALL)
port_pattern = re.compile(r'(input|output|inout)\s*(wire|reg)?\s*(\w+)')
submodule_pattern = re.compile(r'(\w+)\s+(\w+)\s*\((.*?)\);', re.DOTALL)
connection_pattern = re.compile(r'\.(.*?)\((.*?)\)')

def parse_verilog(file_path):
    """
    解析 Verilog 文件，提取模块信息
    :param file_path: Verilog 文件路径
    :return: 模块信息字典，键为模块名，值为 (ports, submodules, connections) 元组
    """
    with open(file_path, 'r') as file:
        content = file.read()

    modules = {}
    for match in module_pattern.finditer(content):
        module_name = match.group(1)
        ports_str = match.group(3)
        body = match.group(4)

        # 提取端口信息
        ports = []
        for port_match in port_pattern.finditer(ports_str):
            port_type = port_match.group(1)
            port_name = port_match.group(3)
            ports.append((port_type, port_name))

        # 提取子模块信息
        submodules = []
        connections = []
        for submodule_match in submodule_pattern.finditer(body):
            submodule_type = submodule_match.group(1)
            submodule_name = submodule_match.group(2)
            submodules.append((submodule_type, submodule_name))

            # 提取连接信息
            connections_str = submodule_match.group(3)
            for conn_match in connection_pattern.finditer(connections_str):
                sub_port = conn_match.group(1)
                main_port = conn_match.group(2)
                connections.append((submodule_name, sub_port, main_port))

        modules[module_name] = (ports, submodules, connections)

    return modules

# 单元测试
import unittest
import glob

class TestParseVerilog(unittest.TestCase):
    def setUp(self):
        self.test_verilog_files = glob.glob('./test/test_verilog_[1-99].v')

    def tearDown(self):
        pass

    def test_parse_verilog(self):
        for file_path in self.test_verilog_files:
            with self.subTest(file_path=file_path):
                modules = parse_verilog(file_path)
                print(modules)
                self.assertEqual(isinstance(modules, dict), True)
                # 假设每个测试文件至少有一个模块
                self.assertGreater(len(modules), 0)

if __name__ == '__main__':
    import os
    unittest.main()