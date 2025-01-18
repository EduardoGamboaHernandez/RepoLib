from .base import BaseRepo
import git


class Bare(BaseRepo):
    """
    Esta clase ayuda a la inicialización de un repositorio bare,
    proporcionando un método sencillo para su creación con una descripción
    y la posibilidad de agregar un remoto de manera opcional.

    Args:
        name_repo: nombre del repositorio específico.
        path_repos: carpeta en donde se almacena los repositorios.
    """

    def __init__(self, name_repo: str, path_repos: str) -> None:
        super().__init__(name_repo, path_repos)

    def create(self, description: str, remote: list[str] = []) -> None:
        """
        creacion del repositorio bare

        Args:
            description (str): Descripción del repositorio.
            remote (list[str]): Repositorio remoto a agregar donde
                la posición 0 es el nombre y la posición 1 la URI.
        """
        repo_bare = git.Repo.init(self.path_repo, bare=True, mkdir=True)
        if description:
            repo_bare.description = description
        if remote:
            repo_bare.create_remote(remote[0], remote[1])
