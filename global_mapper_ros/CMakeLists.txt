cmake_minimum_required(VERSION 3.16)
project(global_mapper_ros LANGUAGES CXX C)

# ————————————————————————————————————————————————————————
# Use ccache if available
# ————————————————————————————————————————————————————————
find_program(CCACHE ccache)
if(CCACHE)
  set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
  set_property(GLOBAL PROPERTY RULE_LAUNCH_LINK   ccache)
endif()

# ————————————————————————————————————————————————————————
# C++17 + warnings, default Release
# ————————————————————————————————————————————————————————
set(CMAKE_CXX_STANDARD 17 CACHE STRING "" FORCE)
set(CMAKE_BUILD_TYPE    Release CACHE STRING "" FORCE)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ————————————————————————————————————————————————————————
# Find ROS2 / ament dependencies
# ————————————————————————————————————————————————————————
find_package(ament_cmake             REQUIRED)
find_package(rclcpp                   REQUIRED)
find_package(MPI COMPONENTS C         REQUIRED)
find_package(global_mapper            REQUIRED)
find_package(fla_utils                REQUIRED)
find_package(pcl_conversions          REQUIRED)
find_package(PCL COMPONENTS common    REQUIRED)
find_package(tf2_ros                  REQUIRED)
find_package(tf2_sensor_msgs          REQUIRED)
find_package(tf2_eigen                REQUIRED)
find_package(sensor_msgs              REQUIRED)
find_package(nav_msgs                 REQUIRED)
find_package(geometry_msgs            REQUIRED)
find_package(visualization_msgs       REQUIRED)
find_package(image_transport          REQUIRED)
find_package(cv_bridge                REQUIRED)
find_package(fla_interfaces           REQUIRED)
find_package(dynus_interfaces           REQUIRED)
find_package(builtin_interfaces       REQUIRED)
find_package(Eigen3                   REQUIRED)
find_package(message_filters          REQUIRED)
find_package(rosidl_typesupport_c REQUIRED)
find_package(rosidl_typesupport_cpp REQUIRED)
find_package(OpenMP REQUIRED)

message(STATUS ">>> global_mapper_INCLUDE_DIRS = ${global_mapper_INCLUDE_DIRS}")
message(STATUS ">>> global_mapper_LIBRARY_DIRS = ${global_mapper_LIBRARY_DIRS}")
message(STATUS ">>> global_mapper_LIBRARIES    = ${global_mapper_LIBRARIES}")

# make sure we know where its headers *and* libs are
include_directories(${global_mapper_INCLUDE_DIRS})
link_directories(   ${global_mapper_LIBRARY_DIRS})

# ————————————————————————————————————————————————————————
# Your node executable
# ————————————————————————————————————————————————————————
add_executable(global_mapper_node
  src/global_mapper_ros.cc
)

# ————————————————————————————————————————————————————————
# Include paths for your headers + external libs
# ————————————————————————————————————————————————————————
target_include_directories(global_mapper_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../fla_utils/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>
  ${PCL_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
)

# ————————————————————————————————————————————————————————
# Pull in dependencies and link
# ————————————————————————————————————————————————————————
target_compile_options(global_mapper_node PRIVATE ${OpenMP_CXX_FLAGS})
target_link_libraries(global_mapper_node
  rclcpp::rclcpp
  ${global_mapper_LIBRARIES}
  ${PCL_LIBRARIES}
  OpenMP::OpenMP_CXX
  pcl_conversions::pcl_conversions
  tf2_ros::tf2_ros
  tf2_sensor_msgs::tf2_sensor_msgs
  tf2_eigen::tf2_eigen
  ${sensor_msgs_TARGETS}
  ${nav_msgs_TARGETS}
  ${geometry_msgs_TARGETS}
  ${visualization_msgs_TARGETS}
  image_transport::image_transport
  cv_bridge::cv_bridge
  message_filters::message_filters
  ${fla_interfaces_TARGETS}
  ${dynus_interfaces_TARGETS}
  ${builtin_interfaces_TARGETS}
  Eigen3::Eigen
)

# ————————————————————————————————————————————————————————
# Install headers & the node executable
# ————————————————————————————————————————————————————————
install(
  DIRECTORY include/${PROJECT_NAME}/
  DESTINATION include/${PROJECT_NAME}
)

install(
  TARGETS global_mapper_node
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

# install for launch and config files
install(DIRECTORY
cfg
launch
DESTINATION share/${PROJECT_NAME}
)

# ————————————————————————————————————————————————————————
# Lint & tests
# ————————————————————————————————————————————————————————
# if(BUILD_TESTING)
#   find_package(ament_lint_auto REQUIRED)
#   set(ament_cmake_cpplint_FOUND   TRUE)
#   set(ament_cmake_copyright_FOUND TRUE)
#   ament_lint_auto_find_test_dependencies()
# endif()

ament_package()
