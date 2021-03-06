import discord


greeting_message = """
OneTimeChannelへようこそ。

**このサーバーについて**

このサーバーは、身内や個人間で話す時に、いちいちサーバーを立てるのがめんどくさい、という方向けに作成されました。
招待リンクを踏むだけで素早くそのチャンネルに参加できます。

**使用方法**

チャンネルを作成したい場合は、このメッセージに\U0001f44dリアクションを付与してください。
Botが自動的にチャンネルを作成し、閲覧可能にします。その他の細かい操作方法は、作成されたチャンネルの最初のメッセージで表示されます。
次に、その招待リンクを参加させたいユーザーに踏ませてください。その招待リンクを使うことで、チャンネルに参加できます。

すでに他のチャンネルに参加している場合、BotにDMで招待を送信することで参加可能です。もしくは、他のチャンネルに招待を送るとリアクションをおすことで参加できます。

**注意**
参加した時はdiscordの仕様により見れない可能性があります。メッセージをさらに表示もしくはリロードをお願いします。

**使われなくなったチャンネルについて**
`/delete`コマンドを使用すると自動で削除されます。

**プライバシーについて**

このサーバーはBotの<@698294955168497714>がオーナーになっており、その管理者は全てのチャンネルを閲覧できないようになっております。
また、このBotではメッセージの最終更新を測定する・コマンドを感知する以外にメッセージを保存するなどの動作は一切行っておりません。

**ご意見・ご要望がある場合**
`/main`コマンドを使用し、メインチャンネル群にある <#698313809588125867> にお書きください。

**招待url**
どのチャンネルにも入らないように入るには、この招待を使用してください。
https://discord.gg/qCKy9va
"""
owner_description = """
  **/everyone**
everyoneメンションを送信します。

  **/here**
hereメンションを送信します。

  **/invite**
そのチャンネルの招待を表示します。

  **/limit <人数>**
チャンネルに参加できる最大人数を制限します。-1にすると無効化されます。

  **/name <名前>**
チャンネルの名前を変更します。

  **/nsfw**
チャンネルをnsfwにする・解除します。

  **/voice**
ボイスチャンネルを作成します。

  **/refresh**
チャンネルの招待を新しくします。60秒に1回実行が可能です。

  **/kick <ユーザー名 or ユーザーid or メンション>**
すでにそのチャンネルに入っている指定したユーザーを退出させます。

"""
user_description = """
 **/main**
メインチャンネル群に接続します。

 **/help**
コマンド一覧を表示します。

 **/leave**
チャンネルから去ります。
"""


def first_message(member):
    embed = discord.Embed(title='チャンネル作成完了', description=f'{member.mention}が作成しました。')
    embed.add_field(name='作成者のみが使用可能なコマンド', value=owner_description)
    embed.add_field(name='全員が使用可能なコマンド', value=user_description)

    return embed


