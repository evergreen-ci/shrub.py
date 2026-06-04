# Agent Guidelines

When adding a new command or making any functional change, always:

1. Bump the version in `pyproject.toml` (this project uses semantic versioning — minor bump for new features, patch for bug fixes).
2. Add a changelog entry at the top of `CHANGELOG.md` using the format:

   ```
   ## X.Y.Z - YYYY-MM-DD
   - Short description of the change.
   ```

