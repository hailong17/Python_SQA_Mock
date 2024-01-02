pipeline {
    agent any
    
    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/hailong17/Python_SQA_Mock.git'
            }
        }
        // stage('Build') {
        //     steps {
        //         // bat 'python checkpi.py'
        //         // bat 'python connectSSH.py'
        //     }
        // }
        stage('Test') {
            steps {
                bat 'python checkpi.py'
                bat 'python connectSSH.py'
                echo "This job has been tested"
            }
        }
        // stage('Deliver') {
        //     steps {
        //         echo 'Deliver....'
        //     }
        // }
    }
}
