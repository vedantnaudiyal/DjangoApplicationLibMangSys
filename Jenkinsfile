pipeline {
    agent any

    environment {
        // Define your environment variables here
        PYTHONPATH = "/usr/local/bin/python3"

    }

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/jenkins_update']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/vedantnaudiyal/DjangoApplicationLibMangSys.git']])

            }
        }
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    python manage.py makemigrations
                    python manage.py migrate
                '''
            }
        }
        stage('Test'){
            steps{
                sh '''
                    source venv/bin/activate
                    pytest
                '''
            }
        }
        stage('Run') {
            steps {
                // Run the Django development server
                sh '''
                    source venv/bin/activate
                    pip install urllib3==1.26.6
                    python manage.py runserver
                '''
            }
        }
        stage('Deliver'){
            steps{
                echo " great done with deploy / delivery of product..."
            }
        }
    }
    post {
        success {
            echo "pipeline completed successfully!"
        }
        failure {
            echo "pipeline creation failed!"
        }
    }
}