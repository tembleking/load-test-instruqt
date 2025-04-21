{
  python3Packages,
  makeWrapper,
  playwright-driver,
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
    playwright
    faker
  ];

  nativeBuildInputs = [
    makeWrapper
  ];

  buildInputs = [ playwright-driver.browsers ];

  postFixup = ''
    wrapProgram $out/bin/load-test-instruqt \
      --set-default PLAYWRIGHT_BROWSERS_PATH ${playwright-driver.browsers} \
      --set-default PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS true
  '';

  meta.mainProgram = "load-test-instruqt"; # Your script name to execute as command
}
