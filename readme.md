# exqudens-py-doxygen-xml2json

### Doxygen

- make dir `build/doxygen/c` run `mkdir -p build/doxygen/c`
- run `doxygen src/test/resources/TestXml2Json/test_1/Doxyfile`

### Hatch

- install pip `<venv-python> -m pip install hatch==1.9.3`
- set env var `HATCH_DATA_DIR` to `build/hatch/data-dir`
- set env var `HATCH_CACHE_DIR` to `build/hatch/cache-dir`

##### How To Clean

```
git clean -xdf -e .idea -e tmp
```

##### How To Build

```
hatch build
```

##### How To Build Executable

```
hatch run installer:pyinstaller --clean --onefile --name doxygen-xml2json src/main/py/exqudens/doxygen/xml2json.py
hatch run installer:pyinstaller --clean --contents-directory doxygen-xml2json --name doxygen-xml2json src/main/py/exqudens/doxygen/xml2json.py
```

##### How To Test

```
hatch run test:pytest -q --collect-only
hatch run test:pytest --log-cli-level=DEBUG src/test/py/test_xml2json.py::TestXml2Json::test_11
```

##### How To Test Wheel

```
hatch env prune
hatch clean
hatch build
hatch run wtest:pytest -q --collect-only
hatch run wtest:pytest --log-cli-level=INFO src/test/py
```
