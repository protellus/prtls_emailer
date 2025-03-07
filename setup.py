from setuptools import setup, find_packages

setup(
    name="emailer",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=3.2",
        "requests",
        "html2text",
        "putils @ git+https://github.com/protellus/putils.git@main",
    ],
)
