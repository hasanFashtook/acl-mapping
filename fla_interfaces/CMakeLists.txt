cmake_minimum_required(VERSION 3.16)
set(CMAKE_CXX_STANDARD 17)
project(fla_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/FlightStateTransition.msg"
  "msg/FlightEvent.msg"
  "msg/FlightCommand.msg"
  "msg/JoyDef.msg"
  "msg/ControlMessage.msg"
  "msg/NodeList.msg"
  "msg/NodeStatus.msg"
  "msg/ProcessStatus.msg"
  "msg/Box.msg"
  "msg/WaypointList.msg"
  "msg/TelemString.msg"
  "msg/Detection.msg"
  "msg/ImageDetections.msg"
  "msg/Latency.msg"
  DEPENDENCIES std_msgs nav_msgs sensor_msgs builtin_interfaces geometry_msgs 
 )

ament_export_dependencies(rosidl_default_runtime)

# if(BUILD_TESTING)
#   find_package(ament_lint_auto REQUIRED)
#   set(ament_cmake_copyright_FOUND TRUE)
#   set(ament_cmake_cpplint_FOUND TRUE)
#   ament_lint_auto_find_test_dependencies()
# endif()

ament_package()
