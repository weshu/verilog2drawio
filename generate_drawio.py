import xml.etree.ElementTree as ET

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def generate_drawio(module_name, ports, submodules, connections):
    """
    生成 Drawio XML 文件
    :param module_name: 模块名
    :param ports: 端口列表
    :param submodules: 子模块列表
    :param connections: 连接信息列表
    """
    # 创建 Drawio XML 结构
    mxfile = ET.Element('mxfile')
    diagram = ET.SubElement(mxfile, 'diagram')
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel')
    root = ET.SubElement(mxGraphModel, 'root')

    # 创建主模块方框
    main_module = ET.SubElement(root, 'mxCell', {
        'id': '1',
        'value': module_name,
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;',
        'vertex': '1',
        'x': '100',
        'y': '100',
        'width': '400',
        'height': '400'
    })

    # 绘制主模块的端口
    input_port_y = 120
    output_port_y = 120
    inout_port_y = 120
    port_id = 2
    port_map = {}
    for port_type, port_name in ports:
        if port_type == 'input':
            x = 100
            y = input_port_y
            input_port_y += 30
        elif port_type == 'output':
            x = 500
            y = output_port_y
            output_port_y += 30
        else:  # inout
            x = 300
            y = inout_port_y
            inout_port_y += 30

        port = ET.SubElement(root, 'mxCell', {
            'id': str(port_id),
            'value': port_name,
            'style': 'shape=ellipse;whiteSpace=wrap;html=1;',
            'vertex': '1',
            'parent': '1',
            'x': str(x),
            'y': str(y),
            'width': '20',
            'height': '20'
        })
        port_map[port_name] = port_id
        port_id += 1

    # 绘制子模块
    submodule_x = 150
    submodule_y = 150
    submodule_port_id = port_id
    submodule_port_map = {}
    for submodule_type, submodule_name in submodules:
        submodule = ET.SubElement(root, 'mxCell', {
            'id': str(submodule_port_id),
            'value': f'{submodule_type} {submodule_name}',
            'style': 'shape=rectangle;whiteSpace=wrap;html=1;',
            'vertex': '1',
            'parent': '1',
            'x': str(submodule_x),
            'y': str(submodule_y),
            'width': '200',
            'height': '150'
        })
        submodule_port_map[submodule_name] = {}
        submodule_port_id += 1

    # 绘制子模块端口并连接
    for submodule_name, sub_port, main_port in connections:
        if main_port in port_map:
            submodule = next((s for s in submodules if s[1] == submodule_name), None)
            if submodule:
                submodule_id = list(submodules).index(submodule) + port_id
                sub_x = 150 + submodule_id * 220
                sub_y = 150
                if sub_port.startswith('input'):
                    x = sub_x
                    y = sub_y + 20
                elif sub_port.startswith('output'):
                    x = sub_x + 200
                    y = sub_y + 20
                else:  # inout
                    x = sub_x + 100
                    y = sub_y + 20

                sub_port_cell = ET.SubElement(root, 'mxCell', {
                    'id': str(submodule_port_id),
                    'value': sub_port,
                    'style': 'shape=ellipse;whiteSpace=wrap;html=1;',
                    'vertex': '1',
                    'parent': str(submodule_id),
                    'x': str(x),
                    'y': str(y),
                    'width': '20',
                    'height': '20'
                })
                submodule_port_map[submodule_name][sub_port] = submodule_port_id

                # 绘制连线
                edge = ET.SubElement(root, 'mxCell', {
                    'id': str(port_id),
                    'style': 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;',
                    'edge': '1',
                    'source': str(port_map[main_port]),
                    'target': str(submodule_port_id),
                    'parent': '1'
                })
                port_id += 1
                submodule_port_id += 1

    # 保存 Drawio 文件
    tree = ET.ElementTree(mxfile)
    indent(tree.getroot())  # 使用自定义的缩进函数
    tree.write(f'{module_name}.drawio', encoding='utf-8', xml_declaration=True)
   
# 单元测试
import unittest
import os


class TestGenerateDrawio(unittest.TestCase):
    def setUp(self):
        self.test_module_name = './test/test_module'
        self.test_ports = [('input', 'in1'), ('output', 'out1')]
        self.test_submodules = [('sub_module', 'sub_inst')]
        self.test_connections = [('sub_inst', 'in_port', 'in1'), ('sub_inst', 'out_port', 'out1')]

    def tearDown(self):
        pass

    def test_generate_drawio(self):
        generate_drawio(self.test_module_name, self.test_ports, self.test_submodules, self.test_connections)
        drawio_file = f'{self.test_module_name}.drawio'
        self.assertEqual(os.path.exists(drawio_file), True)


if __name__ == '__main__':
    unittest.main()