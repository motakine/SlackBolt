# SlackBolt
 SlackアプリのためのBolt for Pythonを使ってなんかやる

## やりたいこと

なんか適当にSlack Botを作る。最終的にはherokuへデプロイとかしたい。

## 実行環境
- ぶっちゃけSpotifyAppと同じ環境でやってる
- Windows 10 Home
- Anaconda 4.10.1
- `conda list` :

```
# Name                    Version                   Build  Channel
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_0
charset-normalizer        2.0.7                    pypi_0    pypi
idna                      3.3                      pypi_0    pypi
oauthlib                  3.1.1                    pypi_0    pypi
openssl                   1.1.1l               h2bbff1b_0
pip                       21.0.1           py38haa95532_0
python                    3.8.12               h6244533_0
python-dotenv             0.19.2                   pypi_0    pypi
requests                  2.26.0                   pypi_0    pypi
requests-oauthlib         1.3.0                    pypi_0    pypi
setuptools                58.0.4           py38haa95532_0
six                       1.16.0                   pypi_0    pypi
slack-bolt                1.10.0                   pypi_0    pypi
slack-sdk                 3.11.2                   pypi_0    pypi
spotipy                   2.19.0                   pypi_0    pypi
sqlite                    3.36.0               h2bbff1b_0
tweepy                    4.3.0                    pypi_0    pypi
twitterapi                2.7.7                    pypi_0    pypi
urllib3                   1.26.7                   pypi_0    pypi
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wheel                     0.37.0             pyhd3eb1b0_1
wincertstore              0.2              py38haa95532_2
```

## 使い方
なんだろう

## 自分用メモ
### 公式系

- [Slack Your Apps][slack-apps]

### ドキュメント系

- [slack-boltのガイド？][slack-bolt-python-guides]
- [Boltでアプリを作る][slack-build-app-with-bolt]
- [Slackでリッチなテキストを書く][slack-rich-message]


## 作り方メモ

頑張れ！

### heroku

アカウントを作成し、アプリケーションを作成してSettingタブから設定を行う。

- `Config Vars` の `Reveal Config Vars` から環境変数を設定
  - GitHubとの連携でデプロイする場合、 **`.env`ファイルに含まれる環境変数は`.gitignore`で無視されるため反映されない！** ここでしっかり設定しておくこと。
- `Buildpacks` の `Add Buildpack` から `Python` を指定

buildに必要なファイルをプロジェクトルートに作成する。

- Procfile
  - Herokuでデプロイ時に実行するプロセスの定義。例： `pbot: python run.py`
    - これで `$ pbot` というコマンドで `$ python run.py` を呼び出せる。
  - `プロセス名の定義: 実行される処理` という感じ。プロセス名の定義は `web` 以外なら任意の文字列でOK、実行される処理はローカルと同じ実行コマンド。
- runtime.txt
  - 実行Pythonのバージョンの定義。例： `python-3.6.0`
  - 確認には `$ python -V` を使う。
- requirements.txt
  - Pythonの依存ライブラリの定義。例： `slackbot==0.4.1`
  - これは `pip install -r requirements.txt` でパッケージを一括でインストールできるやつ。
  - `pip freeze` で現在の環境にインストールされたパッケージとバージョンが出力されるが、リダイレクト `>` でファイルに出力できる。
  - つまり `pip freeze > requirements.txt` で生成されたものを置けばよい。
  - `conda` で似たようなことをする必要はない。

デプロイはHerokuのアプリのページの `Deploy` タブからGitHubを選び、連携を行うと楽。

- **但し今回の場合は後述の `Heroku CLI` で `heroku ps:scale pbot=1 --app <appname>` するか `Resources` タブから `pbot python app.py` の右側にあるスイッチをONにするかしてサーバ？を起動？しておかないとbotが動かない。**
  - なお `<appname>` はHerokuアプリの名前。URLの一部にもみられる。
- `Connect to GitHub` を押し、 `Authorize heroku` したらリポジトリを選択して `Connect` 。
- `Automatic deploys` ではリモートリポジトリの選択したブランチにpushしたものが自動的にデプロイされる。
- `Manual deploy` ではリモートリポジトリの選択したブランチを手動でデプロイできる。
  - 手動デプロイが終わると `Your app was successfully deployed.` `View` というボタンが出てきてクリックするが **これが罠でもある** 。

