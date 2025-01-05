from setuptools import setup, find_packages

with open('requirements.txt') as file:
    required_packages = file.read().splitlines()

setup(
    name="giftcard-service-backend",
    version="0.0.1",
    description="A Giftcard Management System using FastAPI",
    author="Luca Franzesi",
    author_email="lfranzesi@hotmail.it",
    url="https://github.com/LucaFranzesi/giftcard-service-backend",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=required_packages,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)