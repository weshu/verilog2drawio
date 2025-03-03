from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, session
import os
from werkzeug.utils import secure_filename
from verilog2drawio import parse_verilog, generate_drawio
from functools import lru_cache

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
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

@app.route('/generate/<filename>', methods=['POST'])
def generate(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    port_groups = request.form.getlist('port_groups')
    selected_submodules = request.form.getlist('submodules')
    drawio_xml = generate_drawio(filepath, port_groups, selected_submodules)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.drawio')
    with open(output_path, 'w') as f:
        f.write(drawio_xml)
    return send_file(output_path, as_attachment=True)

@app.route('/save_groups', methods=['POST'])
def save_groups():
    data = request.json
    # 这里可以保存分组信息到数据库或 session
    return jsonify({'success': True})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, use_reloader=False)  # 禁用自动重载功能以避免 watchdog 兼容性问题