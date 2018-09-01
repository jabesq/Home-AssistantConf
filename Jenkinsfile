pipeline {
    agent any
    stages {
        stage('Copy secrets') {
            when {
                not { branch 'secrets' }
            }
            steps {
                sh '''mv travis_secrets.yaml secrets.yaml'''
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'docker_hass_image'
                }
            }
            steps {
                sh '''hass --script check_config -c .'''
            }
        }
    }
}

