from setuptools import setup

setup(name='driftator',
      version='0.1',
      description='Projet du cours LU2IN013',
      url='https://github.com/MaxDtrc/Projet-Robot-LU2IN013',
      author='Driftator',
      author_email='',
      license='Aucune',
      packages=['driftator'],
      install_requires=[
          'panda3d',
          'pygame',
          'pynput',
          'numpy',
          'pillow'
      ],
      zip_safe=False)
