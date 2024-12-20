# to install the requirements

from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='faiz hadiyan',
    author_email='faizhadiyanfirza@gmail.com',
    install_requires=[
        "openai",
        "langchain",
        "langchain-community",
        "langchain-openai",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages()
)