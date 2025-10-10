# Cookiecutter Python Component - Agent Guidelines

## Overview

This cookiecutter template helps create new Keboola Python components. It automates the initial setup and integrates with the Keboola Developer Portal for component registration and deployment.

## Quick Reference for Devin

To create a new Keboola component, you need these credentials configured:

**Environment Variables Required:**
- `CF_GITHUB_TOKEN` - GitHub PAT with `repo` and `admin:org` scopes
- `CF_DEVELOPER_PORTAL_DEVIN_USERNAME` - Developer Portal account email
- `CF_DEVELOPER_PORTAL_DEVIN_PASSWORD` - Developer Portal account password

**Workflow Summary:**
1. Create GitHub repo: `POST https://api.github.com/orgs/keboola/repos`
2. Login to Dev Portal: `POST https://apps-api.keboola.com/auth/login`
3. Register component: `POST https://apps-api.keboola.com/vendors/keboola/apps`
4. Run cookiecutter: `cookiecutter gh:keboola/cookiecutter-python-component`
5. Push code to GitHub
6. Configure CI/CD secrets using GitHub CLI or API

**Repository Naming Convention:**
- Format: `component-{normalized-name}` (e.g., `component-my-extractor`)
- Organization: `keboola`
- Visibility: Public (typically)

See detailed sections below for complete API documentation and examples.

## Developer Portal API Integration

### Authentication

The Developer Portal API requires authentication via username and password. Authentication tokens are obtained from the login endpoint.

**Endpoint:** `POST https://apps-api.keboola.com/auth/login`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "$CF_DEVELOPER_PORTAL_DEVIN_USERNAME",
  "password": "$CF_DEVELOPER_PORTAL_DEVIN_PASSWORD"
}
```

**Environment Variables:**
- `CF_DEVELOPER_PORTAL_DEVIN_USERNAME` - Developer Portal account email
- `CF_DEVELOPER_PORTAL_DEVIN_PASSWORD` - Developer Portal account password

**Example curl:**
```bash
curl 'https://apps-api.keboola.com/auth/login' \
  -H 'accept: */*' \
  -H 'content-type: application/json' \
  --data-raw '{"email":"$CF_DEVELOPER_PORTAL_DEVIN_USERNAME","password":"$CF_DEVELOPER_PORTAL_DEVIN_PASSWORD"}'
```

**Response:**
The endpoint returns an authentication token (JWT) that should be used in the `Authorization` header for subsequent API calls.

### Component Registration

Once authenticated, new components can be registered through the Developer Portal API.

**Endpoint:** `POST https://apps-api.keboola.com/vendors/keboola/apps`

**Headers:**
```
Authorization: <JWT_TOKEN_FROM_LOGIN>
Content-Type: text/plain;charset=UTF-8
```

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
- `id` - Unique component ID, typically in kebab-case (e.g., "my-data-extractor")
- `type` - Component type. Common values: `other`, `extractor`, `writer`, `application`

**Example curl:**
```bash
curl 'https://apps-api.keboola.com/vendors/keboola/apps' \
  -H 'accept: */*' \
  -H 'authorization: <JWT_TOKEN>' \
  -H 'content-type: text/plain;charset=UTF-8' \
  --data-raw '{"name":"test-component","id":"test-component","type":"other"}'
```

## GitHub Repository Creation

### GitHub API for Repository Creation

To create a new repository in the Keboola organization, use the GitHub REST API.

**Endpoint:** `POST https://api.github.com/orgs/keboola/repos`

**Headers:**
```
Authorization: Bearer $CF_GITHUB_TOKEN
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
```

**Request Body:**
```json
{
  "name": "component-name",
  "description": "Component description",
  "private": false,
  "auto_init": false
}
```

**Environment Variables:**
- `CF_GITHUB_TOKEN` - GitHub Personal Access Token (PAT) with `repo` and `admin:org` scopes

**Example curl:**
```bash
curl -X POST 'https://api.github.com/orgs/keboola/repos' \
  -H "Authorization: Bearer $CF_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  --data-raw '{"name":"component-example","description":"Example component","private":false,"auto_init":false}'
```

**Response:**
Returns repository details including `clone_url`, `html_url`, and `ssh_url`.

### GitHub Secrets API for CI/CD Configuration

After creating the repository, configure CI/CD secrets for automatic deployment.

