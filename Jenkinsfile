pipeline {
    agent any

    environment {
        APP_NAME = 'devops-task-api'
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${APP_NAME}:${BUILD_NUMBER}"
        STAGING_PORT = '5001'
        PROD_PORT = '5000'
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python -m compileall app
                '''
                archiveArtifacts artifacts: 'app/**/*.py,requirements.txt,Dockerfile,docker-compose.yml', fingerprint: true
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest -q --cov=app --cov-report=xml --junitxml=test-results.xml
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
                sh '''
                    . .venv/bin/activate
                    python -m compileall -q app
                    if command -v pylint >/dev/null 2>&1; then
                      pylint app || true
                    else
                      echo "Pylint not installed; connect this stage to SonarQube using the Jenkins SonarQube plugin."
                    fi
                '''
            }
        }

        stage('Security') {
            steps {
                sh '''
                    if command -v trivy >/dev/null 2>&1; then
                      trivy fs --severity HIGH,CRITICAL --exit-code 1 .
                    else
                      echo "Trivy is not installed on this Jenkins agent."
                    fi
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME} .
                    docker rm -f ${APP_NAME}-staging 2>/dev/null || true
                    docker run -d --name ${APP_NAME}-staging -p ${STAGING_PORT}:5000 ${IMAGE_NAME}
                    sleep 5
                    curl --fail http://localhost:${STAGING_PORT}/health
                '''
            }
        }

        stage('Release') {
            steps {
                sh '''
                    docker tag ${IMAGE_NAME} ${APP_NAME}:latest
                    docker rm -f ${APP_NAME}-production 2>/dev/null || true
                    docker run -d --name ${APP_NAME}-production -p ${PROD_PORT}:5000 ${APP_NAME}:latest
                    sleep 5
                    curl --fail http://localhost:${PROD_PORT}/health
                    git tag -f "v1.0.${BUILD_NUMBER}" || true
                '''
            }
        }

        stage('Monitoring') {
            steps {
                sh '''
                    echo "Checking production health endpoint..."
                    curl --fail http://localhost:${PROD_PORT}/health
                    echo "Monitoring check passed."
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully: ${APP_NAME}:${BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline failed. Review the failed stage and Jenkins console output."
        }
        always {
            archiveArtifacts artifacts: 'test-results.xml,coverage.xml', allowEmptyArchive: true
        }
    }
}
