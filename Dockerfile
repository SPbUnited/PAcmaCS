FROM python:3.12-slim

WORKDIR /app

# Resolve fb4-NN.local via the host's avahi-daemon (socket mounted in docker-compose.yml)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libnss-mdns \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i 's/^hosts:.*/hosts:          files mdns4_minimal [NOTFOUND=return] dns/' /etc/nsswitch.conf

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["honcho", "-f", "Procfile.docker", "start"]