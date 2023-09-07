# Tackle-DiVA (Data-intensive Validity Analyzer)

Tackle-DiVA is a command-line tool for data-centric application analysis. It imports a set of target application source files (*.java/xml) and provides following analysis result files.

- Service entry (exported API) inventory 
- Database inventory
- Transaction inventory
- Code-to-Database dependencies (call graphs)
- Database-to-Database dependencies
- Transaction-to-Transaction dependencies
- Transaction refactoring recommendation.

![Overview](./docs/diva-overview.png)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkonveyor%2Ftackle-diva.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkonveyor%2Ftackle-diva?ref=badge_shield)

## Prerequisites
- Docker runnable environment (e.g. RHEL, Ubuntu, macOS)


## Getting Started

Supposed that `tackle-diva` is cloned to `/tmp`,

0. Build docker image for diva.
```
$ cd /tmp/tackle-diva/
$ docker build . -t diva
```

1. Prepare source codes of target Java applications whose Java framework is supported in DiVA, such as [DayTrader7](https://github.com/WASdev/sample.daytrader7) and [TradingApp](https://github.com/saud-aslam/trading-app).
   
```
$ cd /tmp
$ git clone https://github.com/WASdev/sample.daytrader7.git
```

2. Move to `tackle-diva/distrib/bin/` directory, and execute `diva_docker` command attaching directory full path.

```
$ cd /tmp/tackle-diva/distrib/bin/
$ ./diva_docker /tmp/sample.daytrader7/
```

3. Check `tackle-diva/distrib/output` directory and confirm analysis result files
```
$ ls /tmp/tackle-diva/distrib/output
contexts.yml            transaction.json        transaction_summary.dot
database.json           transaction.yml         transaction_summary.pdf
```

## Analysis Results
An `output` directory for storing analysis result files:

- `contexts.yml`: Extracted application service entries
- `database.json`: Extracted database tables
- `transaction.json/yml`: Extracted transactions that expresses as a sequence of service entry, call graphs, SQLs
- `transaction_summary.dot/pdf`: Extracted database-to-database/transaction-to-transaction dependencies and recommended transaction refactoring.

## Supported Java Frameworks

- Spring Boot (e.g. [TradingApp](https://github.com/saud-aslam/trading-app))
- Servlet  (e.g. [DayTrader7](https://github.com/WASdev/sample.daytrader7))
  
The other frameworks to be supported.

## Materials

- [opensource.com article](https://opensource.com/article/21/6/tackle-diva-kubernetes)
- [Youtube recording](https://youtu.be/UJi1tGFMw2M)


## Code of Conduct
Refer to Konveyor's Code of Conduct [here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkonveyor%2Ftackle-diva.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkonveyor%2Ftackle-diva?ref=badge_large)