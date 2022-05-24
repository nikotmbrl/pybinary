import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-binary",
    version="0.1",
    author="Skliarenko Nikolai",
    author_email="skliarenko.nikolai@gmail.com",
    description="Serialization library for python structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
