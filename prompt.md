I want to add an flask web ui for this verilog2drawio app, the python function code may also be modified too. the basic concept is:
 1, modern look UI, user can do all the operations in single page UI.
 2, a group of button on the left of the UI to help user follow the flows.
 3, btn to open the verilog file upload page on the right pannel, support drag function to upload.
 4, btn to parse the verilog file, display net group configuration panel on the right, shows all the input/output/inout ports (with auto group), user can group the ports.
 5, submodule edit botton and panel, user select the submodules that will be shown.
 6, generate drawio botton and panel,  based on the port/submodule information, generate draw.io xml file. 


 I hope to improve the index.html as follows:
 1. It have left pannel and right pannel, the width of left pannel is 20%, the width of right pannel is 80%.
 2. The left pannel have a group of button, each button is a function, like parse verilog, port configuration, submodule configuration, generate drawio, etc.
 3. The right pannel have a group of panel, each panel is a function, like verilog file upload, port configuration, submodule configuration, generate drawio, etc.
 4. The verilog file upload panel have a drag function to upload the verilog file.
 5. The port configuration panel shows all the input/output/inout ports, user can group the ports for simplify display.
 6. The submodule configuration panel shows all the submodules, user can select the submodules that will be shown.
 7. The generate drawio panel shows the draw.io xml file, user can download the file.


 bueatify the index.html, change the left pannel to a navbar, add a footer, add a header, change the right panel to a main

 change the height of this page, make it 100% height.

 could we seperate the "upload, port-config, submodule-config, generate-drawio" these 4 panels into seperate file? so the index.html can be short and clean

 in port configuration panel, we should:
 1. when loaded, call the parse_verilog function to get the port information, and display it as a list view.
 2. user will select the 1 or several ports, and click the group button, then the selected ports will be grouped together.
 3. user can edit the group name
 4. user can add more groups, and delete groups
 5. after click the save button, then the group configuration will be saved
 6. then redirect to submodule configuration panel

I'd like to change the display of the port configuration panel:
1. the port/group display should be a 3 column table
2. the 1st column is group name, the 2nd column is port name, the 3rd column is port type(nput, output, inout)
3. each port can not be in more than one group
4. multiple ports can be selected, and then the group button can be clicked, then the selected ports will be grouped together, and assiged a default group name, grp_id_xxxx, user can edit the name later.
5. multiple ports can be selected, and then the ungroup button can be clicked, then the selected ports will be ungrouped.
6. gouped ports displayed together, under the ungrouped ports

the port element is chaged from list to a dict, fix the code in generate_drawio.py that impacted, including the TestGenerateDrawio function. 
here is the dict code:
            ports.append({
                'type': port_type,
                'keyword': port_keyword,
                'signed': port_signed,
                'width': f"{port_width_start}:{port_width_end}" if port_width_start else '',
                'name': port_name
            })

in port-config.html, improve the followed:
1. make the table to have a modern look
2. use more decent way for multi-selection instead of checkbox
in index.html, handle that the right panel is very tall, may be a scroll bar is needed, make it morden look

in port-config.html, I want to move "group selected" and "ungroup selected" to the right side, when I scroll down the table, these 2 button keep the relative window position

perfect! I also want the table support "shift" and "ctrl" key for better selection.

In port-config.html, after port group created, if I change the group name in one port, the ports in same port group should all be updated with the new group name

In submodule-config.html, similar to the port-config, I would like a table to show all the submodule. all the submodule by defauled is selected. this table also support "shift" and "ctrl" key for advanced selection, remember the selected submodule in global variables for future processing in gererate drawio page.

In app.py, it should support route: `/get_submodules?filename=${filename}`, I would like to reuse the parse_verilog(filepath) in get_ports, it should have the submodule information