import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coleto-pkg-christofs", # Replace with your own username
    version="0.1.0",
    author="Christof Schöch",
    author_email="c.schoech@gmail.com",
    description="Tool for text comparison.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dh-trier/coleto",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
