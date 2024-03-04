import logging
import logging.config
import os
import shutil
import subprocess
import json
from pathlib import Path

from exqudens.doxygen.xml2json import Xml2Json


class TestXml2Json:
    """
    Class TestXml2Json.
    """
    __logger = logging.getLogger('.'.join([__name__, __qualname__]))

    @classmethod
    def setup_class(cls):
        """
        Setup class.
        """
        try:
            logging.config.dictConfig({
                'version': 1,
                'incremental': True,
                'loggers': {
                    f"{Xml2Json.get_logger_name()}": {'level': logging.getLevelName(logging.DEBUG)},
                    f"{cls.__logger.name}": {'level': logging.getLevelName(logging.INFO)}
                }
            })
        except Exception as e:
            cls.__logger.info(e, exc_info=True)
            raise e

    def test_11(self):
        """
        Test 11.
        """
        try:
            exit_code = Xml2Json.main([
                'app.py',
                '--version',
                '--verbose'
            ])

            assert exit_code == 0
        except Exception as e:
            self.__logger.error(e, exc_info=True)

    def test_21(self):
        """
        Test 21.
        """
        try:
            project_dir = Path(__file__).parent.parent.parent.parent
            self.__logger.info(f"project_dir: '{project_dir}'")
            test_path_elements = [__name__, __class__.__name__, 'test_1']
            self.__logger.info(f"test_path_elements: '{test_path_elements}'")
            resource_dir = Path(project_dir).joinpath(
                'src',
                'test',
                'resources',
                '/'.join(test_path_elements)
            )
            self.__logger.info(f"resource_dir: '{resource_dir}'")
            test_build_dir = Path(project_dir).joinpath('build', 'test', '/'.join(test_path_elements))
            self.__logger.info(f"test_build_dir: '{test_build_dir}'")

            if Path(test_build_dir).exists():
                shutil.rmtree(test_build_dir)

            Path(test_build_dir).mkdir(parents=True)

            doxy_file = '/'.join(Path(resource_dir).joinpath('c-doxyfile.txt').relative_to(project_dir).parts)
            self.__logger.info(f"doxy_file: '{doxy_file}'")

            subprocess.run(['doxygen', doxy_file], check=True)

            xml_file = str(os.path.normpath(Path(test_build_dir).joinpath('xml', 'index.xml')))
            self.__logger.info(f"index_xml_file: '{xml_file}'")

            output_dir = str(os.path.normpath(Path(xml_file).parent.parent.joinpath('json')))
            self.__logger.info(f"output_dir: {output_dir}")

            exit_code = Xml2Json.main([
                'app.py',
                '--verbose',
                '--xml-file', xml_file,
                '--output-dir', output_dir,
                '--parallel', '8'
            ])

            assert exit_code == 0
        except Exception as e:
            self.__logger.error(e, exc_info=True)

    def test_22(self):
        """
        Test 22.
        """
        try:
            project_dir = Path(__file__).parent.parent.parent.parent
            self.__logger.info(f"project_dir: '{project_dir}'")
            test_path_elements = [__name__, __class__.__name__, 'test_1']
            self.__logger.info(f"test_path_elements: '{test_path_elements}'")
            resource_dir = Path(project_dir).joinpath(
                'src',
                'test',
                'resources',
                '/'.join(test_path_elements)
            )
            self.__logger.info(f"resource_dir: '{resource_dir}'")
            test_build_dir = Path(project_dir).joinpath('build', 'test', '/'.join(test_path_elements))
            self.__logger.info(f"test_build_dir: '{test_build_dir}'")

            if Path(test_build_dir).joinpath('json').exists():
                shutil.rmtree(Path(test_build_dir).joinpath('json'))

            config_json_file = str(os.path.normpath(Path(resource_dir).joinpath('config.json')))
            self.__logger.info(f"config_json_file: '{config_json_file}'")
            config_json = json.loads(Path(config_json_file).read_text())
            self.__logger.info(f"config_json_file: '{config_json is not None}'")

            xml_file = config_json['xml_file']
            if len(config_json['xml_file_prefix']) != 0:
                xml_file = str(os.path.normpath(Path(config_json['xml_file_prefix']).joinpath(xml_file)))
            else:
                xml_file = str(os.path.normpath(Path(project_dir).joinpath('build', 'test', '/'.join(test_path_elements), xml_file)))
            self.__logger.info(f"xml_file: '{xml_file}'")

            output_dir = str(os.path.normpath(Path(xml_file).parent.parent.joinpath('json')))
            self.__logger.info(f"output_dir: {output_dir}")

            exit_code = Xml2Json.main([
                'app.py',
                '--verbose',
                '--xml-file', xml_file,
                '--parallel', '8',
                '--parallel-type', 'process'
            ])

            assert exit_code == 0
        except Exception as e:
            self.__logger.error(e, exc_info=True)
