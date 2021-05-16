import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup
sys.path.append("..")
import sdist_upip

setup(name='pico-utils',
      version='0.0.1',
      description='various utils modules for MicroPython',
      long_description="Used to quickly build up robots which incorporate sensors and/or pwm boards",
      url='https://github.com/butoane/pico-utils',
      author='Claudiu Remenyi',
      author_email='remenyic@gmail.com',
      maintainer='Claudiu Remenyi',
      maintainer_email='remenyic@gmail.com',
      license='MIT')