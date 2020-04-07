# Contributing

When contributing to this repository, please first discuss the change you wish
to make via issue, email, or any other method with the owners of this
repository before making a change.

## Pull/merge request process

1. Branch from the `dev` branch. If you are implementing a feature name it
   `feature/name_of_feature`, if you are implementing a bugfix name it
   `bug/issue_name`.
1. Update the README.md and other documentation with details of major changes
   to the interface, this includes new environment variables, useful file
   locations and container parameters.
1. Once you are ready for review please open a pull/merge request to the
   `dev` branch.
1. You may merge the Pull/Merge Request in once you have the sign-off of two
   maintainers.
1. If you are merging `dev` to `master`, you must increment the version number
   in the VERSION file to the new version that this Pull/Merge Request would
   represent. The versioning scheme we use is [SemVer](http://semver.org/).


## Code style

- We name variables using few nouns in lowercase, e.g. `mapping_names`
  or `increment`.
- We name functions using verbs in lowercase, e.g. `map_variables_to_names` or
  `change_values`.
- We use the [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html)
  format for documenting features using docstrings.

## Review process

1. When we want to release the package we will request a formal review for any
   non-minor changes.
2. The review process follows a similar process to ROpenSci.
3. Reviewers will be requested from associated communities.
4. Only once reviewers are satisfied, will the `dev` branch be released.
