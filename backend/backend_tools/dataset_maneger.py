from os import listdir, path
import json

# Consts
UPLOAD_FOLDER = 'Datasets'
FRONTEND_DATASETS = '../frontend/static/Datasets/'
FRONTEND_CMS = '../frontend/static/CMs/'
STATIC_FOLDER = '../frontend/dist/static'
TEMPLATE_FOLDER = '../frontend/dist'
MIN = 1
MAX = 99999999

####


def get_dataset_number():
    from os import listdir

    count = 1
    for dir_name in listdir(UPLOAD_FOLDER):
        if 'dataset' in dir_name:
            count += 1
    return str(count)


def create_dataset(imgs_path, tags):
    images = listdir(imgs_path)
    dataset = {'images': []}
    uri_firname = 'static/Datasets/{}'.format(imgs_path.split('Datasets/')[-1])
    tags = [{"checked": False,
             "label": tag} for tag in tags]
    for img in images:
        dataset['images'].append({"uri": [path.normpath(uri_firname + img)], "tags": tags})
    dst_path = path.dirname(imgs_path) if imgs_path[-1] != '/' else path.dirname(path.dirname(imgs_path))
    with open('{}/dataset.json'.format(dst_path), 'w') as outfile:
        json.dump(dataset, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def get_dataset_data(dataset_name):
    return json.load(open(UPLOAD_FOLDER + '/' + dataset_name + '/dataset.json'))
