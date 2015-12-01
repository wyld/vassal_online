import base64
import hashlib
from lxml import etree
import os
import zipfile

import settings
from utils.exceptions import ValidationError


BUILD_FILE_NAME = 'buildFile'
MODULE_DATA_FILE_NAME = 'moduledata'


class ModuleParser(object):
    def __init__(self, module_file):
        self.module_file = module_file

    def extract(self):
        metadata = {}

        try:
            with zipfile.ZipFile(self.module_file, 'r') as zipped_module:
                try:
                    build_file_content = zipped_module.read(BUILD_FILE_NAME)
                except KeyError:
                    raise ValidationError('Provided file is not a valid module')
                module_hash = base64.b32encode(hashlib.md5(build_file_content).digest()).decode('utf-8')
                module_path = os.path.join(settings.MODULES_DIR, module_hash)

                if os.path.exists(module_path):
                    raise ValidationError('Module is already uploaded')

                os.makedirs(module_path)
                for item in zipped_module.infolist():
                    output_filename = os.path.join(module_path, item.filename)
                    output_dirname = os.path.dirname(output_filename)
                    if not os.path.exists(output_dirname):
                        os.makedirs(output_dirname)

                    try:
                        input_content = zipped_module.read(item.filename)
                        with open(output_filename, 'wb') as output_file:
                            output_file.write(input_content)
                    except IsADirectoryError:
                        pass

                    if item.filename == MODULE_DATA_FILE_NAME:
                        parser = ModuleDataFileParser(input_content)
                        metadata.update(parser.parse())
        except zipfile.BadZipFile:
            raise ValidationError('Provided file is not a valid module')

        return metadata


class ModuleDataFileParser(object):
    def __init__(self, module_data):
        self.et = etree.fromstring(module_data)

    def parse(self):
        parsed_data = {
            'version': self.et.find('./version').text,
            'title': self.et.find('./name').text,
            'description': self.et.find('./description').text}
        return parsed_data
