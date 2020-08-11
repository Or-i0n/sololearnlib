import setuptools 

with open("README.md", "r") as infile:
  readme_file = infile.read()

setuptools.setup(
    name="sololearnlib",
    version="2.0.1",
    author="OR!ON",
    author_email="orionconner00@gmail.com", 
    license="MIT",
    description="Retrieve public data from 'sololearn.com'.",
    long_description_content_type="text/markdown",
    long_description=readme_file,
    url="https://github.com/Or-i0n/sololearnlib",
    packages=setuptools.find_packages(),
    install_requires=[           
          "bs4",
      ],
  classifiers=[
    "Development Status :: 3 - Alpha",      
    "Intended Audience :: Developers",      
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",

  ],
  python_requires=">=3.5"
)