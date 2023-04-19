from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in kaufland_integration/__init__.py
from kaufland_integration import __version__ as version

setup(
	name="kaufland_integration",
	version=version,
	description="Integration with Kaufland interface",
	author="ErpTech",
	author_email="maciej.miskiewicz@erptech.pl",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
