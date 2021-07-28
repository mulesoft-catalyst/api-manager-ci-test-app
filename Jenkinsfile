pipeline {

  agent any
  parameters {
  	booleanParam(name: 'API_DISCOVERY', defaultValue: true, description: 'Indicator if API discovery is enabled')
    string(name: 'API_VERSION_OVERWRITE', defaultValue: 'Y', description: 'Indicator if new instance need to be created after version change')
    booleanParam(name: 'API_DISABLE_OVERWRITE_ON_MAJOR_VERSION', defaultValue: true, description: 'Indicator if new instance need to be created after major version change')
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
    API_NAME = 'sample-api'
    APIID = 'X'
    
  }
  stages {
    stage('Build') {
      steps {
            //sh 'mvn clean -DskipTests package'
            echo 'Build Done'
            
      }
    }
    
    

    stage('Deploy DEV') {
      environment {
        ENVIRONMENT = 'DEV'
        APP_NAME = 'sample-api-design-dev'
        MULEENV = 'dev'
        //MVN_CMD = 'mvn -DskipTests deploy -DmuleDeploy -Dmule.version="$MULE_VERSION" -Danypoint.username="$DEPLOY_CREDS_USR" -Danypoint.password="$DEPLOY_CREDS_PSW" -Dcloudhub.app="$APP_NAME" -Dcloudhub.environment="$ENVIRONMENT" -Dcloudhub.bg="$BG" -Dcloudhub.worker="$WORKER" -Dcloudhub.workerType="$WORKERTYPE" -Dmule.env="$MULEENV" -Dcloudhub.region="$REGION" -Danypoint.platform.client_id="$PLATFORM_CREDS_USR" -Danypoint.platform.client_secret="$PLATFORM_CREDS_PSW"'
      }
      steps {
      	echo 'Evaluating API Discovery'
        script {
          if(params.API_DISCOVERY){
            echo 'API Discovery is on'
            def API_ID = sh (script: 'python3 apimanagerutil.py "QT" "$DEPLOY_CREDS_USR" "$DEPLOY_CREDS_PSW" "$API_NAME" "${GROUPID}" "${DEV_ENVID}" "${params.API_VERSION_OVERWRITE}"',  returnStdout: true)
            echo API_ID
            sh 'echo -DskipTests deploy -DmuleDeploy -Dmule.version="$MULE_VERSION" -Danypoint.username="$DEPLOY_CREDS_USR" -Danypoint.password="$DEPLOY_CREDS_PSW" -Dcloudhub.app="$APP_NAME" -Dcloudhub.environment="$ENVIRONMENT" -Dcloudhub.bg="$BG" -Dcloudhub.worker="$WORKER" -Dcloudhub.workerType="$WORKERTYPE" -Dmule.env="$MULEENV" -Dcloudhub.region="$REGION" -Danypoint.platform.client_id="$PLATFORM_CREDS_USR" -Danypoint.platform.client_secret="$PLATFORM_CREDS_PSW" -Dapi.id=' + API_ID
          }
          else{
            echo 'API Discovery is off'
          }
        }
      }
    }
  }

  tools {
    maven 'M3'
  }
}