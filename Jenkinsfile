pipeline {
    agent any
    
    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/hailong17/Python_SQA_Mock.git'
            }
        }
        stage('Build') {
            steps {
                echo "Hello"
            }
        }
        stage('Test') {
            steps {
                echo "Current Directory: ${pwd()}"
                sh 'python3 checkpi.py'
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
            }
        }
    }
}
