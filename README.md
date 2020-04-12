# fetchmovie

fetch movies url or torrents

## sites supported

- [x] [bbt](https://bbt.tv)
- [ ] [btdx8](https://www.btdx8.com/)
- [ ] [dygod](https://www.dy2018.com/)

## install

```shell script
pip install fetchmovie
```

## USAGE

### show help

```sh
fetchmovie -h
Usage: fetchmovie [OPTIONS]

Options:
  -n, --name TEXT      movie name [OPT] -n <name>
  -s, --site TEXT      site name [OPT] -s <site_name>
  -w, --overwrite      overwrite local cache [OPT] -w
  -img, --display_img  display with image [OPT] -img
  -h, --help           Show this message and exit.
```

### fetch by name

> simple search

![by_name](docs/images/by_name.png)

> with image supported

![with_img](docs/images/with_img.png)
