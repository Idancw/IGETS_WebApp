from os.path import isdir, isfile, join
from re import findall
from random import *

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from backend_tools.dataset_evaluate import *
from backend_tools.dataset_maneger import *
from backend_tools.global_functions import *

app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            template_folder=TEMPLATE_FOLDER)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Globals # TODO: make me global in backend_tools
# regression_reports_root = '/data/GPC/examinations/regression/'
# components_root = '/usr/local/ge/opt/'
components_root = '/Users/idancw/PycharmProjects/IGETS_WebApp/backend/versions/'
regression_reports_root = '/Users/idancw/PycharmProjects/IGETS_WebApp/backend/'


@app.route('/api/upload/<upload_type>', methods=['POST'])
def upload(upload_type):
    if upload_type == 'upload_dataset':
        img_files = dict(request.files)['photos']
        dir_name = dict(request.form)['name'][0].replace(' ', '_')
        tags = [tag.strip() for tag in dict(request.form)['tags'][0].split(',')]
        if img_files:
            dst_path = '{}/{}/images/'.format(app.config['UPLOAD_FOLDER'], dir_name)
            try:
                makedirs(dst_path)
            except:
                return jsonify({'return': 1, 'msg': 'dataset name already exists'})
            for file in img_files:
                filename = secure_filename(file.filename)
                file.save(join(dst_path, filename))
            create_dataset(dst_path, tags)
        return jsonify({'return': 0, 'msg': 'Success'})
    elif upload_type == 'evaluate_dataset':
        print(dict(request.files)['Algo_dataset'])
        print(dict(request.form)['GT_dataset'])
        gt_dataset = dict(request.form)['GT_dataset']
        algo_dataset = dict(request.files)['Algo_dataset']
        print(gt_dataset)
        if not algo_dataset or gt_dataset == 'undefined':
            return jsonify({'return': 1, 'msg': 'No algorithm or GT dataset selected', 'result': ''})
        try:
            cm_table, detailed_table, images, accuracy, warnings = evaluate(get_dataset_data(gt_dataset), json.loads(
                algo_dataset.stream.read().decode('utf-8')))
            try:
                makedirs(FRONTEND_CMS)
            except:
                pass
            dst_path = '{}CM_{}.png'.format(FRONTEND_CMS, randint(MIN, MAX))
            copy_files(src_path='CM.png', dst_path=dst_path, move=True)
            dst_path = dst_path.split('../frontend/')[-1]
            return jsonify({'return': 0, 'msg': '', 'result': dst_path, 'table': cm_table,
                            'detailedTable': detailed_table, 'images': images, 'accuracy': accuracy,
                            'warnings': warnings})
        except Exception as error:
            print(repr(error))
            return jsonify({'return': 1, 'msg': repr(error), 'result': ''})


@app.route('/api/get_component_names')
def get_component_names():
    component_names = sorted(['ig_prep', 'gpc_recon', 'ig_crop'])  # listdir(PATH_TO_COMPONENTS)
    return jsonify({'return': 0, 'msg': 'success', 'result': component_names})


@app.route('/api/get_component_report/<component_name>')
def get_component_report(component_name):
    from os import listdir
    from os.path import isdir

    if not isdir('{}/{}'.format(regression_reports_root, component_name)):
        return jsonify('')
    report_dirs = listdir('{}/{}'.format(regression_reports_root, component_name))
    report_dirs_full = ['{}/{}/{}'.format(regression_reports_root, component_name, d) for d in listdir('{}/{}'.format(regression_reports_root, component_name))]

    report_table = {}
    for i in range(len(report_dirs)):
        report_table[i] = {}
    for i, d in enumerate(report_dirs):
        # Find versions of Golden and Candidate
        versions = findall('_(\d+\.\d+\.\d+)_', d)  # version string of Major.Minor.Patch
        versions += findall('_(\d+\.\d+\.\d+\.\d+)_', d)  # version string of Major.Minor.Patch.Private
        report_table[i]['Golden'] = versions[0]
        report_table[i]['Candidate'] = versions[1]
        report_time = d.split('_')[-1]
        report_table[i]['Time'] = '{}:{}:{}'.format(report_time[0:2], report_time[2:4], report_time[4:6])
        report_date = d.split('_')[-2]
        report_table[i]['Date'] = '{}-{}-{}'.format(report_date[0:4], report_date[4:6], report_date[6:8])
        report_table[i]['Completed'] = check_report_state(report_dirs_full[i])
        report_table[i]['State'] = report_state(report_dirs_full[i])
        report_table[i]['Report_link'] = report_link(report_dirs_full[i])
        report_table[i]['_full_path'] = report_dirs_full[i]

    return jsonify({'return': 0, 'msg': 'success', 'result': report_table})


@app.route('/api/run/<runner_name>', methods=['POST'])
def run_rets(runner_name):
    if runner_name == 'Regression':
        # TODO: change the path to currect one (where the prop file should be)
        return_val, return_msg = generate_regression_property_file(request.form, '/Users/idancw/PycharmProjects/IGETS_WebApp/backend/')
        return jsonify({'return': return_val, 'msg': return_msg, 'result': ''})
    return jsonify({'return': 0, 'msg': 'Nothing has been done', 'result': ''})


@app.route('/api/get_report_html/<report_path>')
def get_report_html(report_path):
    refactor_path = report_path.replace('!', '/')
    with open(refactor_path, 'r') as f:
        return jsonify({'return': 0, 'msg': 'success', 'result': f.read()})


@app.route('/api/get_component_versions/<component>')
def get_component_versions(component):
    from glob import glob

    component_dirs = glob('{}/{}-*'.format(components_root, component))
    versions = []
    for d in component_dirs:
        versions += findall('-(\d+\.\d+\.\d+)', d)  # version string of Major.Minor.Patch
        versions += findall('-(\d+\.\d+\.\d+\.\d+)', d)  # version string of Major.Minor.Patch.Private
    versions = sorted(list(set(versions)))
    versions.append('be')
    versions.append('rc')
    return jsonify({'return': 0, 'msg': 'success', 'result': versions})


@app.route('/api/getoptions')
def get_options():
    datasets = listdir(UPLOAD_FOLDER)
    response = {
        'options': datasets
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    import requests

    print(path)
    print(requests.get('http://localhost:8080/{}'.format(path)).text)
    print(requests.get('http://localhost:8080/{}'.format(path)))
    return requests.get('http://localhost:8080/{}'.format(path)).text


if __name__ == '__main__':
    app.run(debug=True)
