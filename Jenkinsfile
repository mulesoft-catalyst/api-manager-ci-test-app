pipeline {

  agent any
  parameters {
  	booleanParam(name: 'API_DISCOVERY', defaultValue: true, description: 'Indicator if API discovery is enabled')
  }
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
            sh 'mvn clean -DskipTests package'
            echo 'Build Done'
            
      }
    }
    
    stage('API Discovery') {
     steps {
      	echo 'Evaluating API Discovery'
        script {
          if(params.API_DISCOVERY){
            echo 'API Discovery is on'
            sh 'python3 api_get.py'
          }
          else{
            echo 'API Discovery is off'
          }
        }
      }
    }

     stage('Deploy DEV') {
      environment {
        ENVIRONMENT = 'DEV'
        APP_NAME = 'sample-api-design-dev'
        MULEENV = 'dev'
      }
      steps {
            sh 'echo "Deploy Done"'
            sh 'mvn -DskipTests deploy -DmuleDeploy -Dmule.version="$MULE_VERSION" -Danypoint.username="$DEPLOY_CREDS_USR" -Danypoint.password="$DEPLOY_CREDS_PSW" -Dcloudhub.app="$APP_NAME" -Dcloudhub.environment="$ENVIRONMENT" -Dcloudhub.bg="$BG" -Dcloudhub.worker="$WORKER" -Dcloudhub.workerType="$WORKERTYPE" -Dmule.env="$MULEENV" -Dcloudhub.region="$REGION" -Danypoint.platform.client_id="$PLATFORM_CREDS_USR" -Danypoint.platform.client_secret="$PLATFORM_CREDS_PSW"'
      }
    }
  }

  tools {
    maven 'M3'
  }
}