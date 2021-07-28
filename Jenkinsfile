pipeline {

  agent any
  parameters {
  	booleanParam(name: 'API_DISCOVERY', defaultValue: true, description: 'Indicator if API discovery is enabled')
    booleanParam(name: 'API_OVERWRITE', defaultValue: true, description: 'Indicator if new instance need to be created after version change')
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
      }
      steps {
      	echo 'Evaluating API Discovery'
        script {
          if(params.API_DISCOVERY){
            echo 'API Discovery is on'
            echo '${env.GROUPID}'
            echo '${env.DEV_ENVID}'
            sh 'python3 apimanagerutil.py "QT" "$DEPLOY_CREDS_USR" "$DEPLOY_CREDS_PSW" "$API_NAME" "${env.GROUPID}" "${env.DEV_ENVID}" >> apiid'
            sh 'cat apiid'
            //API_ID = '`python3 apimanagerutil.py "QT"`'
            sh 'echo $API_ID'
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