from pathlib import Path

SERVER_RUNNING_BANNER = """
+----------------------------------------+
|             SERVER WORKS!              |
+----------------------------------------+

Visit http://{host}:{port}

..........................................
"""

_this_file_path = Path(__file__).resolve()

DIR_FRAMEWORK = _this_file_path.parent.resolve()

DIR_SRC = DIR_FRAMEWORK.parent.resolve()
DIR_STATIC = (DIR_SRC / "static").resolve()
