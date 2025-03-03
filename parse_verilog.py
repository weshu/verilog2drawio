import re
import os
import copy

# 全局定义正则表达式模式
# 更新 module_pattern 以支持参数化模块和多行端口列表
module_pattern = re.compile(r'module\s+(\w+)(?:\s*#\s*\((.*?)\))?[\s\n]*(\((.*?)\))?;(.*?)endmodule', re.DOTALL)
# 更新 port_pattern 以支持带位宽和 signed 关键字的端口声明
port_pattern = re.compile(r'\s*(input|output|inout)\s*(wire|reg)?\s*(signed|unsigned)?\s*(\[(\d+):(\d+)\])?\s*(\w+)', re.DOTALL)
# 更新 submodule_pattern 以确保它只匹配子模块实例化语句，包括参数化部分
submodule_pattern = re.compile(r'(\w+)\s+(#\s*\(.*?\)\s+)?(\w+)\s*\((.*?)\);', re.DOTALL)
connection_pattern = re.compile(r'\.(.*?)\((.*?)\)')
generate_pattern = re.compile(r'generate\s*(.*?)\s*endgenerate', re.DOTALL)
if_pattern = re.compile(r'if\s*\((.*?)\)\s*(begin)?\s*(.*?)\s*(end)', re.DOTALL)
else_pattern = re.compile(r'else\s*(begin)?\s*(.*?)\s*(end)?', re.DOTALL)

def parse_verilog(file_path, gen_smart_check=False):
    """
    解析 Verilog 文件，提取模块信息
    :param file_path: Verilog 文件路径
    :param gen_smart_check: 是否智能处理 generate 块，如果为 True，则只处理条件为真/假的部分；如果为 False，则处理所有部分
    :return: 模块信息列表，每个元素为 (module_name, ports, submodules, connections) 元组
    """
    with open(file_path, 'r') as file:
        content = file.read()

    modules = []
    for match in module_pattern.finditer(content):
        module_name = match.group(1)
        params_str = match.group(2)
        ports_str = match.group(3)
        body = match.group(5)

        # 提取参数默认值
        params = {}
        if params_str:
            for param in params_str.split(','):
                param = param.strip()
                if '=' in param:
                    param_name, param_default = param.split('=')
                    param_parts = param_name.strip().split()
                    if len(param_parts) > 1 and param_parts[0] == "parameter":
                        param_name = param_parts[1]
                        params[param_name.strip()] = param_default.strip()

        # 如果 ports_str 为 None 或为空字符串，则从 body 中提取端口信息
        if ports_str is None or ports_str.strip() == "":
            ports_str = body
        if ports_str is None:
            ports_str = ""
        if (0):
            print(f"Ports: {ports_str}")

        # 提取端口信息
        ports = []
        for port_match in port_pattern.finditer(ports_str):
            port_type = port_match.group(1)
            port_keyword = port_match.group(2) or ''
            port_signed = port_match.group(3) or ''
            port_width = port_match.group(4) or ''
            port_name = port_match.group(7)
            if port_width:
                port_width_start, port_width_end = port_width[1:-1].split(':')
            else:
                port_width_start = ''
                port_width_end = ''
            ports.append({
                'type': port_type,
                'keyword': port_keyword,
                'signed': port_signed,
                'width': f"{port_width_start}:{port_width_end}" if port_width_start else '',
                'name': port_name
            })

        # 提取子模块信息和连接信息
        submodules, connections = extract_submodules_and_connections(body, params, gen_smart_check)

        modules.append((module_name, ports, submodules, connections))

    return modules

def extract_submodules_and_connections(body, params, gen_smart_check=False):
    """
    从模块体中提取子模块和连接信息
    :param body: 模块体文本
    :param params: 参数字典
    :param gen_smart_check: 是否智能处理 generate 块
    :return: (submodules, connections) 元组
    """
    submodules = []
    connections = []

    generate_matches = list(generate_pattern.finditer(body))
    previous_end = 0

    for generate_match in generate_matches:
        # 处理 generate 块之前的文本
        body_to_parse = body[previous_end:generate_match.start()]
        extract_submodules_and_connections_from_body(body_to_parse, submodules, connections)
        
        # 处理 generate 块内部的文本
        generate_body = copy.deepcopy(generate_match.group(1))  # 使用深拷贝
        if_match = if_pattern.search(generate_body)

        if gen_smart_check and if_match:
            condition = if_match.group(1)
            if_body = copy.deepcopy(if_match.group(3))
            else_match = else_pattern.search(generate_body)
            else_body = copy.deepcopy(else_match.group(2)) if else_match else ""

            # 安全地评估条件表达式
            if safe_eval(condition, params):
                body_to_parse = if_body
            else:
                body_to_parse = else_body
        else:
            body_to_parse = generate_body

        extract_submodules_and_connections_from_body(body_to_parse, submodules, connections)
        # 更新 previous_end 为当前 generate 块的结束位置
        previous_end = generate_match.end()

    # 处理最后一个 generate 块之后的文本
    body_to_parse = body[previous_end:]
    extract_submodules_and_connections_from_body(body_to_parse, submodules, connections)
    return submodules, connections

def extract_submodules_and_connections_from_body(body, submodules, connections):
    for submodule_match in submodule_pattern.finditer(body):
        submodule_type = submodule_match.group(1)
        submodule_name = submodule_match.group(3)
        submodules.append((submodule_type, submodule_name))

        # 提取连接信息
        connections_str = submodule_match.group(4)
        for conn_match in connection_pattern.finditer(connections_str):
            sub_port = conn_match.group(1)
            main_port = conn_match.group(2)
            connections.append((submodule_name, sub_port, main_port))

def safe_eval(condition, params):
    # 简单的条件判断，仅支持常量条件
    try:
        return eval(params[condition], {}, params)
    except Exception as e:
        print(f"Error evaluating condition: {condition}, {e}")
        return False

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