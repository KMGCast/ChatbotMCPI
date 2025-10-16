FROM debian:bookworm-slim

# Inst. Dependencias + librerías
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
    apache2 \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    libmariadb-dev \
    libapache2-mod-wsgi-py3 \
    pkg-config \
    gcc \
    tzdata

# Zona Horaria
ENV TZ=America/Mexico_City
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Entorno python
WORKDIR /app
COPY ./requirements.txt /app/
RUN python3 -m venv /env
ENV PATH="/env/bin:$PATH"

# Librerías de Python
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt


COPY . /app/

# Confg Apache
COPY ./config_apache/000-default.conf /etc/apache2/sites-available/000-default.conf
RUN a2dissite 000-default.conf
RUN a2ensite 000-default.conf

# Puerto e inicio
EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]