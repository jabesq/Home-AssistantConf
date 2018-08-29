pipeline {
    agent any
    stages {
        stage('Install') {
            parallel {
                stage('Install Hass') {
                    agent {
                        docker {
                            image 'python:3.5'
                        }
                    }
                    steps {
                        sh '''python3 -m venv hass
. hass/bin/activate

pip3 install homeassistant
'''
                    }
                }
                stage('Copy secrets') {
                    when {
                        not { branch 'secrets' }
                    }
                    agent {
                        docker {
                            image 'python:3.5'
                        }
                    }
                    steps {
                        sh '''mv travis_secrets.yaml secrets.yaml
    '''
                    }
                }
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'python:3.5'
                }
            }
            steps {
                sh '''. hass/bin/activate
hass --script check_config -c .'''
            }
        }
      }
    }
  }
}