**Endpoint:** `PUT https://api.github.com/repos/keboola/{repo_name}/actions/secrets/{secret_name}`

**Headers:**
```
Authorization: Bearer $CF_GITHUB_TOKEN
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
```

**Request Body:**
```json
{
  "encrypted_value": "<encrypted_secret_value>",
  "key_id": "<public_key_id>"
}
```

**Note:** Secrets must be encrypted using the repository's public key. The simpler approach is to use GitHub CLI:
```bash
gh secret set SECRET_NAME --body "secret_value" --repo "keboola/repo-name"
```

**Required Secrets:**
- `KBC_DEVELOPERPORTAL_APP` - Component ID from Developer Portal registration
- `KBC_DEVELOPERPORTAL_USERNAME` - Developer Portal username (same as login email)
- `KBC_DEVELOPERPORTAL_PASSWORD` - Developer Portal password
- `KBC_DEVELOPERPORTAL_VENDOR` - Vendor name (typically "keboola")

### Required Credentials for Devin

To automate the complete component creation workflow, Devin needs the following environment variables:

**Developer Portal Access:**
- `CF_DEVELOPER_PORTAL_DEVIN_USERNAME` - Developer Portal email for authentication
- `CF_DEVELOPER_PORTAL_DEVIN_PASSWORD` - Developer Portal password for authentication

**GitHub Access:**
- `CF_GITHUB_TOKEN` - GitHub Personal Access Token (PAT) with these scopes:
  - `repo` - Full control of private repositories (includes repo creation)
  - `admin:org` - Full control of orgs and teams (for creating repos in keboola org)
  - `workflow` - Update GitHub Action workflows (optional, for CI setup)

**Token Creation:**
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with scopes: `repo`, `admin:org`, `workflow`
3. Copy token and set as `CF_GITHUB_TOKEN` environment variable in Devin's configuration

### Component Registration Workflow

The complete automated workflow for creating a new component:

1. **Create GitHub Repository** - Use GitHub API to create `keboola/component-{name}` repository
2. **Authenticate to Developer Portal** - Call login endpoint to obtain JWT token
3. **Register Component** - Use JWT token to register component with Developer Portal
4. **Run Cookiecutter** - Execute cookiecutter template with:
   - `component_name` - Human-readable component name
   - `dev_portal_component_id` - Component ID (same as used in step 3)
   - `repository_url` - GitHub repository URL from step 1
   - `template_variant` - "GitHub"
5. **Push to GitHub** - Push the initialized template to the new repository
6. **Configure CI/CD Secrets** - Set repository secrets via GitHub API:
   - `KBC_DEVELOPERPORTAL_APP` - The component ID from registration
   - `KBC_DEVELOPERPORTAL_USERNAME` - Developer Portal username
   - `KBC_DEVELOPERPORTAL_PASSWORD` - Developer Portal password
   - `KBC_DEVELOPERPORTAL_VENDOR` - Vendor name (usually "keboola")
7. **Create Initial Tag** - Tag the commit to trigger deployment (optional)

### Automated Component Creation Script

Complete end-to-end script for creating a new component with GitHub repository and Developer Portal registration:

