# Cookiecutter Python Component - Agent Guidelines

## Overview

This cookiecutter template helps create new Keboola Python components. It automates the initial setup and integrates with the Keboola Developer Portal for component registration and deployment.

## Quick Reference for Devin

To create a new Keboola component, you need these credentials configured:

**Environment Variables Required:**
- `CF_DEVELOPER_PORTAL_DEVIN_USERNAME` - Developer Portal account email
- `CF_DEVELOPER_PORTAL_DEVIN_PASSWORD` - Developer Portal account password
- `CF_GITHUB_TOKEN` - GitHub PAT with `repo` and `admin:org` scopes (optional when using existing repo)

**Workflow Summary:**
1. Create GitHub repo: `POST https://api.github.com/orgs/{GITHUB_ORG}/repos` (skip if repo exists: set `SKIP_REPO_CREATION=true`)
2. Login to Dev Portal: `POST https://apps-api.keboola.com/auth/login`
3. Register component: `POST https://apps-api.keboola.com/vendors/{VENDOR_NAME}/apps` (returns full ID: `vendor.component-id`)
4. Update component config: `PATCH https://apps-api.keboola.com/vendors/{VENDOR_NAME}/apps/{FULL_COMPONENT_ID}` (set UI options, defaultBucket, etc.)
5. Run cookiecutter: `cookiecutter gh:{GITHUB_ORG}/cookiecutter-python-component` (pass component ID **without** vendor prefix)
6. Push code to GitHub
7. Configure CI/CD secrets using GitHub CLI or API (use full component ID for `KBC_DEVELOPERPORTAL_APP`)

**Repository Naming Convention:**
- Format: `component-{normalized-name}` (e.g., `component-my-extractor`)
- Vendor: Configurable (e.g., `keboola`, `YOUR_VENDOR`)
- GitHub Organization: Configurable (e.g., `keboola`, `YOUR_ORG`)
- Visibility: Public (typically)

See detailed sections below for complete API documentation and examples.

## Developer Portal API

### Authentication

**Endpoint:** `POST https://apps-api.keboola.com/auth/login`

**Request Body:**
```json
{
  "email": "$CF_DEVELOPER_PORTAL_DEVIN_USERNAME",
  "password": "$CF_DEVELOPER_PORTAL_DEVIN_PASSWORD"
}
```

**Response:**
Returns a JWT token used in the `Authorization` header for subsequent API calls.

### Component Registration

**Endpoint:** `POST https://apps-api.keboola.com/vendors/{VENDOR_NAME}/apps`

**Headers:** `Authorization: <JWT_TOKEN_FROM_LOGIN>`

**Request Body:**
```json
{
  "name": "component-display-name",
  "id": "component-id",
  "type": "other"
}
```

**Parameters:**
- `name` - Human-readable component name (e.g., "My Data Extractor")
- `id` - Unique component ID (3-64 chars, letters/numbers/dashes only, cannot end with dash, e.g., "my-data-extractor"). The Developer Portal will automatically prefix it with your vendor name and return the full ID (e.g., "keboola.my-data-extractor")
- `type` - Component type: `other`, `extractor`, `writer`, `application`

**Response:**
The API returns the registered component with the full vendor-prefixed `id` field (e.g., "keboola.my-data-extractor"). For CI/CD configuration, you need both:
- The full component ID for `KBC_DEVELOPERPORTAL_APP` secret
- The component ID WITHOUT vendor prefix for the `dev_portal_component_id` cookiecutter parameter

### Component Configuration Update

After initial registration, you can update component configuration using the PATCH endpoint:

**Endpoint:** `PATCH https://apps-api.keboola.com/vendors/{VENDOR_NAME}/apps/{FULL_COMPONENT_ID}`

**Headers:** `Authorization: <JWT_TOKEN_FROM_LOGIN>`

**Request Body:**
```json
{
  "name": "Component Display Name",
  "type": "extractor",
  "repository": {"options": {}},
  "network": "bridge",
  "defaultBucket": true,
  "uiOptions": ["genericDockerUI", "appInfo.experimental"],
  "imageParameters": {},
  "stackParameters": {},
  "actions": [],
  "fees": false,
  "logger": "standard",
  "stagingStorageInput": "local",
  "stagingStorageOutput": "local",
  "dataTypeSupport": "none",
  "allowedProcessorPosition": "any"
}
```

