pipeline {

  agent any
  environment {
    //adding a comment for the commit test
    DEPLOY_CREDS = credentials('anypoint-creds')
    PLATFORM_CREDS = credentials('anypoint-platform-creds')
    MULE_VERSION = '4.3.0'
    BG = "Mulesoft"
    WORKER = '1'
    WORKERTYPE = 'MICRO'
    REGION = 'ap-southeast-2'
  }
  stages {
    stage('Build') {
      steps {
            bat 'mvn -B -U -e -V clean -DskipTests package'
      }
    }

     stage('Deploy DEV') {
      environment {
        ENVIRONMENT = 'DEV'
        APP_NAME = 'sample-api-design-dev'
        MULEENV = 'dev'
      }
      steps {
            bat 'mvn -U -V -e -B -DskipTests deploy -DmuleDeploy -Dmule.version="%MULE_VERSION%" -Danypoint.username="%DEPLOY_CREDS_USR%" -Danypoint.password="%DEPLOY_CREDS_PSW%" -Dcloudhub.app="%APP_NAME%" -Dcloudhub.environment="%ENVIRONMENT%" -Dcloudhub.bg="%BG%" -Dcloudhub.worker="%WORKER%" -Dcloudhub.workerType="%WORKERTYPE%" -Dmule.env="%MULEENV%" -Dcloudhub.region="%REGION%" -Danypoint.platform.client_id="%PLATFORM_CREDS_USR%" -Danypoint.platform.client_secret="%PLATFORM_CREDS_PSW%"'
      }
    }
  }

  tools {
    maven 'M3'
  }
}