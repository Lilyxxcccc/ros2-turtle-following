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
    maintainer='Lilyxxcccc',
    maintainer_email='2712950900@qq.com',
    description='ROS2 TF-based turtle following project with spawn, TF broadcaster, and listener-based follower control.',
    license='Apache-2.0',
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
