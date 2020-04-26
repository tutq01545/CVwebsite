import yaml


def read_yaml_from_file(file_path):
    try:
        file = open(file_path)
    except IOError as e:
        print(e)
        file = None

    if file:
        data = yaml.full_load(file)
        return data
    else:
        return None

