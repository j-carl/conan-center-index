cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

include(CheckCXXCompilerFlag)

find_package(xsimd REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE xsimd)

if (XSIMD_WITH_XTL)
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14)
else()
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_11)
endif()

if (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  foreach(flag "/arch:AVX")
    CHECK_CXX_COMPILER_FLAG(${flag} COMPILER_SUPPORTS_MARCH_NATIVE)
    if(COMPILER_SUPPORTS_MARCH_NATIVE)
      target_compile_options(${PROJECT_NAME} PRIVATE ${flag})
    endif()
  endforeach()
elseif ((CMAKE_CXX_COMPILER_ID STREQUAL "GNU") OR (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")  OR (CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang"))
  foreach(flag "-march=native" "-mtune=native")
    CHECK_CXX_COMPILER_FLAG(${flag} COMPILER_SUPPORTS_MARCH_NATIVE)
    if(COMPILER_SUPPORTS_MARCH_NATIVE)
      target_compile_options(${PROJECT_NAME} PRIVATE ${flag})
    endif()
  endforeach()
endif()
