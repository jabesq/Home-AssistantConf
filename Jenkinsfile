pipeline {
  agent {
    docker {
      image 'python:3.5'
    }

  }
  stages {
    stage('Install') {
      parallel {
        stage('Install Hass') {
          steps {
            sh '''python3 -m venv hass
. hass/bin/activate

pip3 install homeassistant
'''
          }
        }
        stage('Copy secrets') {
          steps {
            sh '''mv travis_secrets.yaml secrets.yaml
'''
          }
        }
      }
    }
    stage('Test') {
      steps {
        sh '''. hass/bin/activate

hass --script check_config -c .'''
      }
    }
  }
}