#!/usr/bin/env python3
"""Setup configuration for t2v package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="t2v",
    version="0.1.0",
    author="T2V Development Team",
    author_email="dev@t2v.com",
    description="T2V - A private repository project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private/t2v",
    project_urls={
        "Bug Tracker": "https://github.com/private/t2v/issues",
        "Documentation": "https://github.com/private/t2v/docs",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "t2v=t2v.cli:main",
        ],
    },
)