なお何かエラーなどがあった時の確認のためにコマンドラインインターフェースとやらをインストールしておいたほうがよい？

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line)とかいうのをインストールする
- Windowsのコマンドプロンプトでなんやかんや
  - `heroku --version` でバージョン確認
  - `heroku login` でブラウザに遷移してログイン

デプロイでbuildは通ってるくせに `View` すると `Application error An error occurred in the application and your page could not be served...` とかのエラーが出る。

- 検索すると、リポジトリをHerokuのリモートリポジトリに
- 同じ画面に `heroku logs --tail` でログをチェックできるとの記述があるのでコマンドプロンプトで実行すると `Error: Missing required flag: -a, --app APP  app to run command against` というエラーが。
- これは `heroku logs --tail` 自体のエラーで、正しくは `heroku logs --tail --app <appname>` とするのが正解らしい。[参考](https://stackoverflow.com/questions/48696878/missing-required-flag-heroku-tail)
  - ここで `<appname>` はHerokuアプリの名前。URLの一部にもみられる。
  - `heroku Error Missing required flag` とかで検索すると、Herokuのサーバにリポジトリを紐付けていないとかがよくヒットするが全く関係なかった。そもそも今回はGitHub連携でデプロイしており、その上で更に紐付けするのはマズそう。[参考](https://devcenter.heroku.com/articles/github-integration)のFAQの最初参照。
- それを実行すると、 `build` は成功しているものの、 `View` を押したタイミングで `at=error code=H14 desc="No web processes running"...` というエラーらしきものが出ている。
  - [公式ドキュメント](https://devcenter.heroku.com/articles/error-codes#h14-no-web-dynos-running)には `heroku ps:scale web=1` しろと書かれているが、今回はそれっぽいことをしても改善なし。そもそも `web` は特別なやつそうなので関係なさそう。
  - しかしこれまでの手順をきちんと踏んでいればslackbotは普通に動いている。
  - Webページを表示するようなプロセスが存在しなかった的な意味合い？
  - 結局気にしなくて良さそう。


## その他メモ

Herokuの参考：

- [Python x Herokuで作る 雑談slack bot](https://www.slideshare.net/dcubeio/python-heroku-slack-bot)
  - Herokuに上げるときに必要なファイルはこれを見よう。
- [PythonでSlackBot開発②「Herokuにデプロイする」](https://www.virtual-surfer.com/entry/2018/04/05/190000)
- [heroku 初級編 - GitHub から deploy してみよう -](https://qiita.com/sho7650/items/ebd87c5dc2c4c7abb8f0)
  - デプロイに関してはこれがよい。


<!-- Markdown links -->

[github-desktop]: https://desktop.github.com/ "GitHub Desktop"
[github-desktop-documents]: https://docs.github.com/ja/desktop "GitHub Desktopのドキュメント"
[github-desktop-documents-readme-md]: https://docs.github.com/ja/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes "GitHub Desktopのドキュメント：README.md"
[github-writing-markdown]: https://gist.github.com/LambdaNote/0d33b7d8284a3c99cffd1a5aa83c115f "GitHub: 記事の書き方"
[gitignore-qiita-1]: https://qiita.com/inabe49/items/16ee3d9d1ce68daa9fff "Qiita: .gitignore の書き方"
[gitignore-qiita-2]: https://qiita.com/anqooqie/items/110957797b3d5280c44f "Qiita: [Git] .gitignoreの仕様解説"
[heroku]: https://www.heroku.com/ "Heroku"
[python-environment-variable]: https://www.twilio.com/blog/environment-variables-python-jp "twilio BLOG: Pythonで環境変数を活用する"
[python-dotenv-documents]: https://pypi.org/project/python-dotenv/ "python-dotenv 公式ドキュメント"
[slack-apps]: https://api.slack.com/apps "Slack: Your Apps"
[slack-bolt-python-guides]: https://slack.dev/bolt-python/ja-jp/tutorial/getting-started "Slack: Bolt for Pythonガイド"
[slack-build-app-with-bolt]: https://api.slack.com/start/building/bolt-python "Building an app with Bolt for Python"
[slack-rich-message]: https://api.slack.com/messaging/composing/layouts "Creating rich message layouts"

