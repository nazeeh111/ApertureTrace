# Source and additions

The reconstruction code, archived environment, teaser and 25 captured-data files come from [KeyholeImaging](https://github.com/computational-imaging/KeyholeImaging/tree/10d9f12f362d912793159c9dfc3d021d7137d5fe), by Christopher A. Metzler, David B. Lindell and Gordon Wetzstein. The retained source accompanies *Keyhole Imaging: Non-Line-of-Sight Imaging and Tracking of Moving Objects Along a Single Optical Path*, IEEE Transactions on Computational Imaging, 2021.

The original BSD-3-Clause notice and Christopher Metzler's 2020 copyright are preserved in [LICENSE](LICENSE). The environment, teaser, captured files and `Demo.py` numerical body match that pinned upstream version. `utils.py` has explicit compatibility repairs described below. Original source attribution comments are restored.

ApertureTrace adds repository identity, documentation, CPU dependency guidance and local verification records maintained by nazeeh111. These additions are distributed under BSD-3-Clause. The research method, data acquisition and original scientific results belong to the cited authors.

The 26 October 2026 sampler repairs rebuild implicit voxel grids per call, accept the declared NumPy defaults, and enable the optional three-bin smoothing filter while preserving its sampling dimension. Radiometric formulas, the main optimizer and captured data are unchanged.
