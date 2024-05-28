### Steps to Collaborate on GitHub

1. Fork repository from source and create copy under my GitHub account

2. Clone forked repository to local machine

    git clone https://github.com/YOUR_USERNAME/YOUR_FORKED_REPO.git

3. Set up repository as remote. In this ecample, the source repository is remote named **upstream**

    cd YOUR_FORKED_REPO
    git remote add upstream https://github.com/FRIEND_USERNAME/FRIEND_REPOSITORY.git

4. Before making changes, make sure the local repository is synced to the remote repository. Then resolve conflicts and push the updated branch to your fork on GitHub

    git fetch upstream
    git checkout main
    git merge upstream/main
    git push origin main

5. Make your changes

    git checkout -b my-feature-branch   # Create new branch for your fix
    git add .
    git commit -m "Description of my changes"
    git push origin my-feature-branch

6. Create pull request. Go to your forked repository on GitHub, create a pull request to merge into source branch

- Ensure the base repository is source (USERNAME/REPOSITORY/main or master)
- Ensure the head repository is your fork (YOUR_USERNAME/YOUR_FORKED_REPO)


###### Summary

- Fork the repository once: Create a personal copy of the repository on GitHub.
- Clone your fork: Bring the repository to your local machine.
- Set up the original repository as a remote: This helps you keep your fork up-to-date with the original repository.
- Sync your fork: Regularly update your fork with changes from the original repository.
- Work on feature branches: Create separate branches for each feature or fix you work on.
- Create pull requests: Propose your changes to be merged into the original repository.


###### Detailed Commands

Coming soon