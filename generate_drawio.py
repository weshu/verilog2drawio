import xml.etree.ElementTree as ET
from draw_main_module import draw_main_module
from draw_submodules import draw_submodules
from draw_connections import draw_connections

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
    :param ports: 端口字典列表
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

    # 计算模块框的高度和宽度
    port_height = 30
    input_ports = [port for port in ports if port['type'] == 'input']
    output_ports = [port for port in ports if port['type'] == 'output']
    input_height = len(input_ports) * port_height
    output_height = len(output_ports) * port_height
    module_height = 50 + max(input_height, output_height)
    max_port_name_length = max(len(port['name']) for port in ports) if ports else 0
    module_width = max_port_name_length * 10 * 2 + 40

    # 绘制主模块和主模块的端口
    next_id, port_map = draw_main_module(root, module_name, ports, module_width, module_height)

    # 绘制子模块和子模块的端口
    next_id, submodule_port_map = draw_submodules(root, submodules, module_width, next_id)

    # 绘制连接
    draw_connections(root, connections, port_map, submodule_port_map, next_id)

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
        self.test_ports = [
            {'type': 'input', 'name': 'in1'},
            {'type': 'output', 'name': 'out1'}
        ]
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