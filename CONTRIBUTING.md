# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

## Merge request process

1. Branch from the `dev` branch. If you are implementing a feature name it `feature/name_of_feature`,
   if you are implementing a bugfix name it `bug/issue_name`.
2. Update the README.md and other documentation with details of changes to the interface, this includes new environment 
   variables, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Merge Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. Once you are ready for review please open a merge request to the `dev` branch.
5. You may merge the Merge Request in once you have the sign-off of two maintainers.

## Code style

- We name variables using one or two nouns in lowercase, e.g. `mapping_names` or `increment`.
- We name functions using verbs in lowercase, e.g. `map_variables_to_names` or `change_values`.

## Review process

1. When we want to release the package we will request a formal review for any non-minor changes.
2. The review process follows a similar process to ROpenSci.
3. Reviewers will be requested from associated communities.
4. Only once reviewers are satisfied will the `dev` branch be released.
