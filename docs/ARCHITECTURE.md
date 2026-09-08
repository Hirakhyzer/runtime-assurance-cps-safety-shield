# Architecture

The framework separates **estimation**, **nominal control**, **safety filtering**, and **plant evolution**. This separation allows the same runtime-assurance layer to wrap different controllers and CPS domains. The shield consumes a set-valued state estimate and never assumes that a single telemetry value is exact.

The primary v0.1 shield searches bounded actions by increasing distance from the nominal proposal and accepts the first candidate whose finite-horizon reachable boxes remain inside the declared safe set.
