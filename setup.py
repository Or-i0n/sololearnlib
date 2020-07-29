from distutils.core import setup

setup(
    name="sololearnlib",
    pakages=["sololearnlib"],
    version="1.0.1",
    licence="MIT",
    description="Retrieve public data from 'sololearn.com'.",
    author="OR!ON",
    author_email='orionconner00@gmail.com', 
    url='https://github.com/Or-i0n/sololearnlib',
    download_url='https://github.com/Or-i0n/sololearnlib/archive/v1.0.0-alpha.tar.gz',
    keywords=["sololearn", 'web scrape', 'api', "public data"],
    install_requires=[           
          'bs4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',

  ],
)