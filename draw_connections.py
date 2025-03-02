import xml.etree.ElementTree as ET

def draw_connections(root, connections, port_map, submodule_port_map, next_id):
    """
    绘制连接
    :param root: XML 根元素
    :param connections: 连接信息列表
    :param port_map: 主模块端口映射
    :param submodule_port_map: 子模块端口映射
    :param next_id: 下一个可用的 ID
    """
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