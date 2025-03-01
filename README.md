# Verilog 到 Drawio 转换工具

## 简介
本项目是一个 Python 工具，用于读取 Verilog 文件并将其中的模块信息转换为 Drawio 格式的文件。对于 Verilog 文件中的每个模块，会生成一个对应的 Drawio 文件，文件中模块以方框表示，方框左右两侧显示其输入输出端口（包括 `input`、`output` 和 `inout`），方框内部展示该模块调用的子模块，子模块也带有相应的输入输出端口。若模块的输入输出端口与子模块的输入输出端口直接相连，会在 Drawio 文件中绘制连线信息；若不直接相连，则不绘制。模块内部的逻辑部分会被省略。

## 项目结构
```plaintext
.
├── verilog2drawio.py
├── parse_verilog.py
├── generate_drawio.py
└── README.md
```
- `verilog2drawio.py`：主程序文件，负责协调 Verilog 文件的解析和 Drawio 文件的生成。
- `parse_verilog.py`：用于读取和解析 Verilog 文件，提取模块、端口、子模块和连接信息。
- `generate_drawio.py`：根据解析得到的模块信息生成 Drawio XML 文件。
- `README.md`：项目说明文档。

## 安装与依赖
本项目仅依赖 Python 标准库，无需额外安装其他依赖项。确保你已经安装了 Python 3.x 环境。

## 使用方法

### 生成 Drawio 文件
在命令行中运行以下命令：
```sh
python verilog2drawio.py your_verilog_file.v
```
其中 `your_verilog_file.v` 是你要处理的 Verilog 文件的路径。运行后，会为 Verilog 文件中的每个模块生成一个对应的 `.drawio` 文件。

### 运行单元测试
在命令行中运行以下命令：
```sh
python verilog2drawio.py --test
```
该命令会执行 `parse_verilog.py` 和 `generate_drawio.py` 中的单元测试，验证解析和生成功能的正确性。

## 代码实现细节

### `parse_verilog.py`
- **全局正则表达式模式**：定义了 `module_pattern`、`port_pattern`、`submodule_pattern` 和 `connection_pattern`，用于匹配 Verilog 文件中的模块、端口、子模块和连接信息。
- **`parse_verilog` 函数**：读取 Verilog 文件，使用正则表达式提取模块信息，并返回一个字典，字典的键为模块名，值为包含端口信息、子模块信息和连接信息的元组。
- **单元测试**：包含 `TestParseVerilog` 类，用于测试 `parse_verilog` 函数的基本功能。

### `generate_drawio.py`
- **`generate_drawio` 函数**：根据模块信息生成 Drawio XML 文件，包括主模块方框、端口、子模块和连线信息，并将其保存为 `.drawio` 文件。
- **单元测试**：包含 `TestGenerateDrawio` 类，用于测试 `generate_drawio` 函数是否能生成 Drawio 文件。

### `verilog2drawio.py`
- **`main` 函数**：调用 `parse_verilog` 解析 Verilog 文件，然后调用 `generate_drawio` 为每个模块生成 Drawio 文件。
- **运行模式**：支持两种运行模式，传入 Verilog 文件路径时正常生成 Drawio 文件，传入 `--test` 参数时运行单元测试。

## 注意事项
- 本项目使用正则表达式解析 Verilog 文件，对于复杂的 Verilog 语法可能存在局限性。如果需要处理更复杂的文件，建议使用专门的 Verilog 解析库，如 `pyverilog`。
- Drawio 文件的布局和样式可以在 `generate_drawio.py` 文件中根据需要进行调整。

## 贡献
如果你发现任何问题或有改进建议，欢迎提交 Issues 或 Pull Requests。
