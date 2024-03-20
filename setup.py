# local package in virtual environment
from setuptools import find_packages,setup

setup(
    name = 'mcqgenrator',
    version='0.0.1',
    author = 'Dikshyant',
    author_email='dikshyant.kashajoo@gmail.com',
    install_requies=['openai','langchain','streamlit','python-dotenv','PyPDF2'],
    packages=find_packages()
)