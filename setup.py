from setuptools import setup, find_packages

setup(
    name="edgartool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'lxml>=4.9.0',
    ],
    author="Pratik Relekar, Xinyao Qian",
    author_email="pratik.relekar@gmail.com, xinyaoq2@illinois.edu",
    description="A tool for cleaning SEC EDGAR HTML files",
    long_description=open('README.md').read(),
    url="https://github.com/pratikrelekar/edgar_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
