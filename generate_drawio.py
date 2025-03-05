import xml.etree.ElementTree as ET
import os
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

def generate_drawio(module_name, ports, submodules, connections, port_groups=None, output_file=None):
    """
    生成 Drawio XML 文件
    :param module_name: 模块名
    :param ports: 端口列表，每个元素为包含 name, type, width 等信息的字典
    :param submodules: 子模块列表，每个元素为包含 name, instance 等信息的字典
    :param connections: 连接信息列表
    :param port_groups: 端口组列表，每个元素为 {'name': group_name, 'ports': [port_dict]}
    :param output_file: 输出文件路径，如果为None则使用默认路径
    :return: 生成的 DrawIO 文件路径（相对于web根目录的路径）
    """
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

    mxCell_0 = ET.SubElement(root, 'mxCell', {'id': '0'})
    mxCell_1 = ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})

    port_height = 30
    input_ports = [port for port in ports if port['mode'] == 'input']
    output_ports = [port for port in ports if port['mode'] == 'output']
    input_height = len(input_ports) * port_height
    output_height = len(output_ports) * port_height
    module_height = 50 + max(input_height, output_height)
    max_port_name_length = max(len(port['name']) for port in ports) if ports else 0
    module_width = max_port_name_length * 10 * 2 + 40

    display_module_name = os.path.splitext(os.path.basename(module_name))[0]

    next_id, port_map = draw_main_module(root, display_module_name, ports, module_width, module_height, port_groups)
    next_id, submodule_port_map = draw_submodules(root, submodules, module_width, next_id)
    draw_connections(root, connections, port_map, submodule_port_map, next_id)

    if output_file is None:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        downloads_dir = os.path.join(root_dir, 'downloads')
        os.makedirs(downloads_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(module_name))[0]
        safe_module_name = base_name.replace('/', '_').replace('\\', '_')
        file_path = os.path.join(downloads_dir, f'{safe_module_name}.drawio')
    else:
        file_path = output_file
    
    tree = ET.ElementTree(mxfile)
    indent(tree.getroot())
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        return f"/downloads/{os.path.basename(file_path)}"
    except Exception as e:
        print(f"Error generating DrawIO file: {str(e)}")
        return None

# 单元测试
import unittest
import os

class TestGenerateDrawio(unittest.TestCase):
    def setUp(self):
        self.test_module_name = 'test_module'
        self.test_ports = [
            {'name': 'in1', 'mode': 'input', 'type': 'wire'},
            {'name': 'out1', 'mode': 'output', 'type': 'wire'}
        ]
        self.test_submodules = [{'name': 'sub_module', 'module_name': 'sub_inst'}]
        self.test_connections = [('sub_inst', 'in_port', 'in1'), ('sub_inst', 'out_port', 'out1')]

    def tearDown(self):
        # 清理测试文件
        downloads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
        test_file = os.path.join(downloads_dir, f'{self.test_module_name}.drawio')
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_generate_drawio(self):
        file_path = generate_drawio(self.test_module_name, self.test_ports, self.test_submodules, self.test_connections)
        self.assertIsNotNone(file_path)
        # Get the actual file path from the downloads directory
        downloads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
        actual_file_path = os.path.join(downloads_dir, f'{self.test_module_name}.drawio')
        print(f"Checking for file at: {actual_file_path}")
        self.assertTrue(os.path.exists(actual_file_path))

if __name__ == '__main__':
    unittest.main()