# Publishing pybnafar

## 1. PyPI (pip)

### Build the distribution
Make sure you have `build` and `twine` installed:
```bash
pip install --upgrade build twine
```

Run the build:
```bash
python -m build
```

### Upload to PyPI
```bash
python -m twine upload dist/*
```

---

## 2. Conda-forge

### Preparation
The `conda/meta.yaml` is already prepared. When you release a new version on GitHub:

1. Fork [conda-forge/staged-recipes](https://github.com/conda-forge/staged-recipes).
2. Create a new branch.
3. Add a new directory `recipes/pybnafar/` and copy the `meta.yaml` there.
4. Point the `source: url` to the GitHub release `.tar.gz`.
5. Open a Pull Request.

---

## 3. Pre-publish Check
Always run tests before publishing:
```bash
pytest tests/
```
