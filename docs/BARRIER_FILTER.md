# Barrier-Style Filter

The v0.1 barrier filter is an interpretable grid-search surrogate: it evaluates the one-step safety margin of candidate actions and chooses the closest candidate with nonnegative margin. It is **not** a general control-barrier-function QP solver and should not be described as one. A future version can add formally specified CBF constraints for supported dynamics.
