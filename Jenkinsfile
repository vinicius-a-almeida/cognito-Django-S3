pipeline{
    agent any
    stages{
        stage('Checkout'){
            steps{
                git branch: 'master', credentialsId: 'ghp_fopco9myzw0gbkf1nwidt4emlsfkss4ycps3', url: 'https://github.com/vinicius-a-almeida/cognito-Django-S3.git'
            }
        }
        stage('Setup Python Virtual Environment'){
            steps{
                sh '''
                    chmod +x envsetup.sh
                    ./envsetup.sh
                '''
            }
        }
        stage('Setup Gunicorn Setup'){
            steps{
                sh '''
                    chmod +x gunicorn.sh
                    ./gunicorn.sh
                '''
            }
        }
        stage('setup NGINX'){
            steps{
                sh '''
                    chmod +x nginx.sh
                    ./nginx.sh
                '''
            }
        }
    }
}