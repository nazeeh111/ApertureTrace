# Local verification

Checked 2026-09-22. These are bounded local checks, not research replication.

- 30 numerical source, environment, figure, and captured-data files preserve the numerical statements and data from the retained pre-publication checkout. 28 files are byte-identical; the remaining files differ only in author/branding comments.
- Lambertian and retroreflective forward models on two voxels / two viewpoints produce exactly equal 2 × 128 arrays against the retained baseline.
- Both forward models produce finite gradients for voxel intensities.
- Total variation, Laplacian, and Hessian regularizers match the retained baseline exactly on an 8 × 8 fixture.
- All 25 included captured `.mat` files opened through h5py and their numeric datasets were finite.

At that date, full 30-step expectation-maximization reconstruction, CUDA execution and physical acquisition were not run. The complete CPU check below is a later result. The historical environment file is retained unchanged.

## Test environment

An isolated local CPU environment used NumPy 2.5.3, PyTorch 2.14.0, h5py 3.16.0, SciPy 1.18.1, and Matplotlib 3.11.2. It did not replace the archived dependency manifests or modify shared environments.

[Machine-readable check results](verification.json) record dimensions and available checks.

## Complete K reconstruction, 2026-10-01

One supervised CPU run completed the original K reconstruction: 66 captured measurements × 768 bins, a 256 × 256 object grid, 1,089 candidate viewpoints and all 30 expectation-maximization stages. The observer recorded 495 Adam updates in the exact original order, 555 forward evaluations and 525 finite loss returns. Losses, gradients, updated parameters and posterior probabilities remained finite. All posterior rows were normalized within 1e-5; the saved object had nonnegative values and positive total intensity.

The run took 503.04 seconds, including supervision and cleanup, on this local macOS arm64 machine. Sampled peak resident memory was 5,529,370,624 bytes; the worker reported a 5,556,912,128-byte peak. The observer used two CPU threads, an eight-GiB sampled memory cutoff and a 900-second wall limit. Neither cutoff fired. Sampling is not a hard memory cap, and these measurements are not performance guarantees for another machine or scene.

The source's unseeded initialization, learning rate, regularizers, dimensions and iteration schedule were unchanged. Ground-truth positions were not used for initialization. The isolated worker could write only to its output directory and had network access denied. Its process group was reaped, and source/capture bytes remained unchanged.

### Motion criterion and diagnostic

The predeclared criterion compared the saved `argmax(W_np)` trajectory against the source-labeled `(xpos - 0.5, zpos)` coordinates. Its root mean square position error was **0.7676194695 m**, worse than the best constant candidate's **0.3304136454 m**. **That criterion failed.**

After the run, globally reflecting the estimated x coordinates gave **0.0783776691 m** error. This orientation was selected against the reference for diagnosis; it does not replace the failed criterion. The forward model permits a joint horizontal reflection of the object and viewpoint positions. A separate asymmetric phantom check supported this symmetry to numerical precision; flipping only the object changed the signal. This explains an ambiguity available to the model, without proving why this optimizer run chose its particular orientation.

The run establishes numerical completion and successful exports, not reconstructed-image quality, convergence, calibrated physical accuracy, repeatability or other-scene performance. No seed was selected or rerun to obtain a passing score.

### Retained outputs

- [Observed configuration, checks, scores and file hashes](verification/default-k/record.json)
- [Original exported arrays](verification/default-k/source-outputs.npz): object 256 × 256, W 66 × 1,089, trajectory 33 × 33 and source reference coordinates.
- [Original object PNG](verification/default-k/object.png): 247 × 247 pixels after the source's crop and display clipping.
- [Original trajectory PNG](verification/default-k/trajectory.png): black points are source-labeled reference positions; colored points are the raw estimates. No reflection correction was applied.

The source exports its object before the final Adam update and its W before the final 31 object updates. The saved object differed from the final parameter square by at most 0.5442781448 in absolute intensity. These inherited export semantics are recorded; their numerical effect is not established as a consequential defect, and they were not changed for this check.

The run used CPython 3.12.14, NumPy 2.5.3, PyTorch 2.14.0, h5py 3.16.0 and Matplotlib 3.11.2 in an existing isolated environment. The direct dependencies are listed in [requirements-cpu.txt](requirements-cpu.txt); a fresh dependency installation was not replicated. CUDA, physical acquisition and the historical Conda environment remain unverified.

## Source preservation

The numerical bodies of `Demo.py` and `utils.py`, all 25 captured files, `KeyholeEnvironment.yml` and `teaser.jpg` match [upstream KeyholeImaging](https://github.com/computational-imaging/KeyholeImaging/tree/10d9f12f362d912793159c9dfc3d021d7137d5fe). The original source headers and BSD-3-Clause notice are restored. Documentation and verification additions are identified in [NOTICE.md](NOTICE.md).

## Continuous checks

The CPU workflow runs `python -m unittest discover -s tests -v` on Python 3.12 and the documented CPU dependencies. Small analytical fixtures check arrival bins, amplitudes and intensity gradients for both forward models, colliding returns, time-window clipping, and constant/affine regularizers. It also opens all 25 included captures and checks their recorded dataset shapes and finite values. These checks do not rerun the full optimizer, measure image quality or supersede the failed raw-motion criterion above.
