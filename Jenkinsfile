pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ellen24k/CollaboRate.git', credentialsId: 'github-ellen24k'
            }
        }
        // stage('Build Docker Image') {
        //     steps {
        //         script {
        //             sh 'docker compose build'
        //         }
        //     }
        // }
        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker compose up --build -d'
                }
            }
        }
    }
    post {
        success {
            slackSend(channel: '#jenkins-logs', message: 'Build succeeded! 🎉', color: 'good')
        }
        failure {
            slackSend(channel: '#jenkins-logs', message: 'Build failed. 😞', color: 'danger')
        }
        always {
            slackSend(channel: '#jenkins-logs', message: 'Build finished. Check the results!', color: 'warning')
        }
    }
}
