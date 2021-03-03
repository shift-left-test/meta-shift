pipeline {
    agent {
        docker {
            image "cart.lge.com/swte/yocto:18.04"
        }
    }
    stages {
        stage("Test") {
            steps {
                sh "python3 -m pytest --basetemp=${env.WORKSPACE}/temp -xvv --junitxml result.xml"
            }
        }
        stage("Report") {
            steps {
                junit "result.xml"
            }
        }
    }
}
