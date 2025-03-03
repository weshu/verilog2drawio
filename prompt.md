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