from setuptools import setup, find_packages

setup(
    name="prtls_emailer",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
    install_requires=[
        "asgiref==3.7.2",
        "certifi==2025.1.31",
        "charset-normalizer==3.4.1",
        "Django>=4.2.20,<5.1.7",
        "djangorestframework==3.14.0",
        "html2text==2024.2.26",
        "idna==3.10",
        "packaging==24.2",
        "prtls-utils @ git+https://github.com/protellus/prtls-utils.git@main",
        "pytz==2023.3",
        "requests==2.32.0",
        "setuptools-scm==8.2.0",
        "sqlparse==0.4.4",
        "tzdata==2025.1",
        "urllib3==2.3.0"
    ],
)