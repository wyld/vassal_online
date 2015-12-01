import base64
import hashlib
from lxml import etree
import os
import shutil
import uuid
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
                metadata['_id'] = module_hash = str(uuid.uuid5(
                    uuid.NAMESPACE_DNS, build_file_content.decode('utf-8')))
                temporary_module_path = module_path = os.path.join(
                    settings.MODULES_DIR, module_hash)

                while os.path.exists(temporary_module_path):
                    temporary_module_path += '_'

                os.makedirs(temporary_module_path)
                for item in zipped_module.infolist():
                    output_filename = os.path.join(
                        temporary_module_path, item.filename)
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

                if temporary_module_path != module_path:
                    shutil.rmtree(module_path)
                    shutil.move(temporary_module_path, module_path)
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
