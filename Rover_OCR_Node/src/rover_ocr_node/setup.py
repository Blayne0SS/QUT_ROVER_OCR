from setuptools import find_packages, setup

package_name = 'rover_ocr_node'

setup(
   name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
    ],
    install_requires=[
        'setuptools',       # Ensures setuptools is installed
        'easyocr',          # EasyOCR for Optical Character Recognition
        'numpy',            # NumPy for numerical operations
        'opencv-python',    # OpenCV for image processing
        #'python3-tk',          # Tkinter for GUI due to issues this is crossed out. 
        'Pillow'            # Pillow for image handling (used by EasyOCR)
    ],
    zip_safe=True,
    maintainer='Blayne Strode Smith',
    maintainer_email='n10514821@qut.edu.au, b.strodesmith@gmail.com',
    description='This package contains the code utilsed to detect text in images. The model use is easyocr. Ubuntu version 22.04, ros 2 humble, cv2',
    license='TODO: License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'rover_ocr = rover_ocr_node.rover_ocr:main',
        ],
    },
)
