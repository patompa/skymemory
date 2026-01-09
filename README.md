# SkyMemory
Code Companion for:
[SkyMemory: A LEO Edge Cache for Transformer Inference Optimization and Scale Out](https://arxiv.org/abs/2505.14427)

```
@article{sandholm2025skymemory,
  title={SkyMemory: A LEO Edge Cache for Transformer Inference Optimization and Scale Out},
  author={Sandholm, Thomas and Mukherjee, Sayandev and Cheng, Lin and Huberman, Bernardo A},
  journal={arXiv preprint arXiv:2505.14427},
  year={2025}
}
```

Paper results can be reproduced by running:
```
./simulate.sh
```
which generates raw result data in `./results` and plots in `./plots`.

Only python dependency is `numpy`.

## Chunk Layout visualization
Requires Python Pillow
```
usage: chunk_visualization.py [-h] [-strategy {rotation,hop,hop_rotation}]
                              [-center_sat CENTER_SAT] [-center_orb CENTER_ORB]
                              [-servers SERVERS] [-rotations ROTATIONS] [-output OUTPUT]
                              [-tot_sats TOT_SATS] [-tot_orbs TOT_ORBS]

Visualize chunk positions

options:
  -h, --help            show this help message and exit
  -strategy, -s {rotation,hop,hop_rotation}
  -center_sat, -cs CENTER_SAT
  -center_orb, -co CENTER_ORB
  -servers, -ss SERVERS
  -rotations, -r ROTATIONS
  -output, -o OUTPUT
  -tot_sats, -ts TOT_SATS
  -tot_orbs, -to TOT_ORBS
```
