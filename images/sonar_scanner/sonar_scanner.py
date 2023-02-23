import os 

def config():
    global git_token
    git_token=os.environ['gitkey']
    global repo
    repo=os.environ['repo']
    global branch
    branch=os.environ['branch']
    global git_username
    git_username=os.environ['git_un']
    global sonar_projectkey
    sonar_projectkey=os.environ['sonar_projectkey']
    global sonar_token
    sonar_token=os.environ['sonar_token']
    global sonar_url
    sonar_url=os.environ['host']
    global scm_source
    scm_source=os.environ['scm_source']

def debug():
    global repo
    repo='devops/waycool2.0_demo'
    global git_token
    git_token=''
    global sonar_projectkey
    sonar_projectkey='waycool2odemo'
    global sonar_token
    sonar_token=''
    global sonar_url
    sonar_url='https://sonarqube.censanext.com'
    global branch
    branch='master'
    global git_username
    git_username='mithun'

if __name__=="__main__":
    config()

    os.system('git clone'+' --branch '+branch+' https://'+git_username+':'+git_token+'@'+scm_source+'/'+repo+'.git')

    os.system('sonar-scanner/bin/sonar-scanner -Dsonar.projectKey='+sonar_projectkey+' -Dsonar.host.url='+sonar_url+' -Dsonar.sources='+repo.split('/')[1]+' -Dsonar.login='+sonar_token )