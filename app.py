from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, session
import os
from werkzeug.utils import secure_filename
from verilog2drawio import parse_verilog, generate_drawio
from functools import lru_cache

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['DOWNLOAD_FOLDER'] = 'downloads/'  # Add downloads folder configuration
app.config['ALLOWED_EXTENSIONS'] = {'v', 'vh'}
app.secret_key = 'your-secret-key-here'  # Required for session

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
    filename = request.args.get('filename', None)  # 获取文件名参数
    return render_template('index.html', filename=filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            # Clear the cache for this file if it exists
            get_parsed_verilog.cache_clear()
            return jsonify({'success': True, 'filename': filename}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/parse/<filename>')
def parse(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with open(filepath, 'r') as file:
            file_content = file.read()  # 读取文件内容
        return render_template('parse.html', filename=filename, file_content=file_content)
    except Exception as e:
        return f"Error reading file: {str(e)}", 500

@app.route('/get_ports')
def get_ports():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    module, error = get_module_info(filename)
    if error:
        return jsonify({'error': error}), 404 if 'No modules found' in error else 500

    ports = module[1]  # Extract port information
    return jsonify({'ports': ports})

@app.route('/get_submodules')
def get_submodules():
    filename = request.args.get('filename')
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    module, error = get_module_info(filename)
    
    if error:
        return jsonify({'error': error}), 404 if 'No modules found' in error else 500

    submodules = module[2] if len(module) > 2 else []  # Extract submodule information
    
    formatted_submodules = [
        {'name': submodule_type, 'instance': submodule_name}
        for submodule_type, submodule_name in submodules
    ]
    
    return jsonify({'submodules': formatted_submodules})

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

@app.route('/generate/<filename>', methods=['POST'])
def generate(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    data = request.json
    
    # Get port groups, submodules, and ports from request data
    port_groups = data.get('port_groups', [])
    selected_submodules = data.get('submodules', [])
    ports = data.get('ports', [])  # Get all ports information
    
    # Get module info to extract connections
    module, error = get_module_info(filename)
    if error:
        return jsonify({'error': error}), 404 if 'No modules found' in error else 500
    
    # Extract connections from module data
    connections = module[3] if len(module) > 3 else []  # Connections are the fourth element
    
    try:
        # Generate DrawIO XML and get the file path
        file_path = generate_drawio(filename, ports, selected_submodules, connections)
        
        if file_path is None:
            return jsonify({'error': 'Failed to generate DrawIO file'}), 500
            
        # Return the file path for download
        return jsonify({'file_path': file_path})
    except Exception as e:
        print(f"Error generating DrawIO: {str(e)}")
        return jsonify({'error': f'Failed to generate DrawIO: {str(e)}'}), 500

@app.route('/save_groups', methods=['POST'])
def save_groups():
    data = request.json
    # Store port groups in session
    session['port_groups'] = data.get('groups', [])
    return jsonify({'success': True})

@app.route('/get_independent_ports')
def get_independent_ports():
    filename = request.args.get('filename')
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    module, error = get_module_info(filename)
    if error:
        return jsonify({'error': error}), 404 if 'No modules found' in error else 500

    # Get all ports from the module
    all_ports = module[1]  # Extract port information
    
    # Get port groups from session
    port_groups = session.get('port_groups', [])
    
    # Get all ports that are in groups
    grouped_ports = set()
    for group in port_groups:
        grouped_ports.update(port['name'] for port in group['ports'])
    
    # Find independent ports (ports not in any group)
    independent_ports = [
        port for port in all_ports
        if port['name'] not in grouped_ports
    ]
    
    return jsonify({'ports': independent_ports})

@app.route('/downloads/<filename>')
def download_file(filename):
    """Serve files from the downloads directory"""
    try:
        return send_file(
            os.path.join(app.config['DOWNLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)  # Create downloads directory
    app.run(debug=True, use_reloader=False)  # 禁用自动重载功能以避免 watchdog 兼容性问题