import socket, cv2, pickle, struct, imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
option = input("please choose, 1 for video and 2 for webcam\n")
print("LISTENING AT:", socket_address)
# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        if option == '1':
            vid = cv2.VideoCapture("lion.mp4")
        elif option == '2':
            vid = cv2.VideoCapture(0)
            vid.set(cv2.CAP_PROP_FPS, 5)
        else:
            exit()

        while vid.isOpened():
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)  # serialize frame to bytes
            message = struct.pack("Q", len(a)) + a  # pack the serialized data
            # print(message)
            try:
                client_socket.sendall(message)  # send message or data frames to client
            except Exception as e:
                print(e)
                raise Exception(e)

            cv2.imshow('TRANSMITTING VIDEO', frame)  # will show video frame on server side.
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
