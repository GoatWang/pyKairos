import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyKairos",
    version="0.0.1",
    author="GoatWang",
    author_email="jeremywang@thinktronltd.com",
    description="KairosDB python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoatWang/pyKairos",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)