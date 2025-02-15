def proxy_thread(conn, client_addr):

  # get the request from browser
  request = conn.recv(MAX_DATA_RECV)

  # parse the first line
  first_line = request.split('n')[0]

  # get url
  url = first_line.split(' ')[1]

  if (DEBUG):
    print first_line
    print
    print "URL:", url
    print

  # find the webserver and port
  http_pos = url.find("://")          # find pos of ://
  if (http_pos==-1):
    temp = url
  else:
    temp = url[(http_pos+3):]       # get the rest of url

  port_pos = temp.find(":")           # find the port pos (if any)

  # find end of web server
  webserver_pos = temp.find("/")
  if webserver_pos == -1:
    webserver_pos = len(temp)

  webserver = ""
  port = -1
  if (port_pos==-1 or webserver_pos < port_pos):      # default port
    port = 80
    webserver = temp[:webserver_pos]
  else:       # specific port
    port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
    webserver = temp[:port_pos]

  print "Connect to:", webserver, port

  try:
    # create a socket to connect to the web server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((webserver, port))
    s.send(request)         # send request to webserver

    while 1:
      # receive data from web server
      data = s.recv(MAX_DATA_RECV)

      if (len(data) > 0):
        # send to browser
        conn.send(data)
      else:
        break
    s.close()
    conn.close()
  except socket.error, (value, message):
    if s:
      s.close()
    if conn:
      conn.close()
    print "Runtime Error:", message
    sys.exit(1)
