# Jenkins Pipeline Plan

## Build
Create the Python environment, install dependencies, compile the application and archive build evidence.

## Test
Run Pytest with coverage and publish JUnit-compatible test results.

## Code Quality
Run source checks and connect the stage to SonarQube in Jenkins for quality-gate analysis.

## Security
Run Trivy and review high/critical findings.

## Deploy
Build a Docker image, deploy a staging container and verify its health endpoint.

## Release
Tag the image as latest, start the production container and create a version tag.

## Monitoring
Perform an automated production health check. Prometheus/Grafana configuration is included for live monitoring evidence.
