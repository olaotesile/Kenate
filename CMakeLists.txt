cmake_minimum_required(VERSION 3.12)
project(kenate VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories
include_directories(include)

# Find Pybind11
# Fetch Pybind11
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.11.1
)
FetchContent_MakeAvailable(pybind11)

# Core Library
add_library(kenate_core INTERFACE)
target_include_directories(kenate_core INTERFACE include)

# Examples
add_executable(simple_loop examples/simple_loop.cpp)
target_link_libraries(simple_loop kenate_core)

# Python bindings
pybind11_add_module(kenate_bindings python/bindings.cpp)
target_link_libraries(kenate_bindings PRIVATE kenate_core)
set_target_properties(kenate_bindings PROPERTIES OUTPUT_NAME "kenate_bindings")
