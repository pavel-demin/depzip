import os
import sys
from importlib import import_module


def contains(string, substrings):
    return any(s.casefold() in string.casefold() for s in substrings)


def bundle(modules=[], includes=[], excludes=[], output="bundle.zip"):
    directory = os.path.dirname(sys.executable)

    # Import modules to discover their dependencies

    for m in modules:
        import_module(m)

    dependencies = sys.modules.copy()

    for m in ["__main__", __name__]:
        dependencies.pop(m, None)

    # Collect files to bundle

    bundle = {v.__file__ for v in dependencies.values() if getattr(v, "__file__", None)}

    # Find and collect license files for bundled modules

    from importlib.metadata import distribution, packages_distributions

    packages = {k.split(".", 1)[0] for k in dependencies.keys()}
    mapping = packages_distributions()
    licenses = {"Python": {os.path.join(directory, "LICENSE.txt")}}

    for p in packages:
        for d in mapping.get(p, []):
            licenses.setdefault(d, set()).update(
                os.path.join(r, f)
                for r, _, files in os.walk(distribution(d)._path)
                for f in files
                if contains(f, ("license", "copying"))
            )

    # Collect DLLs to bundle

    from dllist import dllist

    for dll in dllist():
        if contains(os.path.basename(dll), ("vcruntime", "msvcp")):
            continue
        if os.path.commonpath([dll, directory]) == directory:
            bundle.add(dll)

    # Include additional files and directories

    for path in includes:
        path = path if os.path.exists(path) else os.path.join(directory, path)
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                bundle.update(os.path.join(root, f) for f in files)
        elif os.path.isfile(path):
            bundle.add(path)

    # Exclude specified files

    bundle = {f for f in bundle if not contains(f, excludes)}

    # Create the output zip file

    from zipfile import ZipFile, ZIP_DEFLATED

    with ZipFile(output, mode="w", compression=ZIP_DEFLATED) as zf:
        for d, files in licenses.items():
            for f in sorted(files):
                name = os.path.join("Licenses", d, os.path.basename(f))
                zf.write(f, name)
        for f in sorted(bundle):
            if os.path.isfile(f):
                name = os.path.relpath(f, directory) if os.path.isabs(f) else f
                zf.write(f, name)
