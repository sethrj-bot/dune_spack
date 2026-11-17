# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.generic import Package
from spack.package import *


class Dunedaqdataformats(Package):
    """Dunedaqdataformats"""

    git = "https://github.com/DUNE/dunedaqdataformats"
    url = f"{git}/archive/v4_4_5.tar.gz"

    version("4.4.5", url = "https://github.com/DUNE/dunedaqdataformats/archive/refs/tags/v4_4_5.tar.gz", sha256="fee62823c3a829331f417fc25b59f5203bb0ce4cf7e95d2ea3dbcd11ceb0b10c")
    version("4.4.4", url = "https://github.com/DUNE/dunedaqdataformats/archive/refs/tags/v4_4_4.tar.gz", sha256="4806af70ae20295547fccefb70c93785a14e6b7a0ea1d3a2b7e94e3a47044988")
    version("4.4.0", url = "https://github.com/DUNE/dunedaqdataformats/archive/refs/tags/v4_4_0.tar.gz", sha256="fee0e31693c9fb6747cc252592f6442303c873d4d68ffb43c94a6ca049c97a9e")
    version("4.0.0", url = "https://github.com/DUNE/dunedaqdataformats/archive/refs/tags/v4_0_0.tar.gz", sha256="bdc50531cae25797f940c46b95b42f8ce2f285300c972a3baabf2930aa3da51e")
    version("develop", branch="main", get_full_repo=True)

    def url_for_version(self, version):
        return f"{self.git}/archive/v{version.underscored}.tar.gz"

    @run_before("install")
    def patch_cxx20_accumulate(self):
        # C++20 std::accumulate moves the accumulator into the binary op, so a
        # lambda taking a non-const lvalue reference (auto&) no longer binds.
        # (Already fixed upstream in v4_4_0.)
        for ver in ("v3_3_3", "v3_4_1", "v4_0_0"):
            filter_file(
                r"\[\]\(auto& a, auto& b\)",
                "[](const auto& a, const auto& b)",
                "include/daqdataformats/%s/Fragment.hpp" % ver,
                ignore_absent=True,
            )

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, self.spec.prefix)
