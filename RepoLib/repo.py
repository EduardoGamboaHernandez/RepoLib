from base import RepoInit


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
