# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "asp_module: 5 messages, 3 services")

set(MSG_I_FLAGS "-Iasp_module:/home/prashanth/PartFour/src/asp_module/msg;-Istd_msgs:/opt/ros/hydro/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(asp_module_generate_messages ALL)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
)
_generate_msg_cpp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/State.msg"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg;/home/prashanth/PartFour/src/asp_module/msg/Block.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
)
_generate_msg_cpp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Observation.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
)
_generate_msg_cpp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Action.msg"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
)
_generate_msg_cpp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Block.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
)

### Generating Services
_generate_srv_cpp(asp_module
  "/home/prashanth/PartFour/src/asp_module/srv/AspCurrentState.srv"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg;/home/prashanth/PartFour/src/asp_module/msg/State.msg;/home/prashanth/PartFour/src/asp_module/msg/Block.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
)
_generate_srv_cpp(asp_module
  "/home/prashanth/PartFour/src/asp_module/srv/AspAddObservation.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
)
_generate_srv_cpp(asp_module
  "/home/prashanth/PartFour/src/asp_module/srv/AspAnswer.srv"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg;/home/prashanth/PartFour/src/asp_module/msg/Action.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
)

### Generating Module File
_generate_module_cpp(asp_module
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(asp_module_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(asp_module_generate_messages asp_module_generate_messages_cpp)

# target for backward compatibility
add_custom_target(asp_module_gencpp)
add_dependencies(asp_module_gencpp asp_module_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS asp_module_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
)
_generate_msg_lisp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/State.msg"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg;/home/prashanth/PartFour/src/asp_module/msg/Block.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
)
_generate_msg_lisp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Observation.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
)
_generate_msg_lisp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Action.msg"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
)
_generate_msg_lisp(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Block.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
)

### Generating Services
_generate_srv_lisp(asp_module
  "/home/prashanth/PartFour/src/asp_module/srv/AspCurrentState.srv"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg;/home/prashanth/PartFour/src/asp_module/msg/State.msg;/home/prashanth/PartFour/src/asp_module/msg/Block.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
)
_generate_srv_lisp(asp_module
  "/home/prashanth/PartFour/src/asp_module/srv/AspAddObservation.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
)
_generate_srv_lisp(asp_module
  "/home/prashanth/PartFour/src/asp_module/srv/AspAnswer.srv"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg;/home/prashanth/PartFour/src/asp_module/msg/Action.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
)

### Generating Module File
_generate_module_lisp(asp_module
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(asp_module_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(asp_module_generate_messages asp_module_generate_messages_lisp)

# target for backward compatibility
add_custom_target(asp_module_genlisp)
add_dependencies(asp_module_genlisp asp_module_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS asp_module_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
)
_generate_msg_py(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/State.msg"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg;/home/prashanth/PartFour/src/asp_module/msg/Block.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
)
_generate_msg_py(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Observation.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
)
_generate_msg_py(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Action.msg"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
)
_generate_msg_py(asp_module
  "/home/prashanth/PartFour/src/asp_module/msg/Block.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
)

### Generating Services
_generate_srv_py(asp_module
  "/home/prashanth/PartFour/src/asp_module/srv/AspCurrentState.srv"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg;/home/prashanth/PartFour/src/asp_module/msg/State.msg;/home/prashanth/PartFour/src/asp_module/msg/Block.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
)
_generate_srv_py(asp_module
  "/home/prashanth/PartFour/src/asp_module/srv/AspAddObservation.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
)
_generate_srv_py(asp_module
  "/home/prashanth/PartFour/src/asp_module/srv/AspAnswer.srv"
  "${MSG_I_FLAGS}"
  "/home/prashanth/PartFour/src/asp_module/msg/Configuration.msg;/home/prashanth/PartFour/src/asp_module/msg/Action.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
)

### Generating Module File
_generate_module_py(asp_module
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(asp_module_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(asp_module_generate_messages asp_module_generate_messages_py)

# target for backward compatibility
add_custom_target(asp_module_genpy)
add_dependencies(asp_module_genpy asp_module_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS asp_module_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/asp_module
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(asp_module_generate_messages_cpp std_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/asp_module
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(asp_module_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/asp_module
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(asp_module_generate_messages_py std_msgs_generate_messages_py)