**UI Options & defaultBucket Configuration:**

| Component Type | defaultBucket | uiOptions |
|---|---|---|
| **Extractor** | `true` | `["genericDockerUI", "appInfo.experimental"]` |
| **Writer (multiple tables)** | `false` | `["genericDockerUI", "appInfo.experimental", "genericDockerUI-tableInput"]` |
| **Writer (single table)** | `false` | `["genericDockerUI", "appInfo.experimental", "genericDockerUI-simpleInputTable"]` |
| **Application** | `false` | `["genericDockerUI", "appInfo.experimental"]` |

**Add `genericDockerUI-rows`** to any component type that supports configuration rows.

**Quick Example:**
```bash
# Login
JWT_TOKEN=$(curl -s 'https://apps-api.keboola.com/auth/login' \
  -H 'content-type: application/json' \
  --data-raw '{"email":"user@example.com","password":"pass"}' | jq -r '.token')

# Register & get full component ID
FULL_COMPONENT_ID=$(curl -s 'https://apps-api.keboola.com/vendors/keboola/apps' \
  -H "authorization: $JWT_TOKEN" -H 'content-type: text/plain;charset=UTF-8' \
  --data-raw '{"name":"My Component","id":"my-component","type":"extractor"}' | jq -r '.id')

# Update configuration
curl -s "https://apps-api.keboola.com/vendors/keboola/apps/${FULL_COMPONENT_ID}" -X 'PATCH' \
  -H "authorization: $JWT_TOKEN" -H 'content-type: text/plain;charset=UTF-8' \
  --data-raw '{"repository":{"options":{}},"network":"bridge","defaultBucket":true,"uiOptions":["genericDockerUI","appInfo.experimental"],"imageParameters":{},"stackParameters":{},"actions":[],"fees":false,"logger":"standard","stagingStorageInput":"local","stagingStorageOutput":"local","dataTypeSupport":"none","allowedProcessorPosition":"any"}'
```

## GitHub Setup

**Create Repository:** `POST https://api.github.com/orgs/{GITHUB_ORG}/repos`
```json
{"name": "component-name", "description": "Component description", "private": false, "auto_init": false}
```

**Required CI/CD Secrets** (set via `gh secret set`):
- `KBC_DEVELOPERPORTAL_APP` - Full component ID with vendor prefix (e.g., `keboola.my-component`)
- `KBC_DEVELOPERPORTAL_USERNAME` - Developer Portal email
- `KBC_DEVELOPERPORTAL_PASSWORD` - Developer Portal password
- `KBC_DEVELOPERPORTAL_VENDOR` - Vendor name (e.g., `keboola`)

**Note:** The GitHub Actions workflow constructs the full component ID from `VENDOR.COMPONENT_ID`. The cookiecutter template expects the component ID **without** the vendor prefix in `dev_portal_component_id`, and the vendor name separately in `dev_portal_vendor_name`.

## Automated Component Creation Script

Complete workflow script. Set `SKIP_REPO_CREATION=true` and `REPO_URL` to use an existing repository.

