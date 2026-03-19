from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'py05_exercise'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

    (os.path.join('share', package_name, 'launch'),
        glob('launch/*.launch.xml')),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='li',
    maintainer_email='li@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'exer01_tf_spawn_py = py05_exercise.exer01_tf_spawn_py:main',
        'exer02_tf_broadcaster_py = py05_exercise.exer02_tf_broadcaster_py:main',
        'exer03_tf_listener_py = py05_exercise.exer03_tf_listener_py:main',
        ],
    },
)
