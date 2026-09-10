"""
Analysis fixture — mirrors DeadCode.cs
Contains an unreachable branch and an unused private function.

Techniques unlocked:
  - Dead Code Detection          (Unreachable Logic Identification)
  - Unreachable Path Detection   (Ghost Code Discovery)
  - Unreachable Use Detection    (Ghost Use Identification)
  - All Definition Coverage      (unused variable `_unused_var`)
"""


def _unused_private_function() -> None:
    """This function is never called — mirrors UnusedPrivateMethod in C#."""
    _unused_var = 42  # noqa: F841
    print(f"Ghost function: {_unused_var}")


def never_called_public_method() -> None:
    """Contains an unreachable branch — mirrors NeverCalledPublicMethod."""
    if False:  # noqa: SIM210
        print("Unreachable branch")
