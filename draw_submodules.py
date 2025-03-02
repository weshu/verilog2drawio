import xml.etree.ElementTree as ET

def draw_submodules(root, submodules, module_width, next_id):
    """
    绘制子模块和子模块的端口
    :param root: XML 根元素
    :param submodules: 子模块列表
    :param module_width: 模块宽度
    :param next_id: 下一个可用的 ID
    """
    submodule_x = module_width // 2  # 将子模块放置在模块宽度的中间
    submodule_y = 200
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

        # # 绘制子模块端口
        # sub_input_port_y = submodule_y + 20
        # sub_output_port_y = submodule_y + 20
        # sub_inout_port_y = submodule_y + 100  # 将 inout 端口放置在子模块框的底部
        # for sub_port, sub_port_type in [('input1', 'input'), ('output1', 'output'), ('inout1', 'inout')]:  # 示例端口
        #     if sub_port_type == 'input':
        #         x = submodule_x
        #         y = sub_input_port_y
        #         sub_input_port_y += 20
        #         port_name_x = x + 20  # 将端口名称移动到端口的右侧
        #     elif sub_port_type == 'output':
        #         x = submodule_x + 100
        #         y = sub_output_port_y
        #         sub_output_port_y += 20
        #         port_name_x = x - 20  # 将端口名称移动到端口的右侧
        #     else:  # inout
        #         x = submodule_x + 50
        #         y = sub_inout_port_y
        #         sub_inout_port_y -= 20  # 逐个向上排列 inout 端口
        #         port_name_x = x + 20  # 将端口名称移动到端口的右侧

        #     sub_port_cell = ET.SubElement(root, 'mxCell', {
        #         'id': str(next_id),
        #         'value': sub_port,
        #         'style': 'shape=rectangle;whiteSpace=wrap;html=1;',
        #         'vertex': '1',
        #         'parent': str(submodule_id),
        #         'x': str(port_name_x),  # 修改端口名称的 x 坐标
        #         'y': str(y),
        #         'width': '10',
        #         'height': '10'
        #     })
        #     # 添加子模块端口的 mxGeometry
        #     sub_port_geometry = ET.SubElement(sub_port_cell, 'mxGeometry', {
        #         'x': str(port_name_x),  # 修改端口名称的 x 坐标
        #         'y': str(y),
        #         'width': '10',
        #         'height': '10',
        #         'as': 'geometry'
        #     })
        #     submodule_port_map[submodule_name][sub_port] = next_id
        #     next_id += 1

        submodule_y += 120  # 将下一个子模块向下移动 120 像素

    return next_id, submodule_port_map