```bash
#!/bin/bash
# Complete component creation workflow
# Required environment variables:
# - CF_GITHUB_TOKEN
# - CF_DEVELOPER_PORTAL_DEVIN_USERNAME
# - CF_DEVELOPER_PORTAL_DEVIN_PASSWORD

set -e  # Exit on any error

COMPONENT_NAME="My New Component"
COMPONENT_ID="my-new-component"
COMPONENT_TYPE="other"
COMPONENT_DESC="Short description of the component"
REPO_NAME="component-${COMPONENT_ID}"

echo "=== Step 1: Creating GitHub Repository ==="
REPO_RESPONSE=$(curl -s -X POST "https://api.github.com/orgs/keboola/repos" \
  -H "Authorization: Bearer $CF_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  --data-raw "{\"name\":\"${REPO_NAME}\",\"description\":\"${COMPONENT_DESC}\",\"private\":false,\"auto_init\":false}")

REPO_URL=$(echo $REPO_RESPONSE | jq -r '.clone_url' | sed 's/.git$//')
echo "Repository created: $REPO_URL"

echo ""
echo "=== Step 2: Authenticating to Developer Portal ==="
AUTH_RESPONSE=$(curl -s 'https://apps-api.keboola.com/auth/login' \
  -H 'content-type: application/json' \
  --data-raw "{\"email\":\"$CF_DEVELOPER_PORTAL_DEVIN_USERNAME\",\"password\":\"$CF_DEVELOPER_PORTAL_DEVIN_PASSWORD\"}")

JWT_TOKEN=$(echo $AUTH_RESPONSE | jq -r '.token')
echo "Authenticated successfully"

echo ""
echo "=== Step 3: Registering Component in Developer Portal ==="
COMPONENT_RESPONSE=$(curl -s 'https://apps-api.keboola.com/vendors/keboola/apps' \
  -H "authorization: $JWT_TOKEN" \
  -H 'content-type: text/plain;charset=UTF-8' \
  --data-raw "{\"name\":\"${COMPONENT_NAME}\",\"id\":\"${COMPONENT_ID}\",\"type\":\"${COMPONENT_TYPE}\"}")
echo "Component registered: $COMPONENT_ID"

echo ""
echo "=== Step 4: Running Cookiecutter ==="
cookiecutter gh:keboola/cookiecutter-python-component --no-input \
  template_variant="GitHub" \
  repository_url="$REPO_URL" \
  component_name="$COMPONENT_NAME" \
  dev_portal_component_id="$COMPONENT_ID" \
  component_short_description="$COMPONENT_DESC"

echo ""
echo "=== Step 5: Pushing to GitHub ==="
cd "$REPO_NAME"
git remote set-url origin "https://x-access-token:${CF_GITHUB_TOKEN}@github.com/keboola/${REPO_NAME}.git"
git push -u origin main

echo ""
echo "=== Step 6: Configuring CI/CD Secrets ==="
# Set repository secrets for CI/CD
for SECRET in "KBC_DEVELOPERPORTAL_APP:${COMPONENT_ID}" \
              "KBC_DEVELOPERPORTAL_USERNAME:${CF_DEVELOPER_PORTAL_DEVIN_USERNAME}" \
              "KBC_DEVELOPERPORTAL_PASSWORD:${CF_DEVELOPER_PORTAL_DEVIN_PASSWORD}" \
              "KBC_DEVELOPERPORTAL_VENDOR:keboola"; do
  SECRET_NAME=$(echo $SECRET | cut -d: -f1)
  SECRET_VALUE=$(echo $SECRET | cut -d: -f2-)
  
  # Encrypt and set secret (requires GitHub CLI or additional API calls for encryption)
  gh secret set "$SECRET_NAME" --body "$SECRET_VALUE" --repo "keboola/${REPO_NAME}"
done

echo ""
echo "=== Component Creation Complete ==="
echo "Repository: $REPO_URL"
echo "Component ID: $COMPONENT_ID"
echo "Next steps:"
echo "  1. Edit src/component.py to implement your logic"
echo "  2. Update configuration schema in component_config/"
echo "  3. Create a tag to trigger deployment: git tag 0.0.1 && git push origin 0.0.1"
```

### Security Notes

- **Never commit credentials** - Use environment variables or CI/CD secrets for authentication
- **JWT tokens expire** - Obtain a fresh token for each registration session
- **Component IDs are permanent** - Choose component IDs carefully as they cannot be easily changed
- **Vendor scope** - Components are scoped to vendors; ensure you have proper permissions

## Cookiecutter Template Usage

When using this cookiecutter template:

1. **Run cookiecutter** - Either directly with `cookiecutter gh:keboola/cookiecutter-python-component` or with `make run`
2. **Provide parameters** - Fill in component name, ID, vendor, descriptions
3. **Manual registration** - Currently, component registration must be done manually via the Developer Portal UI or API
4. **Set CI variables** - Configure your CI/CD with the required environment variables
5. **Push and deploy** - Push code and tag to trigger automatic deployment

## Future Enhancements

Potential improvements for automated component registration:
- Add post-generation hook to optionally register component via API
- Provide interactive prompts for Developer Portal credentials
- Validate component ID availability before generation
- Auto-configure CI/CD variables where possible

## Reference Links

- [Keboola Developer Portal](https://components.keboola.com/)
- [Developer Portal Documentation](https://developers.keboola.com/extend/)
- [Python Component Template](https://bitbucket.org/kds_consulting_team/kbc-python-template)

