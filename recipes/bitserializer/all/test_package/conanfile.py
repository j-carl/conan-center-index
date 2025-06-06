from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
import os


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps", "VirtualRunEnv"
    test_type = "explicit"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires(self.tested_reference_str)

    def generate(self):
        tc = CMakeToolchain(self)
        bitserializerOptions = self.dependencies[self.tested_reference_str].options
        tc.variables["WITH_CPPRESTSDK"] = bitserializerOptions.get_safe("with_cpprestsdk", False)
        tc.variables["WITH_RAPIDJSON"] = bitserializerOptions.get_safe("with_rapidjson", False)
        tc.variables["WITH_PUGIXML"] = bitserializerOptions.get_safe("with_pugixml", False)
        tc.variables["WITH_RAPIDYAML"] = bitserializerOptions.get_safe("with_rapidyaml", False)
        tc.variables["WITH_CSV"] = bitserializerOptions.get_safe("with_csv", False)
        tc.variables["WITH_MSGPACK"] = bitserializerOptions.get_safe("with_msgpack", False)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            bin_path = os.path.join(self.cpp.build.bindirs[0], "test_package")
            self.run(bin_path, env="conanrun")
