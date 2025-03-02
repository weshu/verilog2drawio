import xml.etree.ElementTree as ET

def draw_main_module(root, module_name, ports, module_width, module_height):
    """
    绘制主模块和主模块的端口
    :param root: XML 根元素
    :param module_name: 模块名
    :param ports: 端口列表
    :param module_width: 模块宽度
    :param module_height: 模块高度
    """
    # 创建主模块方框
    main_module_id = 2
    main_module = ET.SubElement(root, 'mxCell', {
        'id': str(main_module_id),
        'value': '',
        'style': 'shape=rectangle;whiteSpace=wrap;html=1;',
        'vertex': '1',
        'x': '50',
        'y': '50',
        'width': str(module_width),
        'height': str(module_height),
        'parent': '1'
    })
    # 添加主模块的 mxGeometry
    main_module_geometry = ET.SubElement(main_module, 'mxGeometry', {
        'x': '50',
        'y': '50',
        'width': str(module_width),
        'height': str(module_height),
        'as': 'geometry'
    })

    # 添加模块名称文本
    module_name_cell = ET.SubElement(root, 'mxCell', {
        'id': str(main_module_id + 1),
        'value': module_name,
        'style': 'text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=32;',
        'vertex': '1',
        'parent': str(main_module_id)
    })
    # 添加模块名称文本的 mxGeometry
    module_name_geometry = ET.SubElement(module_name_cell, 'mxGeometry', {
        'x': str(module_width//2-50),
        'y': '10',
        'width': '100',
        'height': '30',
        'as': 'geometry'
    })
    # 绘制主模块的端口
    input_port_y = 70
    output_port_y = 70
    inout_port_y = module_height - 20  # 将 inout 端口放置在模块框的底部
    next_id = main_module_id + 2
    port_map = {}
    for port_type, _, _, _, port_name in ports:  # 修改这里，只提取 port_type 和 port_name
        if port_type == 'input':
            x = 50-5
            y = input_port_y
            input_port_y += 30
            port_style = 'shape=rectangle;whiteSpace=wrap;html=1;labelPosition=right;verticalLabelPosition=middle;align=left;verticalAlign=middle;'  # 将端口名称移动到端口的右侧
        elif port_type == 'output':
            x = module_width+50-5
            y = output_port_y
            output_port_y += 30
            port_style = 'shape=rectangle;whiteSpace=wrap;html=1;labelPosition=left;verticalLabelPosition=middle;align=right;verticalAlign=middle;'  # 将端口名称移动到端口的左侧
        else:  # inout
            x = module_width // 2
            y = inout_port_y
            inout_port_y -= 30  # 逐个向上排列 inout 端口
            port_style = 'shape=rectangle;whiteSpace=wrap;html=1;labelPosition=top;verticalLabelPosition=middle;align=bottom;verticalAlign=middle;'  # 将端口名称移动到端口的右侧

        port = ET.SubElement(root, 'mxCell', {
            'id': str(next_id),
            'value': port_name,
            'style': port_style,
            'vertex': '1',
            'parent': '1',
            'x': str(x),  # 修改端口名称的 x 坐标
            'y': str(y),
            'width': '10',
            'height': '10'
        })
        # 添加端口的 mxGeometry
        port_geometry = ET.SubElement(port, 'mxGeometry', {
            'x': str(x),  # 修改端口名称的 x 坐标
            'y': str(y),
            'width': '10',
            'height': '10',
            'as': 'geometry'
        })
        port_map[port_name] = next_id
        next_id += 1

    return next_id, port_map