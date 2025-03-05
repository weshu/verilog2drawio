import xml.etree.ElementTree as ET

def draw_submodules(root, submodules, module_width, next_id):
    """
    绘制子模块和子模块的端口
    :param root: XML 根元素
    :param submodules: 子模块列表，每个元素为包含 name, module_name 等信息的字典
    :param module_width: 主模块宽度
    :param next_id: 下一个可用的 ID
    :return: (next_id, submodule_port_map) 元组，其中 submodule_port_map 为子模块端口映射
    """
    submodule_port_map = {}
    submodule_height = 100  # 子模块高度
    submodule_spacing = 50  # 子模块之间的间距
    total_height = len(submodules) * (submodule_height + submodule_spacing) - submodule_spacing
    start_y = 200  # 起始y坐标
    
    # 初始化子模块位置变量
    submodule_x = module_width // 2  # 将子模块放置在模块宽度的中间
    submodule_y = 200  # 初始y坐标

    for i, submodule in enumerate(submodules):
        submodule_type = submodule['module_name']
        submodule_name = submodule['name']
        
        # 计算子模块的位置
        x = module_width//2 # 子模块在主模块中间
        y = start_y + i * (submodule_height + submodule_spacing)
        
        # 创建子模块
        submodule_cell = ET.SubElement(root, 'mxCell', {
            'id': str(next_id),
            'value': f"{submodule_type}\n{submodule_name}",
            'style': 'swimlane;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;',
            'vertex': '1',
            'parent': '1'
        })
        
        # 添加子模块的 mxGeometry
        submodule_geometry = ET.SubElement(submodule_cell, 'mxGeometry', {
            'x': str(x),
            'y': str(y),
            'width': '120',
            'height': str(submodule_height),
            'as': 'geometry'
        })
        
        next_id += 1
        submodule_y += 120  # 将下一个子模块向下移动 120 像素

    return next_id, submodule_port_map