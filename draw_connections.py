import xml.etree.ElementTree as ET

def draw_connections(root, connections, port_map, submodule_port_map, next_id):
    """
    绘制连接
    :param root: XML 根元素
    :param connections: 连接信息列表，每个元素为 (submodule_name, submodule_port, main_port) 元组
    :param port_map: 主模块端口映射，key 为端口名，value 为端口 ID
    :param submodule_port_map: 子模块端口映射，key 为子模块名，value 为子模块端口映射
    :param next_id: 下一个可用的 ID
    :return: 下一个可用的 ID
    """
    for conn in connections:
        submodule_name, submodule_port, main_port = conn
        
        # 检查主模块端口是否存在
        if main_port not in port_map:
            continue
            
        # 检查子模块是否存在
        if submodule_name not in submodule_port_map:
            continue
            
        # 检查子模块端口是否存在
        if submodule_port not in submodule_port_map[submodule_name]:
            continue
            
        # 获取端口 ID
        main_port_id = port_map[main_port]
        submodule_port_id = submodule_port_map[submodule_name][submodule_port]
        
        # 创建连接线
        edge = ET.SubElement(root, 'mxCell', {
            'id': str(next_id),
            'value': '',
            'style': 'endArrow=classic;html=1;rounded=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;',
            'edge': '1',
            'parent': '1',
            'source': str(main_port_id),
            'target': str(submodule_port_id)
        })
        
        # 添加连接的 mxGeometry
        edge_geometry = ET.SubElement(edge, 'mxGeometry', {
            'relative': '1',
            'as': 'geometry'
        })
        
        next_id += 1

    return next_id