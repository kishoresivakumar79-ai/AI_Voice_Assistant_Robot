from setuptools import setup

package_name = 'vision_pkg'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name] if False else []),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=true,
    maintainer='Developer',
    maintainer_email='robot@user.com',
    description='ROS2 package for camera streaming, face detection, and tracking',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_node = vision_pkg.camera_node:main',
        ],
    },
)
