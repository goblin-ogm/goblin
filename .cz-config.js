'use strict';

module.exports = {

  types: [
    {value: 'Feat',     name: 'feat:     A new feature'},
    {value: 'Git',      name: 'git:      changes to Git files'},
    {value: 'Fix',      name: 'fix:      A bug fix'},
    {value: 'Docs',     name: 'docs:     Documentation only changes'},
    {value: 'Style',    name: 'style:    Changes that do not affect the meaning of the code\n            (white-space, formatting, etc)'},
    {value: 'Refactor', name: 'refactor: A code change that neither fixes a bug nor adds a feature'},
    {value: 'Perf',     name: 'perf:     A code change that improves performance'},
    {value: 'Test',     name: 'test:     Adding missing tests or correcting existing tests'},
    {value: 'Build',    name: 'build:    Changes that affect the build system or external dependencies (example scopes: maven, gradle, npm, gulp)'},
    {value: 'CI',       name: 'ci:       Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)'},
    {value: 'Chore',    name: 'chore:    Other changes that dont modify src or test files'},
    {value: 'Revert',   name: 'revert:   Reverts a previous commit'}
  ],

  scopes: [
    {name: 'other'}
  ],

  scopeOverrides: {
    build: [
      {name: 'dependencies'},
      {name: 'versioning'},
      {name: 'release'},
      {name: 'build plugin'}
    ],
    ci: [
      {name: 'script'}
    ],
    chore: [
      {name: 'commitizen'},
      {name: 'editorconfig'},
      {name: 'git'}
    ],
    docs: [
      {name: 'API docs'},
      {name: 'repo'},
      {name: 'maven'}
    ]
  },

  allowCustomScopes: true,
  allowBreakingChanges: ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert']

};
