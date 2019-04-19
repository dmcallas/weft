import distutils.cmd
import distutils.log
from setuptools import setup
from src import main
import glob, os

class WeftCommand(distutils.cmd.Command):
    "Custom command to tangle noweb files to source."

    description = 'Run tangle to generate source from noweb files'
    user_options = [
        ('weft-path=', None, 'Path to noweb files'),
    ]

    def initialize_options(self):
      """Set default values for options."""
      # Each user option must be listed here with their default value.
      self.weft_path = ''

    def finalize_options(self):
        """Post-process options."""
        if self.weft_path:
            assert os.path.exists(self.weft_path), f'Weft path {self.weft_path} does not exist.'

    def run(self):
        self.announce("Tangling file", level=distutils.log.INFO)
        if self.weft_path:
          os.chdir(self.weft_path)
        for file in glob.glob("*.nw"):
            main.tangle_file(file)

setup(name='weft',
      version='0.1',
      description='Literate programming',
      author='Danny McAllaster',
      author_email='dmcallas@gmail.com',
      license='Apache-2.0',
      package_dir={'': 'src'},
      setup_requires=["pytest-runner",],
      tests_require=["pytest","pytest-cov",],
      zip_safe=False,
      cmdclass={
          'weft': WeftCommand,
      },
)
