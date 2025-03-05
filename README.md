# Verilog to DrawIO Converter

A tool that converts Verilog modules to DrawIO diagrams, with both command-line and web interface support.

## Features

- Converts Verilog modules to DrawIO diagrams
- Supports port grouping
- Handles submodule connections
- Command-line interface for direct conversion
- Web interface for interactive diagram generation
- Real-time diagram preview
- Download generated diagrams
- Accurate Verilog parsing using hdlparse

## Installation

1. Clone the repository with submodules:
```bash
git clone --recursive https://github.com/weshu/verilog2drawio.git
cd verilog2drawio
```

If you've already cloned the repository without submodules, run:
```bash
git submodule update --init --recursive
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Convert a Verilog file to DrawIO:
```bash
python verilog2drawio.py path/to/your/module.v
```

The generated DrawIO file will be saved in the `downloads` directory.

### Web Interface

1. Start the Flask web server:
```bash
python app.py
```
2. Open your web browser and navigate to: http://localhost:5000
3. Upload your Verilog file through the web interface
4. View the generated diagram
5. Download the DrawIO file

## Project Structure

```
verilog2drawio/
├── app.py                 # Flask web application
├── generate_drawio.py     # Core diagram generation logic
├── draw_main_module.py    # Main module drawing functions
├── draw_submodules.py     # Submodule drawing functions
├── draw_connections.py    # Connection drawing functions
├── parse_verilog.py       # Verilog parsing functions
├── hdlparse/              # hdlparse submodule for Verilog parsing
├── static/                # Static web files
│   ├── css/
│   └── js/
├── templates/             # HTML templates
└── downloads/             # Generated DrawIO files
```

## Dependencies

- Python 3.x
- Flask

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

