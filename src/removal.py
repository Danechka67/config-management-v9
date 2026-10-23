"""Команда rm: изменяет только виртуальные узлы в памяти."""


def parse_rm(args):
    """Разобрать флаги -r/-R/-f, их комбинации и разделитель --."""
    recursive, force, options = False, False, True
    names = []
    for arg in args:
        if options and arg == "--":
            options = False
        elif options and arg.startswith("-") and arg != "-":
            recursive, force = _merge_rm_flags(arg, recursive, force)
        else:
            options = False
            names.append(arg)
    if not names and not force:
        raise ValueError("использование: rm [-r] [-f] [--] путь...")
    return recursive, force, names


def _merge_rm_flags(arg, recursive, force):
    """Проверить опцию rm и дополнить уже установленные флаги."""
    flags = set(arg[1:])
    if not flags or flags - set("rRf"):
        raise ValueError(f"неизвестная опция rm: {arg}")
    return recursive or bool(flags & set("rR")), force or "f" in flags


def _check_protected_path(path, cwd):
    """Запретить удаление корня, текущего каталога и его предков."""
    if path == "/" or cwd == path or cwd.startswith(path + "/"):
        raise ValueError("нельзя удалить корень/текущий каталог/предка")


def removal_targets(vfs, cwd, names, recursive, force):
    """Проверить все пути до удаления; защитить корень и текущий каталог."""
    targets = set()
    for name in names:
        path = vfs.resolve(name, cwd)
        _check_protected_path(path, cwd)
        if path not in vfs.nodes and force:
            continue
        node = vfs.require(path)
        if node.kind == "dir" and not recursive:
            raise ValueError(f"для каталога требуется rm -r: {path}")
        targets.add(path)
        if recursive:
            targets.update(item for item in vfs.nodes
                           if item.startswith(path + "/"))
    return targets


def remove(vfs, cwd, args):
    """Атомарно удалить проверенные узлы; CSV на диске не трогать."""
    recursive, force, names = parse_rm(args)
    targets = removal_targets(vfs, cwd, names, recursive, force)
    for path in targets:
        del vfs.nodes[path]
    return ""
