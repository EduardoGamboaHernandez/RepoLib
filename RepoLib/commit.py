from .base import RepoInit
import git


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

    def get_commit_list(self, branch: str = "HEAD") -> list[any]:
        """
        obtiene los commits agrupados por fecha.

        Args:
            branch (str): rama a la que se consulta el historial.

        Returns:
            list[any]: lista de los commits agrupados por fecha.
        """
        commits = []
        try:
            commits = list(self.repo.iter_commits(branch))
        except git.exc.GitCommandError as e:
            print(e)
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
                date = commited_datetime.strftime("%Y-%m-%d")
            # agrupación de commits según la fecha establecida
            if commited_datetime.strftime("%Y-%m-%d") == date:
                commit_object = {
                    "hash": commit.hexsha,
                    "message": commit.message,
                    "author": commit.committer.name,
                    "stats": commit.stats.total,
                }
                commits_obj_list.append(commit_object)
            # si la fecha ya no coincide se agrega el diccionario
            # de los comiits a la lista final
            else:
                commits_dict = {"date": date, "commits": commits_obj_list}
                commits_list.append(commits_dict)
                # reinicio de la fecha y el diccionario con los commits agrupados
                commits_obj_list = []
                date = ""
        return commits_list

    def get_last_commit(self, branch: str = "HEAD") -> dict:
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
            "date": commit.committed_datetime.strftime("%Y-%m-%d"),
        }
        return commit_dict
