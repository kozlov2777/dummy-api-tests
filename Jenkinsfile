pipeline {
    agent any

    stages {
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
