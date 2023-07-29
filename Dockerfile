FROM php:7.4-apache

# обновление системы
RUN apt-get update

# установка интерпретатора и зависимостей
RUN apt-get install -y python3 pip iputils-ping
