from setuptools import setup, find_packages

setup(
  name='speciesguessr',
  packages=find_packages(exclude=['examples']),
  version='0.1',
  license='MIT',
  description='Game to guess species',
  long_description_content_type='text/markdown',
  author='Gaspard Dussert',
  author_email='gaspard.dussert@gmail.com',
  url='https://github.com/Gasp34/speciessguessr',
  keywords=[
    'game',
  ],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
