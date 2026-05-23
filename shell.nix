let
  # We pin to a specific nixpkgs commit for reproducibility.
  # Last updated: 2024-04-29. Check for new commits at https://status.nixos.org.
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/687f05a9184cad4eaf905c48b63649e3a86f5433.tar.gz") {};
in
  pkgs.mkShell {
    packages = with pkgs; [
        nodejs_20
        jq
        honcho
        # foreman
        watchdog
        protobuf
      (pkgs.python313.withPackages (python-pkgs:
        with python-pkgs; [
          # select Python packages here
        #   pandas
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
        ]))
    ];
  }