```bash
#!/bin/bash
# Complete component creation workflow
# Required environment variables:
# - CF_DEVELOPER_PORTAL_DEVIN_USERNAME
# - CF_DEVELOPER_PORTAL_DEVIN_PASSWORD
# - CF_GITHUB_TOKEN (only required if SKIP_REPO_CREATION is not set, or for automated CI/CD secret setup)
#
# Optional environment variables (for existing repositories):
# - SKIP_REPO_CREATION=true (skip GitHub repo creation if repo already exists)
# - REPO_URL (required when SKIP_REPO_CREATION=true, e.g., "https://github.com/{GITHUB_ORG}/component-name")

set -e  # Exit on any error

# Configuration variables - customize these for your vendor and GitHub organization
VENDOR_NAME="${VENDOR_NAME:-keboola}"  # Developer Portal vendor name
GITHUB_ORG="${GITHUB_ORG:-keboola}"    # GitHub organization name

COMPONENT_NAME="My New Component"
COMPONENT_ID="my-new-component"  # Component ID without vendor prefix (will be prefixed automatically by Dev Portal)
COMPONENT_TYPE="extractor"
COMPONENT_DESC="Short description of the component"
REPO_NAME="component-${COMPONENT_ID}"

# Step 1: Create GitHub Repository (skip if already exists)
if [ "${SKIP_REPO_CREATION}" = "true" ]; then
  echo "=== Step 1: Skipping GitHub Repository Creation (using existing repo) ==="
  if [ -z "${REPO_URL}" ]; then
    echo "Error: REPO_URL must be provided when SKIP_REPO_CREATION=true"
    exit 1
  fi
  echo "Using existing repository: $REPO_URL"
else
  echo "=== Step 1: Creating GitHub Repository ==="
  REPO_RESPONSE=$(curl -s -X POST "https://api.github.com/orgs/${GITHUB_ORG}/repos" \
    -H "Authorization: Bearer $CF_GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    --data-raw "{\"name\":\"${REPO_NAME}\",\"description\":\"${COMPONENT_DESC}\",\"private\":false,\"auto_init\":false}")
  
  REPO_URL=$(echo $REPO_RESPONSE | jq -r '.clone_url' | sed 's/.git$//')
  echo "Repository created: $REPO_URL"
fi

echo ""
echo "=== Step 2: Authenticating to Developer Portal ==="
AUTH_RESPONSE=$(curl -s 'https://apps-api.keboola.com/auth/login' \
  -H 'content-type: application/json' \
  --data-raw "{\"email\":\"$CF_DEVELOPER_PORTAL_DEVIN_USERNAME\",\"password\":\"$CF_DEVELOPER_PORTAL_DEVIN_PASSWORD\"}")

JWT_TOKEN=$(echo $AUTH_RESPONSE | jq -r '.token')
echo "Authenticated successfully"

echo ""
echo "=== Step 3: Registering Component in Developer Portal ==="
COMPONENT_RESPONSE=$(curl -s "https://apps-api.keboola.com/vendors/${VENDOR_NAME}/apps" \
  -H "authorization: $JWT_TOKEN" \
  -H 'content-type: text/plain;charset=UTF-8' \
  --data-raw "{\"name\":\"${COMPONENT_NAME}\",\"id\":\"${COMPONENT_ID}\",\"type\":\"${COMPONENT_TYPE}\"}")

# Extract the full component ID from the response (includes vendor prefix)
FULL_COMPONENT_ID=$(echo $COMPONENT_RESPONSE | jq -r '.id')
echo "Component registered: $FULL_COMPONENT_ID"

# Extract just the component ID part (without vendor prefix) for cookiecutter
# e.g., "keboola.my-component" -> "my-component"
COMPONENT_ID_ONLY="${FULL_COMPONENT_ID#*.}"

echo ""
echo "=== Step 4: Updating Component Configuration ==="
# Determine UI options based on component type
UI_OPTIONS='["genericDockerUI","appInfo.experimental"]'
DEFAULT_BUCKET="false"

# Set component-type specific configurations
if [ "$COMPONENT_TYPE" = "extractor" ]; then
  DEFAULT_BUCKET="true"
fi

curl -s "https://apps-api.keboola.com/vendors/${VENDOR_NAME}/apps/${FULL_COMPONENT_ID}" \
  -X 'PATCH' \
  -H "authorization: $JWT_TOKEN" \
  -H 'content-type: text/plain;charset=UTF-8' \
  --data-raw "{
    \"name\":\"${COMPONENT_NAME}\",
    \"type\":\"${COMPONENT_TYPE}\",
    \"repository\":{\"options\":{}},
    \"network\":\"bridge\",
    \"defaultBucket\":${DEFAULT_BUCKET},
    \"uiOptions\":${UI_OPTIONS},
    \"imageParameters\":{},
    \"stackParameters\":{},
    \"actions\":[],
    \"fees\":false,
    \"logger\":\"standard\",
    \"stagingStorageInput\":\"local\",
    \"stagingStorageOutput\":\"local\",
    \"dataTypeSupport\":\"none\",
    \"allowedProcessorPosition\":\"any\"
  }" > /dev/null

echo "Component configuration updated"

echo ""
echo "=== Step 5: Running Cookiecutter ==="
# Note: dev_portal_component_id should be WITHOUT vendor prefix
# The GitHub Actions workflow will construct the full ID as: VENDOR.COMPONENT_ID
cookiecutter gh:${GITHUB_ORG}/cookiecutter-python-component --no-input \
  template_variant="GitHub" \
  repository_url="$REPO_URL" \
  component_name="$COMPONENT_NAME" \
  dev_portal_vendor_name="$VENDOR_NAME" \
  dev_portal_component_id="$COMPONENT_ID_ONLY" \
  component_short_description="$COMPONENT_DESC"

echo ""
if [ "${SKIP_REPO_CREATION}" = "true" ]; then
  echo "=== Step 6: Skipping GitHub Push (existing repository) ==="
  echo "Please push the code manually or ensure the repository is already configured"
else
  echo "=== Step 6: Pushing to GitHub ==="
  cd "$REPO_NAME"
  git remote set-url origin "https://x-access-token:${CF_GITHUB_TOKEN}@github.com/${GITHUB_ORG}/${REPO_NAME}.git"
  git push -u origin main
fi

echo ""
if [ -n "${CF_GITHUB_TOKEN}" ]; then
  echo "=== Step 7: Configuring CI/CD Secrets ==="
  # Set repository secrets for CI/CD
  for SECRET in "KBC_DEVELOPERPORTAL_APP:${FULL_COMPONENT_ID}" \
                "KBC_DEVELOPERPORTAL_USERNAME:${CF_DEVELOPER_PORTAL_DEVIN_USERNAME}" \
                "KBC_DEVELOPERPORTAL_PASSWORD:${CF_DEVELOPER_PORTAL_DEVIN_PASSWORD}" \
                "KBC_DEVELOPERPORTAL_VENDOR:${VENDOR_NAME}"; do
    SECRET_NAME=$(echo $SECRET | cut -d: -f1)
    SECRET_VALUE=$(echo $SECRET | cut -d: -f2-)
    
    # Encrypt and set secret (requires GitHub CLI or additional API calls for encryption)
    gh secret set "$SECRET_NAME" --body "$SECRET_VALUE" --repo "${GITHUB_ORG}/${REPO_NAME}"
  done
else
  echo "=== Step 7: Skipping CI/CD Secret Configuration ==="
  echo "CF_GITHUB_TOKEN not set. Please configure the following secrets manually:"
  echo "  - KBC_DEVELOPERPORTAL_APP: ${FULL_COMPONENT_ID}"
  echo "  - KBC_DEVELOPERPORTAL_USERNAME: ${CF_DEVELOPER_PORTAL_DEVIN_USERNAME}"
  echo "  - KBC_DEVELOPERPORTAL_PASSWORD: (your password)"
  echo "  - KBC_DEVELOPERPORTAL_VENDOR: ${VENDOR_NAME}"
fi

echo ""
echo "=== Component Creation Complete ==="
echo "Repository: $REPO_URL"
echo "Component ID: $FULL_COMPONENT_ID"
echo "Next steps:"
echo "  1. Edit src/component.py to implement your logic"
echo "  2. Update configuration schema in component_config/"
echo "  3. Create a tag to trigger deployment: git tag 0.0.1 && git push origin 0.0.1"
```


## Notes

- Never commit credentials - use environment variables
- JWT tokens expire - obtain fresh token per session
- Component IDs are permanent - choose carefully
- Components are vendor-scoped
- **Important:** When the Developer Portal returns a component ID like `keboola.my-component`, you must split it:
  - Pass `keboola` to `dev_portal_vendor_name` cookiecutter parameter
  - Pass `my-component` (without vendor) to `dev_portal_component_id` cookiecutter parameter
  - The GitHub Actions workflow will reconstruct the full ID as `VENDOR.COMPONENT_ID`

**Links:** [Developer Portal](https://components.keboola.com/) | [Documentation](https://developers.keboola.com/extend/)
