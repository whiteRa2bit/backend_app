from setuptools import setup, find_packages

from pathlib import Path
from pkg_resources import parse_requirements

import mafia_resources


def _get_requirements():
    with (Path(__file__).parent / 'requirements.txt').open() as fp:
        return [str(requirement) for requirement in parse_requirements(fp)]


setup(
    name='mafia_resources',
    version=mafia_resources.__version__,
    description='Mafia resources service',
    license="MIT",
    author='Pavel Fakanov',
    author_email='pavel.fakanov@gmail.com',
    packages=find_packages(),
    install_requires=_get_requirements()
)
