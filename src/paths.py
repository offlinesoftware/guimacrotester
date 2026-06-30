'''
from pathlib import Path

class Paths:
    base = Path(__file__).parent
    icons = base / "../icons"
    debug = True

    # File loaders.
    @classmethod
    def icon(cls, filename):
        return (cls.icons / filename).as_posix()
'''

class Paths:
    debug = False

    @classmethod
    def icon(cls, filename):
        return f":/icons/{filename}"