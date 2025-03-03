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
        # 检查子模块和子模块端口是否存在
        if submodule_name not in submodule_port_map:
            print(f"Warning: Submodule {submodule_name} not found in submodule_port_map")
            continue
            
        if sub_port not in submodule_port_map[submodule_name]:
            print(f"Warning: Submodule port {sub_port} not found in submodule {submodule_name}")
            continue

        # 获取子模块端口的ID
        sub_port_id = submodule_port_map[submodule_name][sub_port]
        
        # 如果main_port为空，说明这是一个内部连接，跳过
        if not main_port:
            continue
            
        # 如果main_port是主模块的端口
        if main_port in port_map:
            # 创建从主模块端口到子模块端口的连接
            edge = ET.SubElement(root, 'mxCell', {
                'id': str(next_id),
                'style': 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;',
                'edge': '1',
                'parent': '1',
                'source': str(port_map[main_port]),
                'target': str(sub_port_id)
            })
            # 添加连线的 mxGeometry
            edge_geometry = ET.SubElement(edge, 'mxGeometry', {
                'relative': '1',
                'as': 'geometry'
            })
            next_id += 1
        else:
            # 这是一个内部连接，需要找到另一个子模块的端口
            for other_submodule, other_ports in submodule_port_map.items():
                if other_submodule != submodule_name and main_port in other_ports:
                    # 创建从子模块到子模块的连接
                    edge = ET.SubElement(root, 'mxCell', {
                        'id': str(next_id),
                        'style': 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;',
                        'edge': '1',
                        'parent': '1',
                        'source': str(sub_port_id),
                        'target': str(other_ports[main_port])
                    })
                    # 添加连线的 mxGeometry
                    edge_geometry = ET.SubElement(edge, 'mxGeometry', {
                        'relative': '1',
                        'as': 'geometry'
                    })
                    next_id += 1
                    break