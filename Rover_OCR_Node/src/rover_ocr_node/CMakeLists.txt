cmake_minimum_required(VERSION 3.5)
project(rover_ocr_node)

# Default to C++11
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 11)
endif()

# Enable Python support
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

# Install Python scripts
install(PROGRAMS
  scripts/rover_ocr.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
