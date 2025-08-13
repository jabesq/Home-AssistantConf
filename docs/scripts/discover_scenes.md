### discover_scenes.py

**Purpose**: Discover and print Philips Hue Groups and Scenes using the `phue` library.

- **File**: `discover_scenes.py`
- **Functions**: `getargs()`, `discover()`

### Requirements

- Python package: `phue`

Install:

```bash
pip install phue
```

### Usage

```bash
python discover_scenes.py /path/to/hue.conf
```

- The config path points to your `phue` configuration file (often `~/.python_hue`).
- The script connects to the bridge, then prints:
  - "List of Groups" followed by the group objects
  - "List of Scenes" followed by the scene objects

Example output is verbose pretty-printed structures via Python's `pprint`.