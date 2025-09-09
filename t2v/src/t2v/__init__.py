"""T2V - Private Repository Package

This is the main package for the T2V private repository project.
"""

__version__ = "0.1.0"
__author__ = "T2V Development Team"
__email__ = "dev@t2v.com"

# Main package imports
from .core import T2VCore
from .utils import T2VUtils

__all__ = [
    "T2VCore",
    "T2VUtils",
    "__version__",
    "__author__",
    "__email__",
]