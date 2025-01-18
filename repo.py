from base import BaseRepo, RepoInit
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
        repo_bare = git.Repo.init(self.repo_path, bare=True, mkdir=True)
        if description:
            repo_bare.description = description
        if remote:
            repo_bare.create_remote(remote[0], remote[1])

        # inicializar el repositorio con el primer commit.
        repo_bare.index.commit("init: initial commit")


class Commit(RepoInit):
    """
    Esta clase proporciona una interfaz para obtener el historial
    de los commits de una rama especifica en un repositorio Git,
    permite la información de cada commit como el hash, el mensaje,
    autor, fecha y una estadística de cambios en el commit.
    Además, facilita la identificación y obtención del último
    commit hecho en una rama.

    Args:
        name_repo: nombre del repositorio específico.
        path_repos: carpeta en donde se almacena los repositorios.
    """
    def __init__(self, name_repo: str, path_repos: str) -> None:
        super().__init__(name_repo, path_repos)

    def get_commit_list(self, branch: str) -> list[any]:
        """
        obtiene los commits agrupados por fecha.

        Args:
            branch (str): rama a la que se consulta el historial.

        Returns:
            list[any]: lista de los commits agrupados por fecha.
        """
        commits = list(self.repo.iter_commits(branch))
        # lista que contienen todas las agrupaciones
        commits_list = []
        # fecha en formato año-mes-dia
        date = ""
        # commits_obj_list es una lista de los commits de una sola fecha
        commits_obj_list = []

        for commit in commits:
            commited_datetime = commit.committed_datetime
            # si no hay ninguna fecha a la que se está agrupando se crea una nueva
            if date == "":
                date = commited_datetime.strftime('%Y-%m-%d')
            # agrupación de commits según la fecha establecida
            if commited_datetime.strftime('%Y-%m-%d') == date:
                commit_object = {
                    "hash": commit.hexsha,
                    "message": commit.message,
                    "author": commit.committer.name,
                    "stats": commit.stats.total
                }
                commits_obj_list.append(commit_object)
            # si la fecha ya no coincide se agrega el diccionario
            # de los comiits a la lista final
            else:
                commits_dict = {
                    "date": date,
                    "commits": commits_obj_list
                }
                commits_list.append(commits_dict)
                # reinicio de la fecha y el diccionario con los commits agrupados
                commits_obj_list = []
                date = ""
        return commits_list

    def get_last_commit(self, branch: str) -> dict:
        """
        obtiene el ultimo commit hecho en una rama especifica.

        Args:
            branch (str): rama a la que se obtiene el commit.

        Returns:
            dict: el ultimo commit de la rama.
        """
        commit = list(self.repo.iter_commits(branch, max_count=1))[0]
        commit_dict = {
            "hash": commit.hexsha,
            "message": commit.message,
            "autor": commit.author.name,
            "date": commit.committed_datetime
        }
        return commit_dict


class Repo(RepoInit):
    """
    Esta clase obtiene información de un repositorio Git,
    permite acceder a su descripción, el nombre de las ramas
    existentes, el total de commits que se han hecho
    a la rama que apunta HEAD o a una rama especifica,
    a si como los tags registrados

    Args:
        name_repo: nombre del repositorio específico.
        path_repos: carpeta en donde se almacena los repositorios.
    """
    def __init__(self, name_repo: str, path_repos: str) -> None:
        super().__init__(name_repo, path_repos)

    def get_info(self, branch: str = 'HEAD'):
        """
        retorna un diccionario con la informacion de un repositorio

        Args:
            branch (str): rama a la que se obtiene el commit.

        Returns:
            dict: el ultimo commit de la rama.
        """
        info_repo = {}
        if self.repo.bare:
            info_repo = {
                "name": self.name_repo,
                "description": self.repo.description,
                "brranches": [branch.name for branch in self.repo.branches],
                "active_branch": self.repo.active_branch.name,
                "total_commits": len(list(self.repo.iter_commits(branch)))
            }
        return info_repo

    def get_tags(self) -> list[str]:
        """
        Devuelve una lista de los tags en una rama

        Returns:
            list[str]: una lista con los tags :)
        """
        tags = []
        if self.repo.bare:
            for tag in self.repo.tags:
                tags.append({
                    "name": tag.name,
                    "commit": tag.commit.hexsha
                })
        return tags
