import json
import os
import shutil
import sys
from shutil import copyfile

import yaml
from jinja2 import FileSystemLoader, Environment

offering_yaml = str(sys.argv[1])
# offering_yaml = str("sample.yml")
working_dir = os.getcwd()


def run():
    with open(f"{offering_yaml}") as f:
        offering = yaml.safe_load(f)

    offering_name = offering['offering']

    # c. new folder is created under the snacks directory with the offering’s name value - {offering_name}
    try:
        shutil.rmtree(f'snacks/{offering_name}')
        os.makedirs(f'snacks/{offering_name}')
    except:
        print(f'\n-.- snacks/{offering_name} sub-dir already exists -.-')

    # d. variables.json is created and placed in the snacks/{offering_name} subdirectory
    env = Environment(loader=FileSystemLoader('templates'))
    v_template = env.get_template("variables.json.j2")
    variables_template = v_template.render(offering)
    text = "\n".join([ll.rstrip() for ll in variables_template.splitlines() if ll.strip()])

    jsonobj = json.loads(text)
    json_data = json.dumps(jsonobj, indent=2)
    with open(f'snacks/{offering_name}/variables.json', 'w') as outfile:
        print(json_data, file=outfile)
        # print(json.loads(json_data),file=outfile)

    copyfile(f'{offering_yaml}', f'snacks/{offering_name}/offering.yml')

    print(json_data)
    return offering_name


if __name__ == '__main__':
    run()
