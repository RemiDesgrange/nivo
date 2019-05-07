from setuptools import setup, find_packages

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().split('\n')

setup(name='nivo_api',
      version='0.1',
      description='API to serve snow opendata from meteofrance',
      author='Remi Desgrange',
      author_email='remi+nivo@desgran.ge',
      url='',
      packages=find_packages(),
      install_requires=REQUIREMENTS,
      entry_points='''
            [console_scripts]
            import_last_nivo_data=nivo_api.cli:import_last_nivo_data
            import_all_nivo_data=nivo_api.cli:import_all_nivo_data
            import_last_bra=nivo_api.cli:import_last_bra
            import_all_bra=nivo_api.cli:import_all_bra
        ''',
      )
