{
  python3Packages,
}:
let
  pyproject = builtins.fromTOML (builtins.readFile ./pyproject.toml);
in
python3Packages.buildPythonApplication {
  pname = pyproject.project.name;
  version = pyproject.project.version;
  src = ./.;
  pyproject = true;

  build-system = with python3Packages; [
    setuptools
    setuptools-scm
  ];

  dependencies = with python3Packages; [
    # your dependencies
  ];

  meta.mainProgram = "load-test-instruqt"; # Your script name to execute as command
}
