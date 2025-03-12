from setuptools import setup, find_packages

setup(
    name="prtls_emailer",
    version="0.1.13",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "asgiref==3.7.2",
        "Django==4.2.20",
        "djangorestframework==3.15.2",
        "packaging==24.2",
        "prtls-utils @ git+https://github.com/protellus/prtls-utils.git@main",
        "pytz==2023.3",
        "sqlparse==0.5.0",
        "tzdata==2025.1",
    ],
)
