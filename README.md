# oss-leaderboard

Leaderboard for opensource contributors.

## Usage

#### Building

```bash 
$ docker build -t leaderboard .
```

```bash 
$ docker run --env-file .env leaderboard
```

## Development

#### Setting up the codebase

1. Clone the repository.

```bash
$ git clone git@github.com:leapfrogtechnology/oss-leaderboard.git
$ cd oss-leaderboard
```

2. Setup a virtualenv.

```bash
$ make venv
```

3. Activate the virtualenv.

```bash
$ source .venv/bin/activate
$ make setup
```

#### Running tests

```bash
$ make test
```

Note: This ensures all the dependencies are complete since tests are run in an isolated container.

## Contributing

Feel free to send pull requests.
Make sure to run following commands:
```bash
$ make format
$ make check
$ make test
```

## License

Licensed under [The MIT License](LICENSE).
