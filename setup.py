from setuptools import setup, find_packages

setup(
    name="emailer",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "asgiref==3.7.2"
        "Django==3.2"
        "packaging==24.2"
        "pytz==2025.1"
        "sqlparse==0.4.4"
        "tzdata==2025.1"
    ],
)