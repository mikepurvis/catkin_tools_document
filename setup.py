from setuptools import setup

setup(
    name='catkin_tools_document',
    packages=['catkin_tools_document'],
    package_data={'catkin_tools_document': ['catkin_tools_document/external/*']},
    include_package_data=True,
    version='0.2.0',
    author='Mike Purvis',
    author_email='mike@uwmike.com',
    maintainer='Mike Purvis',
    maintainer_email='mike@uwmike.com',
    url='https://github.com/mikepurvis/catkin_tools_document',
    keywords=['catkin'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    description="Plugin for catkin_tools to enable building workspace documentation.",
    license='Apache 2.0',
    entry_points={
        'catkin_tools.commands.catkin.verbs': [
            'document = catkin_tools_document:description',
        ]
    },
    install_requires=[
        'catkin_pkg',
        'catkin_tools>=0.4.4',
        'catkin_sphinx',
#        'pydoctor',
        'sphinx']
)
