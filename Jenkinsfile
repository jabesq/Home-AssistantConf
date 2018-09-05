pipeline {
    agent any
    stages {
        stage('Test Config') {
            agent {
                docker {
                    image 'docker_hass_image'
                    args  '-u 0'
                }
            }
            stages{
                stage('Deploy key') {
                    steps{
                        sh '''mkdir -p /home/homeassistant/.ssh
cd /home/homeassistant/.ssh
touch id_rsa'''
                    }
                }
                stage('Copy secrets') {
                    when {
                        not { branch 'secrets' }
                    }
                    steps {
                        sh '''mv travis_secrets.yaml secrets.yaml'''
                    }
                }
                stage('Test') {
                    steps {
                        sh '''hass --script check_config -c .'''
                    }
                }
            }
        }
        stage('Deployment') {
            when  { branch 'secrets' }
            steps {
                sshagent(['d6f00138-0986-4c78-868b-c92b7a9383d7']) {
                    sh """ssh pi@dupras.fr "cd Home-AssistantConf; git pull -r; sudo systemctl restart home-assistant@homeassistant.service" """
                }
            }
        }
    }

    post {
        always {
            echo 'One way or another, I have finished'
            deleteDir() /* clean up our workspace */
        }
        success {
            slackSend color: 'good',
                      message: "The pipeline ${currentBuild.fullDisplayName} completed successfully. Hass configuration is updated"
        }
        unstable {
            echo 'I am unstable :/'
        }
        failure {
            slackSend color: 'warning',
                      message: "This configuration is not working"
        }
        changed {
            echo 'Things were different before...'
        }
    }
}
