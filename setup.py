from setuptools import setup

setup(name='literate',
      version='0.1',
      description='Literate programming',
      author='Danny McAllaster',
      author_email='dmcallas@gmail.com',
      license='GPLv3',
      package_dir={'': 'src'},
      setup_requires=["pytest-runner",],
      tests_require=["pytest","pytest-cov",],
      zip_safe=False,
)
