# ApertureTrace

CPU execution and verification of [KeyholeImaging](https://github.com/computational-imaging/KeyholeImaging/tree/10d9f12f362d912793159c9dfc3d021d7137d5fe), by **Christopher A. Metzler, David B. Lindell and Gordon Wetzstein**. The original method reconstructs hidden object shape and motion from transient measurements along one optical path.

![ApertureTrace](assets/identity.svg)

![Original captured-scene overview](teaser.jpg)

## Run on CPU

The modern CPU check uses Python 3.12 on macOS arm64. Create an isolated environment and install the tested direct dependencies:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-cpu.txt
```

Run from the repository root. `K` is the smallest included capture, with 66 measurement rows. This command uses the original 256 × 256 grid and all 30 optimization stages, limits PyTorch to two CPU threads and saves figures without opening windows:

```sh
MPLBACKEND=Agg .venv/bin/python - <<'PY'
import runpy
import sys
import torch

torch.set_num_threads(2)
torch.set_num_interop_threads(1)
sys.argv = ["Demo.py", "--reconstruction", "K"]
runpy.run_path("Demo.py", run_name="__main__")
PY
```

Choose `E`, `K`, `Y`, `Mannequin` or `Mannequin_Assymetric`. The source default remains `Mannequin_Assymetric`. Outputs are written to `reconstructions/`; use `.venv/bin/python Demo.py --help` for the original arguments. A run can consume several GiB of memory. Thread settings limit CPU concurrency, not memory use or elapsed time.

## Compute and data

Captured `.mat` data for all five scenes is included. CPU execution is the default. The original `KeyholeEnvironment.yml` is preserved for the historical Conda stack; it pins old Python, PyTorch and CUDA versions and was not recreated by the modern CPU check. CUDA remains disabled in the source.

The forward models, regularizers, learning rate, iteration schedule, coordinate conventions, file names, and scientific figure remain unchanged.

## Verification

The complete default-resolution K run finished in 503 seconds with finite numerical values and valid array/image exports. Its raw trajectory error failed the declared constant-position baseline. [Verification](VERIFICATION.md) records that failure, the separate reflection diagnostic and the limits on image quality, convergence and physical accuracy. Initialization remains random; this single run is not a repeatability guarantee.

## Source and license

Original code and data: [KeyholeImaging](https://github.com/computational-imaging/KeyholeImaging/tree/10d9f12f362d912793159c9dfc3d021d7137d5fe). Research: [Metzler, Lindell and Wetzstein, IEEE TCI 2021](https://www.computationalimaging.org/publications/keyhole-imaging/).

[BSD-3-Clause license](LICENSE) · [Source and additions](NOTICE.md).

Maintained by **nazeeh111**.
