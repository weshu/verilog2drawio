from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, session
import os
from werkzeug.utils import secure_filename
from generate_drawio import generate_drawio
from functools import lru_cache
import json
from parse_verilog import parse_verilog

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'v', 'sv'}  # Allow Verilog and SystemVerilog files
app.secret_key = 'your-secret-key-here'  # Required for session

# Ensure upload and download directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@lru_cache(maxsize=32)
def get_parsed_verilog(filepath):
    """Cache the parse_verilog results for each file"""
    return parse_verilog(filepath)

def get_module_info(filename):
    """Get module information from cache or parse file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        modules = get_parsed_verilog(filepath)
        
        if not modules:
            return None, 'No modules found in the file'
        
        return modules[0], None  # Return first module and no error
    except Exception as e:
        return None, str(e)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    filename = request.args.get('filename')
    return render_template('index.html', filename=filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    
    if not file.filename.endswith('.v'):
        return jsonify({'success': False, 'error': 'File must be a Verilog file (.v)'})
    
    try:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse the Verilog file
        parsed_data = parse_verilog(filepath)
        if not parsed_data:
            return jsonify({'success': False, 'error': 'Failed to parse Verilog file'})
        
        # Save parsed data to JSON file
        json_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.json")
        with open(json_filepath, 'w') as f:
            json.dump(parsed_data, f)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'File uploaded and parsed successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/parse/<filename>')
def parse(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with open(filepath, 'r') as file:
            file_content = file.read()  # 读取文件内容
        return render_template('parse.html', filename=filename, file_content=file_content)
    except Exception as e:
        return f"Error reading file: {str(e)}", 500

@app.route('/get_ports/<filename>')
def get_ports(filename):
    try:
        json_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.json")
        with open(json_filepath, 'r') as f:
            parsed_data = json.load(f)
        
        if not parsed_data or len(parsed_data) == 0:
            return jsonify({'success': False, 'error': 'No modules found in the file'})
        
        module = parsed_data[0]
        return jsonify({
            'success': True,
            'ports': module['ports']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_submodules/<filename>')
def get_submodules(filename):
    try:
        json_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.json")
        with open(json_filepath, 'r') as f:
            parsed_data = json.load(f)
        
        if not parsed_data or len(parsed_data) == 0:
            return jsonify({'success': False, 'error': 'No modules found in the file'})
        
        module = parsed_data[0]
        return jsonify({
            'success': True,
            'submodules': module['submodules']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/group_ports', methods=['POST'])
def group_ports():
    # Handle port grouping logic
    grouped_ports = request.form.getlist('grouped_ports')
    # Save grouped ports to session or database
    return redirect(url_for('parse', filename=request.form['filename']))

@app.route('/select_submodules', methods=['POST'])
def select_submodules():
    # Handle submodule selection logic
    selected_submodules = request.form.getlist('selected_submodules')
    # Save selected submodules to session or database
    return redirect(url_for('parse', filename=request.form['filename']))

@app.route('/save_submodules', methods=['POST'])
def save_submodules():
    data = request.json
    # Store selected submodules in session
    session['selected_submodules'] = data.get('submodules', [])
    return jsonify({'success': True})

@app.route('/get_groups')
def get_groups():
    # Get port groups from session
    groups = session.get('port_groups', [])
    return jsonify({'groups': groups})

@app.route('/get_selected_submodules')
def get_selected_submodules():
    # Get selected submodules from session
    submodules = session.get('selected_submodules', [])
    return jsonify({'submodules': submodules})

@app.route('/generate_drawio', methods=['POST'])
def generate_drawio_endpoint():
    try:
        data = request.get_json()
        filename = data.get('filename')
        if not filename:
            return jsonify({'success': False, 'error': 'No filename provided'})
        
        json_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.json")
        with open(json_filepath, 'r') as f:
            parsed_data = json.load(f)
        
        if not parsed_data or len(parsed_data) == 0:
            return jsonify({'success': False, 'error': 'No modules found in the file'})
        
        module_data = parsed_data[0]
        if not isinstance(module_data, dict):
            return jsonify({'success': False, 'error': f'Invalid module data structure: {type(module_data)}'})
        
        required_fields = ['name', 'ports', 'submodules']
        for field in required_fields:
            if field not in module_data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'})
        
        drawio_filename = filename.replace('.v', '.drawio')
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], drawio_filename)
        
        port_groups = data.get('port_groups', [])
        if port_groups:
            for group in port_groups:
                if not isinstance(group, dict) or 'name' not in group or 'ports' not in group:
                    return jsonify({'success': False, 'error': 'Invalid port group structure'})
                if not isinstance(group['ports'], list):
                    return jsonify({'success': False, 'error': 'Ports must be a list in each group'})
        
        drawio_path = generate_drawio(
            module_data['name'],
            module_data['ports'],
            module_data['submodules'],
            [],  # No connections for web version
            port_groups,
            output_path
        )
        
        if drawio_path:
            return jsonify({
                'success': True, 
                'drawio_file': drawio_filename,
                'download_url': f'/downloads/{drawio_filename}'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to generate DrawIO file'})
            
    except Exception as e:
        import traceback
        print(f"Error in generate_drawio_endpoint: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/save_groups', methods=['POST'])
def save_groups():
    data = request.json
    # Store port groups in session
    session['port_groups'] = data.get('groups', [])
    return jsonify({'success': True})

@app.route('/get_independent_ports/<filename>', methods=['GET', 'POST'])
def get_independent_ports(filename):
    try:
        json_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.json")
        with open(json_filepath, 'r') as f:
            parsed_data = json.load(f)
        
        if not parsed_data or len(parsed_data) == 0:
            return jsonify({'success': False, 'error': 'No modules found in the file'})
        
        module = parsed_data[0]
        all_ports = module['ports']
        
        # Get port groups from request
        if request.method == 'POST':
            port_groups = request.json.get('port_groups', [])
        else:
            port_groups = request.args.get('port_groups', '[]')
            try:
                port_groups = json.loads(port_groups)
            except json.JSONDecodeError:
                port_groups = []
        
        # Get all ports that are in groups
        grouped_ports = set()
        for group in port_groups:
            grouped_ports.update(port['name'] for port in group['ports'])
        
        # Filter out ports that are not in any group
        independent_ports = [port for port in all_ports if port['name'] not in grouped_ports]
        
        return jsonify({
            'success': True,
            'independent_ports': independent_ports
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(app.config['DOWNLOAD_FOLDER'], filename),
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True)