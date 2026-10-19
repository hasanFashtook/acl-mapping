#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    #––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # launch‐time arguments
    quad                   = LaunchConfiguration('quad')
    load_params            = LaunchConfiguration('load_params')
    param_file             = LaunchConfiguration('param_file')
    use_gazebo             = LaunchConfiguration('use_gazebo')
    depth_pointcloud_topic = PythonExpression([
        "'mid360_PointCloud2' if '", use_gazebo, "' == 'true' else 'sensor_point_cloud'"
    ])
    pose_topic             = LaunchConfiguration('pose_topic')
    goal_topic             = LaunchConfiguration('goal_topic')
    odom_topic             = LaunchConfiguration('odom_topic')
    occupancy_grid_topic   = LaunchConfiguration('occupancy_grid_topic')
    unknown_grid_topic     = LaunchConfiguration('unknown_grid_topic')
    free_grid_topic        = LaunchConfiguration('free_grid_topic')
    explored_volume_topic  = LaunchConfiguration('explored_volume_topic')
    frontier_grid_topic    = LaunchConfiguration('frontier_grid_topic')
    distance_grid_topic    = LaunchConfiguration('distance_grid_topic')
    cost_grid_topic        = LaunchConfiguration('cost_grid_topic')
    path_topic             = LaunchConfiguration('path_topic')
    sparse_path_topic      = LaunchConfiguration('sparse_path_topic')

    # where to find your .yaml (make sure you install it; see below)
    param_file_path = PathJoinSubstitution([
        FindPackageShare('global_mapper_ros'),
        'cfg',
        param_file
    ])

    return LaunchDescription([
        #––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        DeclareLaunchArgument('quad',                 default_value='NX01',                        description='name of the quad / ros namespace'),
        DeclareLaunchArgument('load_params',          default_value='true',                        description='whether to load the YAML params'),
        DeclareLaunchArgument('param_file',           default_value='global_mapper.yaml',           description='name of your params file (in cfg/)'),
        DeclareLaunchArgument('use_gazebo',           default_value='true',                        description='if true use mid360_PointCloud2, else sensor_point_cloud'),
        DeclareLaunchArgument('pose_topic',           default_value='state',                        description='input pose topic'),
        DeclareLaunchArgument('goal_topic',           default_value='/move_base_simple/goal',       description='input goal topic'),
        DeclareLaunchArgument('odom_topic',           default_value='odometry/filtered_no',         description='input odometry topic'),
        DeclareLaunchArgument('occupancy_grid_topic', default_value='occupancy_grid',              description='output occupancy grid topic'),
        DeclareLaunchArgument('unknown_grid_topic',   default_value='unknown_grid',                description='output unknown grid topic'),
        DeclareLaunchArgument('free_grid_topic',      default_value='free_grid',                   description='output free grid topic'),
        DeclareLaunchArgument('explored_volume_topic', default_value='explored_volume',            description='output explored volume topic'),
        DeclareLaunchArgument('frontier_grid_topic',  default_value='frontier_grid',               description='output frontier grid topic'),
        DeclareLaunchArgument('distance_grid_topic',  default_value='distance_grid',               description='output distance grid topic'),
        DeclareLaunchArgument('cost_grid_topic',      default_value='cost_grid',                   description='output cost grid topic'),
        DeclareLaunchArgument('path_topic',           default_value='path',                        description='output path topic'),
        DeclareLaunchArgument('sparse_path_topic',    default_value='sparse_path',                 description='output sparse path topic'),

        #––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        Node(
            package='global_mapper_ros',
            executable='global_mapper_node',
            name='global_mapper_ros',
            namespace=quad,
            output='screen',
            parameters=[
                param_file_path,
                {'use_sim_time': PythonExpression(["'", use_gazebo, "' == 'true'"])}
            ],
            remappings=[
                ('depth_pointcloud_topic',    depth_pointcloud_topic),
                ('pose_topic',           pose_topic),
                ('goal_topic',           goal_topic),
                ('odom_topic',           odom_topic),
                ('occupancy_grid_topic', occupancy_grid_topic),
                ('unknown_grid_topic',   unknown_grid_topic),
                ('free_grid_topic',      free_grid_topic),
                ('explored_volume',      explored_volume_topic),
                ('frontier_grid_topic',  frontier_grid_topic),
                ('distance_grid_topic',  distance_grid_topic),
                ('cost_grid_topic',      cost_grid_topic),
                ('path_topic',           path_topic),
                ('sparse_path_topic',    sparse_path_topic),
            ],
            arguments=['--ros-args', '--log-level', 'error'],
            # prefix='xterm -e gdb -q -ex run --args', # gdb debugging
        ),
    ])
