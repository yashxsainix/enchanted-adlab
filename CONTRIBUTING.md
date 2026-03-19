# Contributing to Enchanted AdLab

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/YashpalSingh/enchanted-adlab.git
cd enchanted-adlab
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Guidelines

1. **Code style** — Follow PEP 8. Use type hints where possible.
2. **Charts** — All visualisations must use Plotly (no matplotlib/seaborn).
3. **Theming** — Use colours from `utils/viz.py` constants (GOLD, BLUE, etc.).
4. **Tests** — Add unit tests for any new statistical functions in `utils/stats_engine.py`.
5. **Commits** — Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`.

## Adding a New Page

1. Create `pages/N_emoji_Name.py`
2. Import and call `apply_global_css()` and `hero_banner()` at the top
3. Use `st.container(border=True)` for card layouts
4. Add the page to the README features table

## Reporting Issues

Open a GitHub issue with:
- Steps to reproduce
- Expected vs actual behaviour
- Screenshots if applicable

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
