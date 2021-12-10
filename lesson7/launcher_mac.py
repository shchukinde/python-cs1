#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import *
from subprocess import Popen
import subprocess
import time

clients=[]
server=''
pathOfFile=path.dirname(__file__)
pathServer=path.join(pathOfFile, "server.py")
pathClient=path.join(pathOfFile, "client.py")
pathToScriptServer = path.join(pathOfFile, "serv.sh")
pathToScriptListenClients = path.join(pathOfFile, "cl_l.sh")
pathToScriptSenderClients = path.join(pathOfFile, "cl_s.sh")
print (pathClient)

while True:
    choice = input("q - запуск сервера, w - остановка сервера, e - запуск 4 клиентов, r - остановка клиентов, t - остановить все, y - остановить все и выйти")
    

        
    if choice=="q":
        print ("Запустили сервер")
        server = Popen(f"open -n -a Terminal.app '{pathToScriptServer}'", shell=True)

    elif choice == "w":
        print ("Убили сервер")
        server.kill()
    elif choice =="e":
            print("Запустили клиенты")
            for i in range(1,3):
                clients.append(Popen(f"open -n -a Terminal.app '{pathToScriptListenClients}'", shell=True))
                #Задержка для того, что бы отправляющий процесс успел зарегистрироваться на сервере, и потом в словаре имен клиентов
                #остался только слушающий клиент
                time.sleep(0.5)
                clients.append(Popen(f"open -n -a Terminal.app '{pathToScriptSenderClients}'", shell=True))
                            
    elif choice == "r":
        for i in range(len(clients)):
            print(clients[i])
            clients[i].kill()
    elif choice == "y":
        for i in range(len(clients)):
            clients[i].kill()        
        server.kill()
        break
