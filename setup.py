from setuptools import setup, find_packages

setup(
    name="prtls_emailer",
    version="0.1.7",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "asgiref==3.7.2",
        "Django==3.2",
        "djangorestframework==3.14.0",
        "packaging==24.2",
        "prtls_utils @ git+https://github.com/protellus/prtls-utils.git@main",
        "pytz==2023.3",
        "sqlparse==0.4.4",
        "tzdata==2025.1",
    ],
)
