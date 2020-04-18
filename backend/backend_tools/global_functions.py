from os import listdir

# TODO: make me global in backend_tools
components_root_path = '/usr/local/ge/opt/'


def check_report_state(path):
    if 'report.html' in listdir(path):
        return 'Yes'
    return 'No'


def report_state(path):
    if 'report.html' in listdir(path):
        with open('{}/report.html'.format(path), 'r') as f:
            if 'Pass' in f.readline():
                return 'Pass'
            return 'Unstable'
    return '---'


def report_link(path):
    if 'report.html' in listdir(path):
        return '{}/report.html'.format(path)
    return ''


def load_from_filter_block(block_index, filter_block):
    block_data = {block_index: {}}
    for inner_block, inner_block_value in filter_block.items():
        for filter_option_name, filter_option_tuple in inner_block_value.items():
            if filter_option_name != 'visible':
                for i in range(len(filter_option_tuple)):
                    if filter_option_tuple[i]['value']:
                        if inner_block == 'Include':
                            if 'inc' not in block_data[block_index]:
                                block_data[block_index]['inc'] = []
                            if filter_option_name == 'CaseID':
                                block_data[block_index]['inc'].append('caseID{}{}'.format(filter_option_tuple[i]['operator'], filter_option_tuple[i]['value']))
                            elif filter_option_name == 'VersionNumber':
                                pass
                            elif filter_option_name == 'YamlCaseID':
                                pass
                            elif filter_option_name == 'Other':
                                block_data[block_index]['inc'].append(filter_option_tuple[i]['value'])
                        elif inner_block == 'Exclude':
                            if 'exc' not in block_data[block_index]:
                                block_data[block_index]['exc'] = []
                            if filter_option_name == 'CaseID':
                                block_data[block_index]['exc'].append('caseID{}{}'.format(filter_option_tuple[i]['operator'], filter_option_tuple[i]['value']))
                            elif filter_option_name == 'VersionNumber':
                                pass
                            elif filter_option_name == 'YamlCaseID':
                                pass
                            elif filter_option_name == 'Other':
                                block_data[block_index]['exc'].append(filter_option_tuple[i]['value'])
                        elif inner_block == 'Multiply':
                            if 'mult' not in block_data[block_index]:
                                block_data[block_index]['mult'] = []
                            if filter_option_name == 'CaseID':
                                block_data[block_index]['mult'].append('caseID{}{}'.format(filter_option_tuple[i]['operator'], filter_option_tuple[i]['value']))
                            elif filter_option_name == 'VersionNumber':
                                pass
                            elif filter_option_name == 'YamlCaseID':
                                pass
                            elif filter_option_name == 'Other':
                                block_data[block_index]['mult'].append(filter_option_tuple[i]['value'])
    return block_data


def generate_regression_property_file(request_data, output_path):
    import json
    import yaml
    from datetime import datetime

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        component_name = request_data['componentName']
        golden_version = request_data['goldenVersion']
        candidate_version = request_data['candidateVersion']
        debug_level = request_data['debugLevel']
        filter_blocks_data = json.loads(request_data['filterBlocks'])

        file_path = '{}/{}_{}_{}.yml'.format(output_path, 'regression', component_name, timestamp)
        property_data = {}

        golden_sep = '_' if golden_version == 'be' or golden_version == 'rc' else '-'
        candidate_sep = '_' if candidate_version == 'be' or candidate_version == 'rc' else '-'
        property_data['released_execute'] = '{0}/{1}{2}{3}/bin/{1}'.format(components_root_path, component_name,
                                                                           golden_sep, golden_version)
        property_data['candidate_execute'] = '{0}/{1}{2}{3}/bin/{1}'.format(components_root_path, component_name,
                                                                            candidate_sep, candidate_version)
        property_data['debug_level'] = debug_level

        filters = []
        for block_index, filter_block in filter_blocks_data.items():
            filters.append(load_from_filter_block(int(block_index), filter_block))

        property_data['filters'] = filters

        with open(file_path, 'w') as property_file:
            yaml.dump(property_data, property_file, default_flow_style=False)

        # TODO: add all regression components
    except Exception as e:
        return 1, str(e)

    return 0, 'Success'
