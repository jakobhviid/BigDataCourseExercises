# Images

```text
.
├── __init__.py
├── images.txt -> images used in the exercises
├── persist-images.py -> used to move images from origin to gitlab.sdu.dk registry
├── side-load.py -> used to load images from gitlab.sdu.dk registry to the Kubernetes cluster
├── side-load.sh -> used to load images defined in images.txt to the Kubernetes cluster
└── utils.py -> utility functions for the python scripts
```

## Persist used images

The [persist-images.py](./persist-images.py) script is used to move the images used in the exercises from their origin registries to the `gitlab.sdu.dk` registry.

```bash
python3 persist-images.py
```

## Side-load container images to the Kubernetes cluster

The [side-load.py](./side-load.py) script is used to side-load images into Kubernetes for faster workflows during exercises.

```bash
python3 side-load.py
```
