import json
import socket
import time
import io
import errno


class CommServer:
    def __init__(self):
        # self.elapsed = 0
        # self.filename = ''
        self.setup_conn()

    def setup_conn(self):
        # TCP/IP 구성 정보를 로드
        global tcp_config
        global channel
        # global conn
        global interval

        try:
            with open('../tcp_config.json', encoding='utf-8') as json_file:
                tcp_config = json.load(json_file)

            host = tcp_config['hostname']
            port = tcp_config['port']
            interval = tcp_config['interval']
            channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            channel.bind((host, port))
            channel.listen(1)
            # conn, addr = channel.accept()
        except FileNotFoundError:
            print("No File exists...")
            exit('socket configuration exception')
        except OSError as ex:
            print("OSError... ", ex.__cause__)
            exit('port exception')

    def send_data(self):
        STX = 2
        # filename = '/Users/andrew/Documents/롯데홈쇼핑RPA/2차프로젝트준비/속기data금지어심의/190812_1540  스킨테크놀로지 의료기기 풀 패키지.txt'
        # with io.open(filename, 'r', encoding='cp949') as text_file:
        #     contents = text_file.readlines()

        while True:
            conn, addr = channel.accept()

            filename = '/Users/andrew/Documents/롯데홈쇼핑RPA/2차프로젝트준비/속기data금지어심의/190812_1540  스킨테크놀로지 의료기기 풀 패키지.txt'
            with io.open(filename, 'r', encoding='cp949') as text_file:
                contents = text_file.readlines()

            for content in contents:
                content = content.replace('-', '')
                content = content.replace('.', '')
                content = content.replace('\n', '')
                # print("From file..", content)
                if len(content) < 5:
                    continue

                try:
                    comm_data = bytearray(200)
                    comm_data[0] = STX
                    send_data = str.encode(content, encoding='cp949')
                    comm_data[1] = len(send_data)
                    comm_data[2:] = bytearray(send_data)
                    conn.send(comm_data)
                    print('Sent...:', comm_data)
                except socket.error as e:
                    print ("error while sending :: " + str(e), errno)
                    if e.errno == errno.EPIPE:
                        break
                    else:
                        raise
                        # exit("terminating")

                time.sleep(interval)


if __name__ == '__main__':
    server = CommServer()
    server.send_data()