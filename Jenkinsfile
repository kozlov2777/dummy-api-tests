pipeline {
    agent any

    stages {
        stage('Python') {
            steps {
                bat 'python3 --version'
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
    }
}
