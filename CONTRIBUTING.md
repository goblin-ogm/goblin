# Contributing

[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![SemVer](https://img.shields.io/badge/SemVer-v2.0.0-green)](https://semver.org/spec/v2.0.0.html)
[![Gitter](https://badges.gitter.im/goblin-ogm/goblin.svg)](https://gitter.im/goblin-ogm/goblin)


When contributing to this repository, it is usually a good idea to first discuss the change you
wish to make via issue, email, or any other method with the owners of this repository before
making a change. This could potentially save a lot of wasted hours.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Development

### Testing

In order to perform tests identical in nature to the integration tests we run then simply ensure you gave gitlab-runner installed then run the following command.

```bash
gitlab-runner exec docker test
```

Keep in mind this will run the tests on your local copy of the master branch so any changes not committed locally will be missed when testing.

### Commit Message Format

All commits on the repository repository follow the
[Conventional Changelog standard](https://github.com/conventional-changelog/conventional-changelog-eslint/blob/master/convention.md).
It is a very simple format so you can still write commit messages by hand. However it is
recommended developers install [Commitizen](https://commitizen.github.io/cz-cli/),
it extends the git command and will make writing commit messages a breeze.

Getting Commitizen installed is usually trivial, just install it via npm. You will also
need to install the cz-customizable adapter which the this repository is configured
to use. However the format is simple enough to use manually this makes it easier not to forget,
especially for developers not accustomed to the format yet.

```bash

npm install -g commitizen@2.8.6 cz-customizable@4.0.0
```

Below is an example of Commitizen in action. It replaces your usual `git commit` command
with `git cz` instead. The new command takes all the same arguments however it leads you
through an interactive process to generate the commit message.

![Commitizen friendly](http://aparapi.com/images/commitizen.gif)

Commit messages are used to automatically generate detailed changelogs, and to ensure
commits are searchable in a useful way. So please use the Commitizen tool or adhere to
the commit message standard or else we cannot accept Pull Requests without editing
them first.

Below is an example of a properly formated commit message.

```
chore(commitizen): Made repository Commitizen friendly.

Added standard Commitizen configuration files to the repo along with all the custom rules.

ISSUES CLOSED: #31
```

### Pull Request Process

1. Ensure that install or build dependencies do not appear in any commits in your code branch.
2. Ensure all commit messages follow the [Conventional Changelog](https://github.com/conventional-changelog/conventional-changelog-eslint/blob/master/convention.md)
   standard explained earlier.
3. Update the CONTRIBUTORS.md file to add your name to it if it isn't already there (one entry
   per person).
4. Adjust the project version to the new version that this Pull Request would represent. The
   versioning scheme we use is [Semantic Versioning](http://semver.org/).
5. Your pull request will either be approved or feedback will be given on what needs to be
   fixed to get approval. We usually review and comment on Pull Requests within 48 hours.

### Deploying to Pypi

1. Ensure version number in setup.py is correct. Note this is updated in both the version property and the download url.
2. Make sure any outstanding commits are pushed.
3. If a dist/ folder exists delete it.
4. Compile source distribution with `python setup.py sdist`
5. Compile binary distribution with `python setup.py bdist_wheel`
6. Check the packages for errors with `twine check dist/*`
7. Upload to Pypi using `twine upload dist/`
8. Create a tag for the current version such as `git tag -a v3.3,3 -m "version 3.3.3"`
9. Push the tag
10. Update the version in CHANGELOG.md and setup.py on master.
