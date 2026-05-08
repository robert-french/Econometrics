# Econometrics (ECON 3300)

Course materials and interactive [marimo](https://marimo.io) notebooks for ECON 3300 Econometrics, exported to WebAssembly and deployed to GitHub Pages.

## 🚀 Usage

1. Add marimo notebooks to the `notebooks/` or `apps/` directory
   1. `notebooks/` notebooks are exported with `--mode edit`
   2. `apps/` notebooks are exported with `--mode run`
2. Push to main branch
3. GitHub Actions will automatically build and deploy to Pages

The course site is deployed via GitHub Pages from the `Settings > Pages` "GitHub Actions" source.

## Including data or assets

To include data or assets in your notebooks, add them to the `public/` directory and load them via:

```python
import polars as pl
df = pl.read_csv(mo.notebook_location() / "public" / "dataset.csv")
```

## 🎨 Templates

This repository includes several templates for the generated site:

1. `index.html.j2` (default): A template with styling and a footer
2. `tailwind.html.j2`: A minimal and lean template using Tailwind CSS

To use a specific template, pass the `--template` parameter to the build script:

```bash
uv run .github/scripts/build.py --template templates/tailwind.html.j2
```

See [templates/README.md](templates/README.md) for more information on customizing templates.

## 🧪 Testing

To test the export process locally, run `.github/scripts/build.py` from the root directory:

```bash
uv run .github/scripts/build.py
```

This will export all notebooks to a `_site/` folder. Then to serve the site:

```bash
python -m http.server -d _site
```

This will serve the site at `http://localhost:8000`.
