from setuptools import setup

setup(
    name='catkin_tools_document',
    packages=['catkin_tools_document'],
    package_data={'catkin_tools_document': ['catkin_tools_document/external/*']},
    include_package_data=True,
    version='0.0.0',
    author='Mike Purvis',
    author_email='mpurvis@clearpath.ai',
    maintainer='Mike Purvis',
    maintainer_email='mpurvis@clearpath.ai',
    url='http://catkin-tools-document.readthedocs.org/',
    keywords=['catkin'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    description="Command line tools for working with catkin.",
    long_description="Provides command line tools for working with catkin.",
    license='Apache 2.0',
    entry_points={
        'catkin_tools.commands.catkin.verbs': [
            'document = catkin_tools_document:description',
        ]
    },
    install_requires=[
        'catkin_pkg',
        'catkin_tools',
        'catkin_sphinx',
        'epydoc',
        'sphinx']
)
