from database.migrations import up, down
import os
import sys
import services
from database import enum
import streamlit as st


args = sys.argv[1:]
if len(args) == 0:
    exit()

if args[0] == "up":
    if args[1]:
        up(int(args[1]))
    else:
        up(0)
if args[0] == "down":
    down()

if args[0] == "createsuperuser":
    name = input("name: ")
    email = input("email: ")
    password = input("password: ")
    services.auth.register(name, email, password, enum.сeo)

# if args[0] == "startapp":
#     pg = st(pages)
#     pg.run()