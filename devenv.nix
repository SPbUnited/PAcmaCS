{
  pkgs,
  lib,
  config,
  ...
}:
{
  # https://devenv.sh/packages/
  packages = [
    pkgs.jq
    pkgs.honcho
    pkgs.watchdog
    pkgs.protobuf
  ];

  # https://devenv.sh/languages/
  languages = {
    javascript = {
      enable = true;
      package = pkgs.nodejs_20;
    };

    python = {
      enable = true;
      package = pkgs.python313.withPackages (
        ps: with ps; [
          pandas
          pyyaml
          attrs
          cattrs
          pytest
          pyzmq
          protoletariat
          flask
          flask-socketio
          python-socketio
          python-engineio
          eventlet
          psutil
        ]
      );
    };
  };

  # See full reference at https://devenv.sh/reference/options/
}
