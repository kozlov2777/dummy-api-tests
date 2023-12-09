pipeline {
    agent any

    stages {
        stage('install Python') {
            steps {
                sh 'sudo apt-get update'
                sh 'sudo apt-get install -y python3'
            }
        }
        stage('version') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('requirements') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('start tests') {
            steps {
                sh '''
                    cd tests
                    pytest --alluredir=allure-results
                '''
            }
        }
    }
}
