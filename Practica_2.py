#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket
import requests
import time
import struct
import _thread
import sys
import os
import operator, ast
import http.client

binOps = {
ast.Add: operator.add,
ast.Sub: operator.sub,
ast.Mult: operator.mul,
ast.Div: operator.floordiv,
ast.Mod: operator.mod
}


def E_0():
     s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s0.connect(('atclab.esi.uclm.es', 2000))
     d = (s0.recv(1024)).decode('utf-8')
     print (d)
     s0.close
     return (d)

def E_1():
     codigo= (E_0().split()[0])
     sUDP=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sUDP.bind(('', 1997))
     sUDP.sendto((codigo+" 1997").encode('utf-8'), ('atclab.esi.uclm.es', 2000))
     d1 =(sUDP.recv(1024)).decode('utf-8')
     print (d1)
     sUDP.close
     return (d1)

def E_2():


     def balanceo (line):
          while True:
               
               contA= 0
               contB= 0

               for i in line:

                     if i==")" or i=="]" or i=="}":
                         contB= contB + 1
                     if i=="(" or i=="[" or i=="{":
                         contA= contA + 1
                     
               
               if contA!=contB:
                    
                     falta= sArithmeticTCP.recv(1024).decode()
                     line= line + falta
               else: 
                     break

          return line      

     def arithmeticEval (s):

         #La función utilizada es la arithmeticEval de la siguiente URL:
         #http://stackoverflow.com/questions/20748202/valueerror-malformed-string-when-using-ast-literal-eval
    
    
          node = ast.parse(s, mode='eval')

          def _eval(node):
               if isinstance(node, ast.Expression):
                    return _eval(node.body)
               elif isinstance(node, ast.Str):
                    return node.s
               elif isinstance(node, ast.Num):
                    return node.n
               elif isinstance(node, ast.BinOp):
                    return binOps[type(node.op)](_eval(node.left), _eval(node.right))
               else:
                    raise Exception('Unsupported type {}'.format(node))

          return _eval(node.body)

          
     
     
     port= int(E_1().split()[0])
     sArithmeticTCP= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
     sArithmeticTCP.connect(('atclab.esi.uclm.es', port))
     
     while True:
          line= ""
          line = line + sArithmeticTCP.recv(1024).decode()
          
          if line[0]!= "(" and line[0]!= "[" and line[0]!= "{":
               print (line)
               sArithmeticTCP.close  
               return (line)
               break

          
          line = (balanceo(line))

          line = line.replace(']' , ')')
          line = line.replace('}' , ')')  

          line = line.replace('[' , '(')
          line = line.replace('{' , '(')
      
          calculo = arithmeticEval(line)
          encapsulado = "("+ str(calculo)+")"
          data =  encapsulado.encode()
          sent = sArithmeticTCP.send(data)
          

def E_3():

     code = E_2().split()[0] 
     conect = http.client.HTTPConnection('atclab.esi.uclm.es',5000)
     conect.request('GET',"/"+code,"")
     res = conect.getresponse()
     datas=res.read().decode()
     conect.close()
     return (datas)
    


def E_4(): 

	
    code = E_3().split()[0]
    
    print(code)
    
    Checksum = 0
    ICMP_ECHO = 8
    ID = 2015
    Sequence = 0
    cabecera = struct.pack("!BBHHH", ICMP_ECHO, 0, Checksum, ID, Sequence) 
 
    data = str(time.clock()) + code
    Checksum = checksum(cabecera + bytes(data,'ascii'))
    cabecera = struct.pack("!BBHHH", ICMP_ECHO, 0, Checksum, ID, Sequence)
    p = cabecera + bytes(data,'ascii')

    sICMP = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sICMP.sendto(p, (socket.gethostbyname('atclab.esi.uclm.es'), 32)) 

    msg = sICMP.recv (512)  
    msg = sICMP.recv(2048)[36:] 

    print (msg.decode())
    sICMP.close()
    return (msg.decode())
  
 
def checksum(s):

         cont1 = (int(len(s)/2))*2
         cont2 = 0
         sum = 0
         
         loByte = 0
         hiByte = 0

         while cont2 < cont1:
             if (sys.byteorder == "little"): 
                 loByte = s[cont2]
                 hiByte = s[cont2 + 1]
             else:
                 loByte = s[cont2 + 1]
                 hiByte = s[cont2]
             sum = sum + (hiByte * 256 + loByte)
             cont2 += 2
       
         
         if cont1 < len(s): 
             loByte = s[len(s)-1]
             sum += loByte
       
         sum &= 0xffffffff 
       
         sum = (sum >> 16) + (sum & 0xffff)    
         sum += (sum >> 16)                    
         resp = ~sum & 0xffff              
         resp = socket.htons(resp)
       
         return resp   


def proxy(ccon, caddr):

    port = 80 
    request = ccon.recv(1024).decode() 
    linethree = request.split('\n')[2].split(' ',2)[1]
    server = linethree.join(linethree.split()) 
  

    socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    socketserver.connect((server, port))
    socketserver.send(request.encode())


    while 1:

        data = socketserver.recv(2048) 
        
        if (len(data) > 0):

            ccon.send(data) 

        else:

            break

    socketserver.close()
    ccon.close()

def communication(proxycode,random):

    scom = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    scom.connect(( socket.gethostbyname('atclab.esi.uclm.es'),9000))
    codigo = proxycode + " " + str(random)

    scom.sendto(codigo.encode(), ( socket.gethostbyname('atclab.esi.uclm.es'), 7))
    msg= scom.recv(1024).decode()
    print (msg)

    scom.close()
    os._exit(0)

def E_5():

    

    ide = E_4().split()[0]
    sproxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sproxy.bind(('', 4600)) 
    sproxy.listen(30) 

    _thread.start_new_thread(communication, (ide,4600)) 

    while 1:
        ccon, caddr = sproxy.accept()
        _thread.start_new_thread(proxy, (ccon, caddr)) 

    
    sproxy.close()

def main():
    E_0()
    E_1()
    E_2()
    E_3()
    E_4()
    E_5()


main()



