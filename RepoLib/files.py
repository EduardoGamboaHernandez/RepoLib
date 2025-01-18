from .base import RepoInit
import os


class Files(RepoInit):
    """
    Esta clase facilita el acceso la estructura de archivos
    y directorios que contiene un repositorio en una rama
    especifica, así como el contenido de un archivo cuando
    se especifica un commit hech

    Args:
        name_repo: nombre del repositorio específico.
        path_repos: carpeta en donde se almacena los repositorios.
    """

    def __init__(self, name_repo: str, path_repos: str) -> None:
        super().__init__(name_repo, path_repos)

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
