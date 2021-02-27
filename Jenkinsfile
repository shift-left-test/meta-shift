pipeline {
    agent {
        docker {
            image "cart.lge.com/swte/yocto:16.04"
        }
    }
    stages {
        stage("Setup") {
            steps {
                updateGitlabCommitStatus name: "jenkins", state: "running"
            }
        }
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
    post {
    	 success {
            updateGitlabCommitStatus name: "jenkins", state: "success"
        }
        failure {
            updateGitlabCommitStatus name: "jenkins", state: "failed"
        }
	aborted {
	    updateGitlabCommitStatus name: "jenkins", state: "canceled"
	}
    }
}

