"""
Deployment/build script
"""
import sys
import subprocess
import uuid

def call(cmd_list):
    print('=>', *cmd_list)
    return subprocess.call(cmd_list)

def deploy():
    print("Adding fake launcher tag.")
    call(['touch', 'LAUNCHER_ENVIRONMENT'])
    print('=-'*4, ' The Untold Odyssey Deployer ', '=-'*4)
    if sys.platform in ('win32', 'win64'): print(":warning: You are running Windows. The build may fail.")
    version = input('Enter the version of this client: ')
    print(':info: Beginning building process; writing version to VER.')
    with open('VER', 'w') as file:
        file.write(version)
    
    print(':info: Committing to GitHub repository. Continue?')
    git_commit_confirm = input('[y/n] ').lower()
    if git_commit_confirm not in ('y', 'n'):
        print(':fatal: Expected `y` or `n` as result; got ',git_commit_confirm)
        exit(-1)
    
    if git_commit_confirm == 'y':
        commit_name = input('Provide name for commit (default=random uuid) ')
        if len(commit_name) < 1:
            print(':git warning: No commit name provided; defaulting to a randomly generated UUID.')
            commit_name = version+str(uuid.uuid4())

        # add files.
        print(':git: Adding files.')
        call(['git', 'add', '.'])

        # commit
        print(':git: Committing to local repository.')
        call(['git', 'commit', '-m', commit_name])

        if not sys.argv[0] == '--local-only' or sys.argv[0] == '-l':
            print("Commit to online repository?")
            git_push_confirm = input('[y/n] ').lower()

            if git_push_confirm not in ('y', 'n'):
                print(':fatal: Expected `y` or `n` as result; got ',git_push_confirm)
                exit(-1)
            if git_push_confirm == 'y':
                print(':git: Pushing to online repository. Here goes nothing!')
                commit_result = call(['git', 'push', 'origin', 'master'])
                print(':git: Done. Exiting with code ', commit_result)

    print('Build/compile the game?')
    do_build_confirm = input('[y/n] ').lower()

    if do_build_confirm not in ('y', 'n'):
        print(':fatal: Expected `y` or `n` as result; got', do_build_confirm)
    
    if do_build_confirm == 'y':
        print(':panda3d-build: Instructing Python to build the client.')
        call(['python3', 'setup.py'])
        

    print(':death: Cleaning up environment.')
    call(['rm', '-rf', 'LAUNCHER_ENVIRONMENT', '&&', 'rm', '-rf', 'build'])

if __name__ == '__main__':
    deploy()
