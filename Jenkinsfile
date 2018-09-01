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
        stage('Deployment') {
            when  { branch 'secrets' }
            steps {
                sshagent(['d6f00138-0986-4c78-868b-c92b7a9383d7']) {
                    sh """ssh pi@dupras.fr cd Home-AssistantConf; git pull -r; sudo systemctl restart home-assistant@homeassistant.service"""
                }
            }
        }
    }
}

