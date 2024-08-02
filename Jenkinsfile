pipeline {
    agent any

    environment {
        // Define your environment variables here
        PATH = "/usr/local/bin/"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/updated']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/vedantnaudiyal/DjangoApplicationLibMangSys.git']])

            }
        }
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    python manage.py makemigrations
                    python manage.py migrate
                    pip install -r requirements.txt
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
                    // python manage.py runserver 0.0.0.0:8000
                '''
            }
        }
        stage('Deliver'){
            steps{
                echo " great done with deploy / delivery of product..."
            }
        }
    }
}