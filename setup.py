from setuptools import setup, find_packages

setup(
    name="emailer",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "asgiref==3.7.2",
        "certifi==2023.7.22",
        "charset-normalizer==3.2.0",
        "Django==3.2",  # 🔥 Downgrade to match project
        "djangorestframework==3.14.0",
        "idna==3.4",
        "pytz==2025.1",
        "requests==2.31.0",
        "sqlparse==0.4.4",
        "tzdata==2025.1",
        "urllib3==1.26.16",  # 🔥 Downgrade to match project
        "oauth @ git+https://github.com/protellus/oauth.git@66849f190a27604acd453b32680fd5412a1d9669",
        "putils @ git+https://github.com/protellus/putils.git@0db043d85012dec3919488a279b5601d172c1046"
    ],
    extras_require={
        "dev": [
            "black",
            "pytest",
        ]
    },
)