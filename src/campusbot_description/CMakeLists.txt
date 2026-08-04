cmake_minimum_required(VERSION 3.8)
project(campusbot_description)

# 查找构建工具，找不到就停止
find_package(ament_cmake REQUIRED)

# 安装规则，把rviz,urdf等文件的结果放到指定的目录
install(
  DIRECTORY rviz urdf
  DESTINATION share/${PROJECT_NAME}
)


# 注册package,导出包信息
ament_package()
