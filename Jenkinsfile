pipeline {
    agent any

    environment {
        APP_NAME = 'devops-task-api'
        IMAGE_NAME = "devops-task-api:${BUILD_NUMBER}"
        STAGING_PORT = '5001'
        PROD_PORT = '5000'
    }

    stages {
        stage('Build') {
            steps {
                bat '''
                    python -m venv .venv
                    .venv\\Scripts\\python.exe -m pip install --upgrade pip
                    .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                    .venv\\Scripts\\python.exe -m compileall app
                '''
                archiveArtifacts artifacts: 'app/**/*.py,requirements.txt,Dockerfile,docker-compose.yml', fingerprint: true
            }
        }

        stage('Test') {
            steps {
                bat '''
                    .venv\\Scripts\\python.exe -m pytest -q --cov=app --cov-report=xml --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                }
            }
        }

        stage('Code Quality') {
            steps {
                bat '''
                    .venv\\Scripts\\python.exe -m pylint app --output-format=text > pylint-report.txt
                    exit /b 0
                '''
            }
        }

        stage('Security') {
            steps {
                bat '''
                    docker run --rm -v "%CD%:/workspace" aquasec/trivy:latest fs --severity HIGH,CRITICAL --exit-code 1 /workspace
                '''
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                    docker build -t %IMAGE_NAME% .
                    docker rm -f %APP_NAME%-staging 2>NUL || exit /B 0
                    docker run -d --name %APP_NAME%-staging -p %STAGING_PORT%:5000 %IMAGE_NAME%
                    timeout /T 5 /NOBREAK >NUL
                    curl --fail http://localhost:%STAGING_PORT%/health
                '''
            }
        }

        stage('Release') {
            steps {
                bat '''
                    docker tag %IMAGE_NAME% %APP_NAME%:latest
                    docker rm -f %APP_NAME%-production 2>NUL || exit /B 0
                    docker run -d --name %APP_NAME%-production -p %PROD_PORT%:5000 %APP_NAME%:latest
                    timeout /T 5 /NOBREAK >NUL
                    curl --fail http://localhost:%PROD_PORT%/health
                '''
            }
        }

        stage('Monitoring') {
            steps {
                bat '''
                    echo Checking production health endpoint...
                    curl --fail http://localhost:%PROD_PORT%/health
                    echo Monitoring check passed.
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully: ${APP_NAME}:${BUILD_NUMBER}"
        }
        failure {
            echo 'Pipeline failed. Review the failed stage and Jenkins console output.'
        }
        always {
            archiveArtifacts artifacts: 'test-results.xml,coverage.xml,pylint-report.txt', allowEmptyArchive: true
        }
    }
}
