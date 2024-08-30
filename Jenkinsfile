pipeline {
    agent any
    environment {
        SITENAME = 'your_sitename'
        ORG_ID = 'your_org_id'
        EMAIL = credentials('your_email_credential_id')
        API_TOKEN = credentials('your_api_token_credential_id')
        SITE_ID = 'your_site_id'  // Add if needed
    }
    parameters {
        string(name: 'DISPLAY_NAME', defaultValue: '', description: 'Name of the team to create')
    }
    stages {
        stage('Create Jira Team') {
            steps {
                script {
                    // Execute the Python script and capture the result
                    def result = sh(script: "python3 create_team.py ${params.DISPLAY_NAME}", returnStatus: true)
                    if (result != 0) {
                        error "Failed to create team or team already exists. Exit code: ${result}"
                    } else {
                        echo "Team created successfully!"
                    }
                }
            }
        }
    }
}
