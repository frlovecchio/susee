import setuptools

with open('README.md', "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="susee",
    version='4.7',
    author="eng. Francesco Saverio Lovecchio, ph.D - Bari, Italy",
    author_email="frlovecchio@pugliautomazione.it",
    description="suSEE - Energy Monitoring System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/frlovecchio/susee',

    # packages=setuptools.find_packages(),
    packages=['susee'],

    install_requires=[
        'numpy',
        'pandas==1.5',  #due to error: 'DataFrame' object has no attribute 'iteritems'
        'markupsafe==2.0.1',
        'mysql-connector',
        'pymodbus==3.2.2',  #requires python >3.8
        'pytz',
        'scipy',
        'statsmodels',
        'python-decouple',
        'setuptools',
        'wheel',
        'bokeh==1.4.0,  "1.3.4. # 2.4.3'
        'jinja2==2.11.3',  # due to bokeh==1.3.4
    ],
   
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: System :: Monitoring',
        'Topic :: Scientific/Engineering :: Information Analysis',
        "Topic :: Software Development :: User Interfaces",
    ],

    package_dir={"": "src"},
    python_requires=">=3.7.0",
)
