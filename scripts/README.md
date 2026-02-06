# Deployment Scripts

This directory contains all deployment and utility scripts for PerspectiveConnect.

## Scripts

### Core Deployment
- **`deploy-versioned.sh`** - Main deployment script with versioning and rollback
- **`rollback.sh`** - Rollback to previous deployment version
- **`list-versions.sh`** - List all deployment versions and history

### Utilities
- **`check-status.sh`** - Quick health check for all services
- **`debug-deployment.sh`** - Detailed deployment diagnostics
- **`fix-deployment.sh`** - Display logs and restart services
- **`cleanup-versions.sh`** - Clean up old deployment versions

## Usage

All scripts should be run from the project root directory:

```bash
# From /opt/perspectiveconnect
./scripts/deploy-versioned.sh
./scripts/rollback.sh
./scripts/check-status.sh
```

Or use the convenience symlink in the project root:

```bash
./deploy.sh  # Points to scripts/deploy-versioned.sh
```

## Documentation

See the [`docs/`](../docs/) directory for detailed documentation on deployment procedures and workflows.
