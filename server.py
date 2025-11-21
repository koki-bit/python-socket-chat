import socket
import threading

# 1. 接続設定
HOST = '127.0.0.1' # 自分自身のPC（localhost）を表している。
PORT = 55555       # 通信に使うポート番号（空いている適当な数字）

# クライアントリスト（接続してきた人をここに記録する）
clients = []

def broadcast(message):
    """
    接続している全員にメッセージを送信する関数
    """
    for client in clients:
        try:
            client.send(message)
        except:
            #通信に失敗した（切断された）クライアントは削除
            client.remove(client)

def handle_client(client_socket):
    """
    個々のクライアントとの通信を担当する関数（スレッドごとに動く）
    """
    while True:
        try:
            # 2. クライアントからメッセージを受け取る（最大1024バイト）
            message = client_socket.recv(1024)
            if not message:
                break # メッセージが空なら切断されたとみなす

            # 3. 受け取ったメッセージを全員に転送（ブロードキャスト）
            broadcast(message)
        except:
            # エラーが起きたらループを抜ける
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    """
    サーバーを立ち上げるメイン関数
    """
    # 3. ソケット（通信の窓口）を作成
    # AF_INET: IPv4を使う, SOCK_STREAM: TCPを使う
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 4. ソケットにIPアドレスとポート番号を紐付ける（Bind）
    server.bind((HOST, PORT))

    # 5. 接続の待ち受けを開始（Listen）
    server.listen()
    print(f"[*] サーバーが起動しました。{HOST}:{PORT} で接続を待機中...")

    while True:
        # 6. クライアントからの接続を受け入れる（Accept）
        client_socket, addr = server.accept()
        print(f"[+] 新しい接続: {addr}")

        # クライアントリストに追加
        clients.append(client_socket)

        # 7. クライアントごとに新しいスレッドを立ち上げて通信を担当させる
        # これにより、メインのループはすぐに次の人を待ち受けらる。
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
