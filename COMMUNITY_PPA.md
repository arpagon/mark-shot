# Unofficial community PPA automation

This branch exists only to operate the explicitly unofficial Mark Shot community PPA for Ubuntu 26.04 Resolute. The repository's `main` branch remains an exact mirror of `upstream/main`; community-only automation is intentionally excluded from upstream pull requests.

## Release flow

`community-ppa-sync.yml` runs every six hours and can also be started manually. It:

1. reads GitHub's latest stable release for `jswysnemc/mark-shot`;
2. rejects drafts, prereleases, and unexpected tag formats;
3. checks Launchpad for an existing source publication of that upstream version;
4. avoids dispatching while another publication workflow is active;
5. requests `ppa-publish.yml` with PPA revision `1` when the release is missing.

Publication remains protected by the `ppa-production` environment. A configured reviewer must approve the run before the signing key is exposed or a source package is uploaded. Launchpad, not GitHub Actions, builds the binary package.

The publisher uses the `debian/` packaging shipped in the official release tag. This lets upstream packaging dependency and changelog changes travel with the release rather than relying on a stale copy in this community branch. For Rust releases, it uses the release's vendoring script and locked dependencies to include an `orig-vendor` source component; application compilation remains offline on Launchpad.

Version-specific packaging backports:

- `v0.1.61`: `.github/packaging/v0.1.61-smoke` backports upstream commit `24d15f10e0ba7347cd4107e8c83e7e15dde9f660` (the `debian/tests/smoke` change only). This corrects private helper paths after their move to `/usr/libexec/mark-shot`, without modifying application sources. The source changelog records the backport. `.github/packaging/prepare-v0.1.61.py` also normalizes private Python module permissions, wraps long Debian changelog bullets, and removes an installed duplicate license file (the required license remains in `debian/copyright`). These packaging-only fixes resolve the release's actionable Lintian warnings.

## Configuration

Repository configuration remains outside Git:

- variable: `PPA_TARGET` (`ppa:owner/archive`);
- secrets: `LAUNCHPAD_GPG_PRIVATE_KEY` and `LAUNCHPAD_GPG_PASSPHRASE`;
- environment: `ppa-production`, with required reviewers.

If a build of the same upstream release must be repeated, manually run `ppa-publish.yml` with an incremented `ppa_revision`. Never overwrite or reuse an already uploaded Debian version.
