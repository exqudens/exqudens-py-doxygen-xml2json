import logging
import inspect
import json
import sys
from pathlib import Path
from typing import Any
from enum import Enum
from argparse import ArgumentParser

import doxmlparser


class Xml2Json:
    """
    Class Xml2Json.
    """
    __logger = logging.getLogger('.'.join([__name__, __qualname__]))

    @classmethod
    def set_logger_level(cls, level=logging.DEBUG):
        try:
            cls.__logger.setLevel(level)
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def get_logger_name(cls):
        try:
            return cls.__logger.name
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def main(cls, arguments: list[str]) -> int:
        try:
            parser = ArgumentParser()
            parser.add_argument('--xml-file', type=str, required=True)
            parser.add_argument('--output-dir', type=str, required=True)
            parser.add_argument('--indent', type=int, default=4, help='default: 4')
            parser.add_argument('--silence', type=bool, default=True, help='default: True')
            parser.add_argument('--warnings', type=bool, default=True, help='default: True')
            parser.add_argument('--xml-type', type=str, default='all', help='default: all', choices=['all', 'index', 'compound'])

            args = parser.parse_args(arguments[1:])

            cls.__logger.debug(f"args.xml_file: '{args.xml_file}' ({type(args.xml_file)})")
            cls.__logger.debug(f"args.output_dir: '{args.output_dir}' ({type(args.output_dir)})")
            cls.__logger.debug(f"args.indent: '{args.indent}' ({type(args.indent)})")
            cls.__logger.debug(f"args.silence: '{args.silence}' ({type(args.silence)})")
            cls.__logger.debug(f"args.warnings: '{args.warnings}' ({type(args.warnings)})")
            cls.__logger.debug(f"args.xml_type: '{args.xml_type}' ({type(args.xml_type)})")

            cls.check_output_dir(args.output_dir)

            if args.xml_type == 'all':
                root_result = Xml2Json.transform(
                    xml_file=args.xml_file,
                    silence=args.silence,
                    warnings=args.warnings,
                    xml_type='index'
                )
                json_file = Path(args.output_dir).joinpath(Path(args.xml_file).stem + '.json')
                json_str = json.dumps(root_result, indent=args.indent)

                Path(json_file).parent.mkdir(parents=True, exist_ok=True)
                Path(json_file).write_text(json_str)

                if len(root_result) == 0:
                    raise Exception(f"'root_result' is empty!")
                compound_dict = root_result[len(root_result) - 1]
                if len(compound_dict) < 2:
                    raise Exception(f"'compound_dict' too small!")
                for compound in compound_dict['compound']:
                    compound_xml_file_name = compound['refid'] + '.xml'
                    compound_xml_file = str(Path(args.xml_file).parent.joinpath(compound_xml_file_name))
                    compound_result = Xml2Json.transform(
                        xml_file=compound_xml_file,
                        silence=args.silence,
                        warnings=args.warnings,
                        xml_type='compound'
                    )
                    json_file = Path(args.output_dir).joinpath(Path(compound_xml_file_name).stem + '.json')
                    json_str = json.dumps(compound_result, indent=args.indent)
                    Path(json_file).parent.mkdir(parents=True, exist_ok=True)
                    Path(json_file).write_text(json_str)
            else:
                root_result = Xml2Json.transform(
                    xml_file=args.xml_file,
                    silence=args.silence,
                    warnings=args.warnings,
                    xml_type=args.xml_type
                )
                json_file = Path(args.output_dir).joinpath(Path(args.xml_file).stem + '.json')
                json_str = json.dumps(root_result, indent=args.indent)

                Path(json_file).parent.mkdir(parents=True, exist_ok=True)
                Path(json_file).write_text(json_str)

            return 0
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def transform(
            cls,
            xml_file: str,
            silence: bool = True,
            warnings: bool = True,
            xml_type: str = None
    ) -> list[dict[str, Any]]:
        """
        Main method.

        :param xml_file: XML file path string.
        :param silence: silence.
        :param warnings: print warnings.
        :param xml_type: XML file type string.

        :return: index JSON file path string.

        :raise Exception: on error.
        """
        try:
            if xml_type is None:
                if Path(xml_file).name == 'index.xml':
                    xml_type = 'index'
                else:
                    xml_type = 'compound'
            elif xml_type != 'index' and xml_type != 'compound':
                raise Exception(f"Unsupported 'xml_type': '{xml_type}'! Supported: ['index', 'compound']")

            if xml_type == 'index':
                return cls.transform_index(xml_file, silence, warnings)
            elif xml_type == 'compound':
                return cls.transform_compound(xml_file, silence, warnings)
            else:
                raise Exception(f"Unsupported 'xml_type': '{xml_type}'!")
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def check_xml_file(cls, xml_file: str) -> None:
        try:
            if xml_file is None:
                raise Exception(f"'xml_file' is None!")

            if len(xml_file) == 0:
                raise Exception(f"'xml_file' is empty!")

            if not Path(xml_file).exists():
                raise Exception(f"'xml_file' not exists!")
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def check_output_dir(cls, output_dir: str) -> None:
        try:
            if output_dir is None:
                raise Exception(f"'output_dir' is None!")

            if len(output_dir) == 0:
                raise Exception(f"'output_dir' is empty!")
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def transform_index(
            cls,
            xml_file: str,
            silence: bool = False,
            warnings: bool = False
    ) -> list[dict[str, Any]]:
        try:
            cls.check_xml_file(xml_file)

            root_xml = doxmlparser.index.parse(xml_file, silence=silence, print_warnings=warnings)

            root_result = cls.index_enum_dicts()
            root_result.append(cls.to_dict(root_xml))

            return root_result
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def transform_compound(
            cls,
            xml_file: str,
            silence: bool = False,
            warnings: bool = False
    ) -> list[dict[str, Any]]:
        try:
            cls.check_xml_file(xml_file)

            root_xml = doxmlparser.compound.parse(xml_file, silence=silence, print_warnings=warnings)

            root_result = cls.compound_enum_dicts()
            root_result.append(cls.to_dict(root_xml))

            return root_result
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def index_enum_dicts(cls) -> list[dict[str, Any]]:
        try:
            result = []

            members = inspect.getmembers(doxmlparser.index, predicate=inspect.isclass)
            for name, type_obj in members:
                type_obj: type = type_obj
                if type_obj.__module__ == 'doxmlparser.index' and issubclass(type_obj, Enum):
                    result_child_list = []
                    for entry in type_obj:
                        result_child_list.append(entry.value)
                    result_child = {type_obj.__name__: result_child_list}
                    result.append(result_child)

            return result
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def compound_enum_dicts(cls) -> list[dict[str, Any]]:
        try:
            result = []

            members = inspect.getmembers(doxmlparser.compound, predicate=inspect.isclass)
            for name, type_obj in members:
                type_obj: type = type_obj
                if type_obj.__module__ == 'doxmlparser.compound' and issubclass(type_obj, Enum):
                    result_child_list = []
                    for entry in type_obj:
                        result_child_list.append(entry.value)
                    result_child = {type_obj.__name__: result_child_list}
                    result.append(result_child)

            return result
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def to_dict(cls, obj) -> dict[str, Any]:
        try:
            if obj is None:
                raise Exception(f"'obj' is None!")

            if (
                    not isinstance(obj, doxmlparser.index.DoxygenType)
                    and not isinstance(obj, doxmlparser.compound.DoxygenType)
            ):
                raise Exception(f"Unsupported type: '{type(obj)}'!")

            return cls.__to_dict(obj)
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def __to_dict_is_doxmlparser_object(cls, obj) -> bool:
        try:
            if obj is None:
                raise Exception(f"'obj' is None!")

            obj_type = type(obj)

            if obj_type.__module__ == 'doxmlparser.index':
                if obj_type.__name__ in doxmlparser.index.__all__:
                    return True
            elif obj_type.__module__ == 'doxmlparser.compound':
                if obj_type.__name__ in doxmlparser.compound.__all__:
                    return True

            return False
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def __to_dict_method_key_names(cls, methods: list[tuple[str, Any]]) -> list[tuple[str, str]]:
        try:
            result = []

            for method_name, _ in methods:
                if method_name.startswith('get_') and not method_name.endswith('_'):
                    key_name = method_name.split('_', 1)[1]
                    result.append((method_name, key_name))
                elif method_name == 'get_valueOf_':
                    key_name = 'value'
                    result.append((method_name, key_name))

            return result
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def __to_dict(cls, obj) -> dict[str, Any] | None:
        try:
            if obj is None:
                return None

            if cls.__to_dict_is_doxmlparser_object(obj):
                result = {}
                methods = inspect.getmembers(obj, predicate=inspect.ismethod)
                method_key_names = cls.__to_dict_method_key_names(methods)
                for method_name, key in method_key_names:
                    value = getattr(obj, method_name)()
                    if value is not None:
                        if cls.__to_dict_is_doxmlparser_object(value):
                            value = cls.__to_dict(value)
                            result[key] = value
                        elif isinstance(value, list):
                            if len(value) > 0:
                                result_list = []
                                for o in value:
                                    result_list.append(cls.__to_dict(o))
                                value = result_list
                                result[key] = value
                        else:
                            result[key] = value
                return result

            return obj
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e


Xml2Json.set_logger_level(logging.INFO)

if __name__ == "__main__":
    argv = sys.argv
    ecode = Xml2Json.main(argv)
    sys.exit(ecode)
