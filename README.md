# yandex-ege

CLI to get collection and task answers for [YandexEGE](https://education.yandex.ru/ege)

## 📦 Installing

### Via [uv](https://docs.astral.sh/uv) (recommended)

```sh
uv tool install git+https://github.com/ZUB3C/yandex-ege.git
```

### Via [pipx](https://pipx.pypa.io)

```sh
pipx install git+https://github.com/ZUB3C/yandex-ege.git
```

## Usage

```text
Usage: yandex-ege [OPTIONS] URLS...


╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    urls      URLS...  Collection and/or task urls. [default: None] [required]                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --timeout                                      INTEGER  Request timeout in seconds. [default: 10]                                                          │
│ --global-heading        --no-global-heading             Print global heading before all answers. [default: no-global-heading]                              │
│ --redirects             --no-redirects                  Allow links which redirects to education.yandex.ru [default: redirects]                            │
│ --install-completion                                    Install completion for the current shell.                                                          │
│ --show-completion                                       Show completion for the current shell, to copy it or customize the installation.                   │
│ --help                                                  Show this message and exit.                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Usage example

```sh
yandex-ege https://education.yandex.ru/ege/task/a59f3bdb-ccef-4a7f-b2d8-1bf3b3982a40
```
