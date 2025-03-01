import xml.etree.ElementTree as ET


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
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
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', {
        'dx': '946',
        'dy': '625',
        'grid': '1',
        'gridSize': '10',
        'guides': '1',
        'tooltips': '1',
        'connect': '1',
        'arrows': '1',
        'fold': '1',
        'page': '1',
        'pageScale': '1',
        'pageWidth': '1169',
        'pageHeight': '827',
        'math': '0',
        'shadow': '0'
    })
    root = ET.SubElement(mxGraphModel, 'root')

    # 创建初始的 mxCell 元素
    mxCell_0 = ET.SubElement(root, 'mxCell', {'id': '0'})
    mxCell_1 = ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})

    # 创建主模块方框
    main_module_id = 2
    main_module = ET.SubElement(root, 'mxCell', {
        'id': str(main_module_id),
        'value': module_name,
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;',
        'vertex': '1',
        'x': '50',
        'y': '50',
        'width': '200',
        'height': '200',
        'parent': '1'
    })
    # 添加主模块的 mxGeometry
    main_module_geometry = ET.SubElement(main_module, 'mxGeometry', {
        'x': '50',
        'y': '50',
        'width': '200',
        'height': '200',
        'as': 'geometry'
    })

    # 绘制主模块的端口
    input_port_y = 70
    output_port_y = 70
    inout_port_y = 70
    next_id = 3
    port_map = {}
    for port_type, port_name in ports:
        if port_type == 'input':
            x = 50
            y = input_port_y
            input_port_y += 30
        elif port_type == 'output':
            x = 250
            y = output_port_y
            output_port_y += 30
        else:  # inout
            x = 150
            y = inout_port_y
            inout_port_y += 30

        port = ET.SubElement(root, 'mxCell', {
            'id': str(next_id),
            'value': port_name,
            'style': 'shape=ellipse;whiteSpace=wrap;html=1;',
            'vertex': '1',
            'parent': '1',
            'x': str(x),
            'y': str(y),
            'width': '10',
            'height': '10'
        })
        # 添加端口的 mxGeometry
        port_geometry = ET.SubElement(port, 'mxGeometry', {
            'x': str(x),
            'y': str(y),
            'width': '10',
            'height': '10',
            'as': 'geometry'
        })
        port_map[port_name] = next_id
        next_id += 1

    # 绘制子模块
    submodule_x = 70
    submodule_y = 70
    submodule_port_map = {}
    for submodule_type, submodule_name in submodules:
        submodule = ET.SubElement(root, 'mxCell', {
            'id': str(next_id),
            'value': f'{submodule_type} {submodule_name}',
            'style': 'shape=rectangle;whiteSpace=wrap;html=1;',
            'vertex': '1',
            'parent': '1',
            'x': str(submodule_x),
            'y': str(submodule_y),
            'width': '100',
            'height': '100'
        })
        # 添加子模块的 mxGeometry
        submodule_geometry = ET.SubElement(submodule, 'mxGeometry', {
            'x': str(submodule_x),
            'y': str(submodule_y),
            'width': '100',
            'height': '100',
            'as': 'geometry'
        })
        submodule_port_map[submodule_name] = {}
        submodule_id = next_id
        next_id += 1

        # 绘制子模块端口
        sub_input_port_y = submodule_y + 20
        sub_output_port_y = submodule_y + 20
        sub_inout_port_y = submodule_y + 20
        for submodule_name_, sub_port, main_port in connections:
            if submodule_name_ == submodule_name:
                if sub_port.startswith('input'):
                    x = submodule_x
                    y = sub_input_port_y
                    sub_input_port_y += 20
                elif sub_port.startswith('output'):
                    x = submodule_x + 100
                    y = sub_output_port_y
                    sub_output_port_y += 20
                else:  # inout
                    x = submodule_x + 50
                    y = sub_inout_port_y
                    sub_inout_port_y += 20

                sub_port_cell = ET.SubElement(root, 'mxCell', {
                    'id': str(next_id),
                    'value': sub_port,
                    'style': 'shape=ellipse;whiteSpace=wrap;html=1;',
                    'vertex': '1',
                    'parent': str(submodule_id),
                    'x': str(x),
                    'y': str(y),
                    'width': '10',
                    'height': '10'
                })
                # 添加子模块端口的 mxGeometry
                sub_port_geometry = ET.SubElement(sub_port_cell, 'mxGeometry', {
                    'x': str(x),
                    'y': str(y),
                    'width': '10',
                    'height': '10',
                    'as': 'geometry'
                })
                submodule_port_map[submodule_name][sub_port] = next_id
                next_id += 1

    # 绘制连线
    for submodule_name, sub_port, main_port in connections:
        if main_port in port_map and sub_port in submodule_port_map[submodule_name]:
            edge = ET.SubElement(root, 'mxCell', {
                'id': str(next_id),
                'style': 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;',
                'edge': '1',
                'parent': '1',
                'source': str(port_map[main_port]),
                'target': str(submodule_port_map[submodule_name][sub_port])
            })
            # 添加连线的 mxGeometry
            edge_geometry = ET.SubElement(edge, 'mxGeometry', {
                'relative': '1',
                'as': 'geometry'
            })
            next_id += 1

    # 保存 Drawio 文件
    tree = ET.ElementTree(mxfile)
    indent(tree.getroot())
    try:
        tree.write(f'{module_name}.drawio', encoding='utf-8', xml_declaration=True)
        print(f"成功生成 Drawio 文件: {module_name}.drawio")
    except Exception as e:
        print(f"生成 Drawio 文件 {module_name}.drawio 时出错: {e}")


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
