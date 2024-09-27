from distutils.core import setup

setup(
    name='PlantUmlToJSchema',
    version='1.0',
    packages=['composer', 'customexception'],
    url='https://www.messaggiero.it',
    license='GPL',
    author='Massimo Iannuzzi',
    author_email='max.iannuzzi@gmail.com',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ),
    entry_points={
        'console_scripts': [
            'plantumltojschema=plantumltojschema:main',
        ],
    },
    description='Convert plantuml file in json schema'
)
