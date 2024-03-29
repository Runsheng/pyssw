# pyssw: python wrapper for Smith-Waterman Python Module

The C code for SWW alignment is derived from:
[original source repository](https://github.com/mengyao/Complete-Striped-Smith-Waterman-Library)

Please cite this [PLOS ONE paper](http://dx.plos.org/10.1371/journal.pone.0082138) by Zhao et al. 2013

## Overview

SSW is a fast implementation of the Smith-Waterman algorithm, which uses the
Single-Instruction Multiple-Data (SIMD) instructions to parallelize the
algorithm at the instruction level. It can return the Smith-Waterman score,
alignment location and traceback path (cigar) of the optimal alignment
accurately; and return the sub-optimal alignment score and location
heuristically.

Note: When SSW open a gap, the gap open penalty alone is applied.

## Installation

from [PyPi](https://pypi.org/project/pyssw/)

    pip install pyssw


or from source
    
    git clone  https://github.com/Runsheng/pyssw.git
    cd pyssw
    pip install . 