import git
import os


class BaseRepo:
    def __init__(self, name: str, path_repos: str) -> None:
        self.path_repos = path_repos
        self.name_repo = name
        self.repo_path = os.path.join(self.path_repos, f"{self.name_repo}.git")

class RepoInit(BaseRepo):
    def __init__(self, name, path_repos):
        super().__init__(name, path_repos)

        self.repo = git.Repo(self.repo_path)
