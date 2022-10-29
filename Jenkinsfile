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
    API_NAME = 'sample-api'
    USE_CODE_API_VERSION = "FALSE"
    API_VERSION_FILENAME = ''

  }
  stages {
    stage('Build') {
      steps {
            sh 'mvn clean -DskipTests package'
            echo 'Build Done'

      }
    }
    stage('Deploy DEV') {
      environment {
        ENVIRONMENT = 'DEV'
        DEPLOY_APP_NAME = 'sample-api-design-dev'
        MULEENV = 'dev'
        API_VERSION_OVERWRITE = "NORMAL"
      }
      steps {
      	echo 'Evaluating API Discovery'
        script {
          if(params.API_DISCOVERY){
            echo 'API Discovery is on'
            def API_ID = sh (script: 'python3 apimanagerutil.py "GETID" "$DEPLOY_CREDS_USR" "$DEPLOY_CREDS_PSW" "$API_NAME" "${GROUPID}" "${DEV_ENVID}" "${API_VERSION_OVERWRITE}" "${USE_CODE_API_VERSION}" "${API_VERSION_FILENAME}"',  returnStdout: true)
            echo API_ID
            def props = readJSON text: API_ID.trim()
            def apiid = props['api_id']
            def updateLater = props['updateVersion']
            def exchangeVersion = props['exchageVersion']
            def access_token = props['access_token']
            // Deploying API in runtime manager
            echo 'Deploying in Runtime'
            sh 'mvn -DskipTests deploy -DmuleDeploy -Dmule.version="$MULE_VERSION" -Danypoint.username=[YOUR "$DEPLOY_CREDS_USR"] -Danypoint.password=[YOUR "$DEPLOY_CREDS_PSW"] -Dcloudhub.app="$DEPLOY_APP_NAME" -Dcloudhub.environment="$ENVIRONMENT" -Dcloudhub.bg="$BG" -Dcloudhub.worker="$WORKER" -Dcloudhub.workerType="$WORKERTYPE" -Dmule.env="$MULEENV" -Dcloudhub.region="$REGION" -Danypoint.platform.client_id=[YOUR "$PLATFORM_CREDS_USR"] -Danypoint.platform.client_secret=[YOUR "$PLATFORM_CREDS_PSW"] -Dapi.id=' + "${apiid}"

            if ("${updateLater}" == 'True'){
                echo 'Updating API version'
                def UPDATE_STATUS = sh (script: 'python3 apimanagerutil.py "UPDATEVERSION" "$DEPLOY_CREDS_USR" "$DEPLOY_CREDS_PSW" "$API_NAME" "${GROUPID}" "${DEV_ENVID}" ' + "${apiid}" + ' ' + "${exchangeVersion}" + ' ' + "${access_token}",  returnStdout: true)
                echo UPDATE_STATUS
            }
            else {
              echo 'API Manager update is not required'
            }

          }
          else{
            echo 'API Discovery is off'
            sh 'mvn -DskipTests deploy -DmuleDeploy -Dmule.version="$MULE_VERSION" -Danypoint.username=[YOUR "$DEPLOY_CREDS_USR"] -Danypoint.password=[YOUR "$DEPLOY_CREDS_PSW"] -Dcloudhub.app="$DEPLOY_APP_NAME" -Dcloudhub.environment="$ENVIRONMENT" -Dcloudhub.bg="$BG" -Dcloudhub.worker="$WORKER" -Dcloudhub.workerType="$WORKERTYPE" -Dmule.env="$MULEENV" -Dcloudhub.region="$REGION" -Danypoint.platform.client_id=[YOUR "$PLATFORM_CREDS_USR"] -Danypoint.platform.client_secret=[YOUR "$PLATFORM_CREDS_PSW"]'
          }
        }
      }
    }
  }

  tools {
    maven 'M3'
  }
}
