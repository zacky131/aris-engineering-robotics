# Vendor

This directory is reserved for vendored third-party content if needed.

**Policy**: Prefer references and symlinks via the installer over vendoring.
Only vendor content here if it is not otherwise installable or if an offline
installation is needed.

Any vendored content must:
1. Include its original license.
2. Be documented in `NOTICE.md`.
3. Be listed in the installer manifest.
