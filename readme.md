# exqudens-py-doxygen-xml2json

### Doxygen

- make dir `build/doxygen/c` run `mkdir -p build/doxygen/c`
- run `doxygen src/test/resources/TestXml2Json/test_1/Doxyfile`

### Hatch

- set env var `HATCH_DATA_DIR` to `build/hatch/data-dir`
- set env var `HATCH_CACHE_DIR` to `build/hatch/cache-dir`

##### How To Build

```
hatch build
```

##### How To Executable

```
hatch run installer:pyinstaller --clean --onefile --name exqudens-doxygen-xml2json src/main/py/exqudens/doxygen/xml2json.py
```

##### How To Test

```
hatch run test:pytest -q --collect-only
hatch run test:pytest --log-cli-level=INFO src/test/py
```

##### How To Test Wheel

```
hatch env prune
hatch clean
hatch build
hatch run wtest:pytest -q --collect-only
hatch run wtest:pytest --log-cli-level=INFO src/test/py
```
