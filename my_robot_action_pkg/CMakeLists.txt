cmake_minimum_required(VERSION 3.8)
project(my_robot_action_pkg)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID
MATCHES "Clang")
add_compile_options(-Wall -Wextra -Wpedantic)
endif()
# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(action_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
# Generate the action interface
rosidl_generate_interfaces(${PROJECT_NAME}
"action/DoTask.action"
DEPENDENCIES action_msgs
)
# Ensure Python package installation
find_package(ament_cmake_python REQUIRED)
# Install scripts (client & server)
install(PROGRAMS
scripts/action_server.py
scripts/action_client.py
DESTINATION lib/${PROJECT_NAME}
)
# Export dependencies
ament_export_dependencies(rosidl_default_runtime)
if(BUILD_TESTING)
find_package(ament_lint_auto REQUIRED)
ament_lint_auto_find_test_dependencies()
endif()
ament_package()