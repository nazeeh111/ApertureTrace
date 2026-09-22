# Local verification

Checked 2026-09-22. These are bounded local checks, not research replication.

- 30 numerical source, environment, figure, and captured-data files preserve the numerical statements and data from the retained pre-publication checkout. 28 files are byte-identical; the remaining files differ only in author/branding comments.
- Lambertian and retroreflective forward models on two voxels / two viewpoints produce exactly equal 2 × 128 arrays against the retained baseline.
- Both forward models produce finite gradients for voxel intensities.
- Total variation, Laplacian, and Hessian regularizers match the retained baseline exactly on an 8 × 8 fixture.
- All 25 included captured `.mat` files opened through h5py and their numeric datasets were finite.

Not run: full 30-step expectation-maximization reconstruction, CUDA execution, or physical acquisition. CPU kernel/data checks do not establish final-scene image quality, convergence, or runtime. The historical environment file is retained unchanged.

## Test environment

An isolated local CPU environment used NumPy 2.5.3, PyTorch 2.14.0, h5py 3.16.0, SciPy 1.18.1, and Matplotlib 3.11.2. It did not replace the archived dependency manifests or modify shared environments.

[Machine-readable check results](verification.json) record dimensions and available checks.
