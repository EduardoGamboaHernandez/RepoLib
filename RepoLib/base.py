import git
import os


class BaseRepo:
    """
    Esta clase es para poder encapsular información necesaria
    para manipular un repositorio Git bare.

    Args:
        name_repo: nombre del repositorio específico.
        path_repos: carpeta en donde se almacena los repositorios.

    Attributes:
        name_repo: nombre del repositorio específico.
        path_repos: carpeta en donde se almacena los repositorios.
        path_repos: ruta absoluta del repositorio.
    """

    def __init__(self, name_repo: str, path_repos: str) -> None:
        # nombre y directorio donde estan los repositorios
        self.path_repos = path_repos
        self.name_repo = name_repo

        # ruta completa del repositorio bare
        self.path_repo = os.path.join(self.path_repos, f"{self.name_repo}.git")


class RepoInit(BaseRepo):
    """
    Esta clase proporciona una interfaz simple para poder
    modificar o consultar datos de un repositorio bare.

    Args:
        name_repo: nombre del repositorio específico.
        path_repos: carpeta en donde se almacena los repositorios.

    Attributes:
        name_repo: nombre del repositorio específico.
        path_repos: carpeta en donde se almacena los repositorios.
        path_repos: ruta absoluta del repositorio.
        repo: objeto del repositorio
    """

    def __init__(self, name_repo, path_repos) -> None:
        super().__init__(name_repo, path_repos)

        # objeto del repositorio para manipular
        self.repo = git.Repo(self.path_repo)
