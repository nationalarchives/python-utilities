import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tna-utilities",
    version="0.0.1",
    author="Andrew Hosgood",
    author_email="andrew.hosgood@nationalarchives.gov.uk",
    description="A library of common National Archives Python functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nationalarchives/python-utilities",
    project_urls={
        "Bug Tracker": "https://github.com/nationalarchives/python-utilities/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
    ],
    packages=["tna_utilities"],
    # package_data={
    #     "": ["**/*.py", "**/*.html"],
    # },
    python_requires=">=3.9",
)
