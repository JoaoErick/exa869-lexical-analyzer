from setuptools import setup

packages = [
    "lexical_analyzer",
    "lexical_analyzer.util"
]

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name='lexical_analyzer',
    packages=packages,
    version='1.0.0',
    description='Analisador léxico construído como forma de avaliação para a disciplina EXA869 MI - Processadores de Linguagem de Programação.',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/JoaoErick/exa869-lexical-analyzer',
    project_urls={
        "Issue tracker": "https://github.com/JoaoErick/exa869-lexical-analyzer/issues",
      },
    author='AllanCapistrano | JoãoErick',
    author_email='asantos@ecomp.uefs.br | jsilva@ecomp.uefs.br',
    license='MIT License',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
		"Programming Language :: Python :: 3.11",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
	],
    python_requires='>=3.11',
)