pipeline {
    agent any

    stages {
        stage('Python') {
            steps {
                bat 'python --version'
            }
        }
        stage('requirements') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        stage('start tests') {
            steps {
                bat '''
                    cd tests
                    pytest --alluredir=allure-results
                '''
            }
        }
        stage('publish report') {
            steps {
                allure([
                    includeProperties: false, 
                    jdk: '', 
                    results: [[path: 'tests/allure-results']]
                ])
            }
        }
    }
}

