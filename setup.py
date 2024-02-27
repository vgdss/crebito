import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths), 
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip() 
        for line in read(path).split("\n") 
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="Crebito",
    version="0.1.0",
    description="Créditos e Débitos (crébitos)",
    url="https://github.com/zanfranceschi/rinha-de-backend-2024-q1/tree/main/participantes/vgdss",
    python_requires=">=3.12.1",
    long_description="Rinha de Backend - 2024/Q1",
    long_description_content_type="text/markdown",
    author="Vitor Gabriel",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=read_requirements("requirements.txt"),
)