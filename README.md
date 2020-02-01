# [![Goblin Header](http://goblin-ogm.com/goblin-header-forlight.png)](http://goblin-ogm.com)

[![tests](http://git.qoto.org/goblin-ogm/goblin/badges/master/pipeline.svg)](http://git.qoto.org/goblin-ogm/goblin/commits/master)
[![Requirements](https://requires.io/github/goblin-ogm/goblin/requirements.svg?branch=master)](https://requires.io/github/goblin-ogm/goblin/requirements/?branch=master)
[![test coverage](http://git.qoto.org/goblin-ogm/goblin/badges/master/coverage.svg)](http://git.qoto.org/goblin-ogm/goblin/commits/master)
[![codecov](https://codecov.io/gh/goblin-ogm/goblin/branch/master/graph/badge.svg)](https://codecov.io/gh/goblin-ogm/goblin)
[![Codacy](https://api.codacy.com/project/badge/Grade/7d7e40a92482485c851e303cfbf5eb39)](https://www.codacy.com/gh/goblin-ogm/goblin)
[![Scrutinizer](https://img.shields.io/scrutinizer/quality/g/goblin-ogm/goblin/master.svg?style=flat)](https://scrutinizer-ci.com/g/goblin-ogm/goblin)

[![PyPi](https://img.shields.io/pypi/v/goblin.svg?style=flat)](https://pypi.python.org/pypi/goblin)
[![Supported Versions](https://img.shields.io/pypi/pyversions/goblin.svg?style=flat)](https://pypi.python.org/pypi/goblin)
[![Downloads](https://img.shields.io/pypi/dm/goblin.svg?style=flat)](https://pypi.python.org/pypi/goblin)
[![SemVer](https://img.shields.io/badge/SemVer-v2.0.0-green)](https://semver.org/spec/v2.0.0.html)
[![docs](https://readthedocs.org/projects/goblin/badge/?version=latest)](https://goblin.readthedocs.io/en/latest/)
[![Gitter](https://badges.gitter.im/goblin-ogm/goblin.svg)](https://gitter.im/goblin-ogm/goblin)

# Goblin OGM on top of [TinkerPop 3](http://tinkerpop.apache.org/)


**Licensed under the Apache Software License v2**

The original Goblin was a TinkerPop 3 ready port of Cody Lee's mogwai, an excellent library that had been developed for use with pre-TinkerPop 3 versions of Titan. We designed Goblin to provide asynchronous programming abstractions that would work using any version of Python 2.7 + with a variety of asynchronous I/O libraries (Tornado, Asyncio, Trollius). While in theory this was great, we found that in our effort to promote compatibility we lost out on many of the features the newer Python versions provide to help developers deal with asynchronous programming. Our code base became large and made heavy use of callbacks, and nearly all methods and functions returned some sort of `Future`. This created both a clunky user API, and a code base that was difficult to reason about and maintain.

So, we decided to rewrite Goblin from scratch...

Goblin is built directly on top of TinkerPop and allows access to all of the internals. This ensures all the
TinkerPop features are available to the end-user. The TinkerPop stack provides several tools which can be used to work
with Goblin.

* **Gremlin**, a database agnostic query language for Graph Databases.
* **Gremlin Server**, a server that provides an interface for executing Gremlin on remote machines.
* a data-flow framework for splitting, merging, filtering, and transforming of data
* **Graph Computer**, a framework for running algorithms against a Graph Database.
* Support for both **OLTP** and **OLAP** engines.
* **TinkerGraph** a Graph Database and the reference implementation for TinkerPop.
* Native **Gephi** integration for visualizing graphs.
* Interfaces for most major Graph Compute Engines including **Hadoop M/R**. **Spark**, and **Giraph**.

Goblin also supports any of the many databases compatible with TinkerPop including the following.

 * [JanusGraph](http://janusgraph.org/)
 * [Titan](http://thinkaurelius.github.io/titan/)
 * [Neo4j](http://neo4j.com)
 * [OrientDB](http://www.orientechnologies.com/orientdb/)
 * [MongoDB](http://www.mongodb.org)
 * [Oracle NoSQL](http://www.oracle.com/us/products/database/nosql/overview/index.html)
 * TinkerGraph

 Some unique feature provided by the Goblin OGM include:

* High level asynchronous *Object Graph Mapper* (OGM)
* Integration with the *official gremlin-python Gremlin Language Variant* (GLV) - now provided by [aiogremlin](http://git.qoto.org/goblin-ogm/aiogremlin)
* Native Python support for asynchronous programing including *coroutines*, *iterators*, and *context managers* as specified in [PEP 492](https://www.python.org/dev/peps/pep-0492/)
* *Asynchronous Python driver* for the Gremlin Server - now provided by [aiogremlin](https://git.qoto.org/goblin-ogm/aiogremlin)
* Async `Graph` implementation that produces *native Python GLV traversals* - now provided by [aiogremlin](https://git.qoto.org/goblin-ogm/aiogremlin)

## Donating

[![Librepay](http://img.shields.io/liberapay/receives/goblin-ogm.svg?logo=liberapay)](https://liberapay.com/goblin-ogm/donate)

As an open-source project we run entierly off donations. Buy one of our hardworking developers a beer by donating with one of the above buttons. All donations go to our bounty fund and allow us to place bounties on important bugs and enhancements.

## Support and Documentation

The official homepage for the project is at [http://goblin-ogm.com](http://goblin-ogm.com). The source is officially hosted on [QOTO GitLab here](https://git.qoto.org/goblin-ogm/goblin) however an up-to-date mirror is also maintained on [Github here](https://github.com/goblin-ogm/goblin).

Documentation: [latest](http://goblin-ogm.qoto.io/goblin)

For support please use [Gitter](https://gitter.im/goblin-ogm/goblin) or the [official Goblin mailing list and Discourse forum](https://discourse.qoto.org/c/PROJ/GOB).

Please file bugs and feature requests on [QOTO GitLab](https://git.qoto.org/goblin-ogm/goblin/issues) our old archived issues can still be viewed on [Github](https://github.com/davebshow/goblin/issues) as well.

Aparapi conforms to the [Semantic Versioning 2.0.0](http://semver.org/spec/v2.0.0.html) standard. That means the version of a release isnt arbitrary but rather describes how the library interfaces have changed. Read more about it at the [Semantic Versioning page](http://semver.org/spec/v2.0.0.html).

## Related Projects

This particular repository only represents the one component in a suite of libraries. There are several other related repositories worth taking a look at.

* [AIO Gremlin](https://git.qoto.org/goblin-ogm/aiogremlin) - An asynchronous Gremlin DSL for gremlin-python.
* [Goblin Buildchain](https://git.qoto.org/goblin-ogm/goblin-buildchain) - Docker image containing all the needed tools to build and test Goblin.
* [Python Gremlin Server](https://git.qoto.org/goblin-ogm/gremlin-server-python) - Vanilla Gremlin-server with Python Script Engine loaded, used for integration testing.
