from distutils.core import setup

setup(
    name="sololearn",
    pakages=["sololearn"],
    version="1.0",
    licence="MIT",
    description="Retrieve public data from 'sololearn.com'.",
    author="OR!ON",
    author_email='orionconner00@gmail.com',      # Type in your E-Mail
    url='https://github.com/user/reponame',   # Provide either the link to your github or to your website
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
    keywords=["sololearn", 'web scrape', 'api', "public data"],
    install_requires=[           
          'bs4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)