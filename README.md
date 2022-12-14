Powder Diffraction Analysis
==========

This is the Python code to facilitate a Search/Match functionality for X-ray powder diffraction.

The basic idea is to have experimental reflections (peaks) identified and compared to reference data. To do this a background function is added to enable background subtraction. This is very helpful when doing a peak search and intensity estimation. The example file shows how the code can be used to do a search by using a directory of dI files are used as a reference database.

The Search/Match is implemented as a computation of figures of merit (FOM) between the experimental data and each of the reference data. The best FOM should coincide with the most likely candidate.
