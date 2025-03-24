import git
import os


class RepoLib:
    """
    Esta clase sirve para crear y obtener información de un repositorio git bare

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

    def init(self):
        self.repo = git.Repo(self.path_repo)

    def get_info(self, branch: str = "HEAD"):
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
                "total_commits": len(list(self.repo.iter_commits(branch))),
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
                tags.append({"name": tag.name, "commit": tag.commit.hexsha})
        return tags

    def get_tree(self, commitSHA: str, iterate: bool = False) -> list:
        """
        retorna la estructura completa de archivos de un
        commit o solo los primeros archivos y carpetas

        Args:
            commitSHA (str): hexsha del comit para consultar
            iterate (str): sí es True devuelve el contenido total de archivos y carpetas

        Returns:
            dict: diccionario con el árbol de archivos del commit
        """

        def tree(tree_list) -> list:
            """funcion para hacer el arbol de archivos"""
            data = []
            for item in tree_list:
                # poner en el diccionario la información básica
                obj = {
                    "type": item.type,
                    "name": item.name,
                    "path": item.path,
                }
                # añadir información según el tipo de objeto que sea
                if item.type == "blob":
                    obj["size"] = item.size
                if item.type == "tree":
                    if iterate:
                        obj["content"] = tree(item)
                data.append(obj)
            return data

        commit = self.repo.commit(commitSHA)
        # formatear los datos en un diccionario con la función tree()
        tree = tree(commit.tree)
        return tree

    def get_file_content(self, commitSHA: str, filename: str) -> dict[str, str]:
        """
        retorna el contenido de un archivo de un commit.

        Args:
            commitSHA (str): hexsha del comit para buscar el archivo
            filename (str): nombre del archivo a consultar

        Returns:
            dict: diccionario con el nombre del archivo y su contenido
        """
        file_basename = os.path.basename(filename)
        commit = self.repo.commit(commitSHA)
        tree = commit.tree
        blob = tree[filename].data_stream
        # Decodificar a UTF-8, ajustar según la codificación
        content = str(blob.read().decode("utf-8"))
        return {"name": file_basename, "content": content}

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

        # diccionario que contiene en bruto los commits separados por fecha
        commits_by_date = {}
        # iteración para separar los commits
        for commit in commits:
            committed_datetime = commit.committed_datetime.strftime("%Y-%m-%d")

            if committed_datetime not in commits_by_date:
                commits_by_date[committed_datetime] = []

            commits_by_date[committed_datetime].append(
                {
                    "hash": commit.hexsha,
                    "message": commit.message,
                    "author": commit.committer.name,
                    "stats": commit.stats.total,
                }
            )

        # procesamiento de los commits a una lista
        for commits_date in commits_by_date.items():
            commits_list.append({"date": commits_date[0], "commits": commits_date[1]})
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

    def create(self, description: str = None, remote: list[str] = []) -> None:
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
