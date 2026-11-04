# Casper Exchange — server deployment

Public URL: **https://exchange.kraken892.rest**. Server: `144.31.151.128`; application directory: `/opt/casper-exchange`.

The existing host nginx routes `exchange.kraken892.rest` to `127.0.0.1:5183`. Its existing `kraken892.rest`/`www.kraken892.rest` configuration and the `otzivi-backend-1` container are independent. Compose project `casper-exchange` has its own network, PostgreSQL volume and receipt volume. The API and PostgreSQL have no published host ports. Port 8000 remains assigned to the existing application.

The server environment is `/opt/casper-exchange/.env`, mode 600, with separate generated database/JWT/HMAC/admin secrets. The local development `.env` is unchanged. Operator credentials are also available locally in ignored `backups/server-exchange/access.txt`; they are not committed. Production started with the current site settings and 225 published reviews, plus a new administrator. Historical local accounts and tickets were not imported. Telegram is disabled, as in the local environment.

Run from `/opt/casper-exchange`:

```sh
# Status and logs
docker compose --env-file .env -f deploy/docker-compose.server.yml ps
docker compose --env-file .env -f deploy/docker-compose.server.yml logs --tail=100 backend

# Build services sequentially on this 2 GB server, then replace this project's containers
docker compose --env-file .env -f deploy/docker-compose.server.yml build backend
docker compose --env-file .env -f deploy/docker-compose.server.yml build frontend
docker compose --env-file .env -f deploy/docker-compose.server.yml up -d --no-build --wait

# Database backup; retain .env and the receipt volume separately
umask 077
docker compose --env-file .env -f deploy/docker-compose.server.yml exec -T postgres pg_dump -U exchange -d exchange -Fc > operations/postgres-backup.dump
```

The first database backup is `operations/postgres-initial.dump`. Source archive checksum, build logs and the original existing-site nginx configuration are in `operations/` (root access only). The source archive contains the current workspace, including Casper assets and animation changes that are newer than the last GitHub commit.

Host configuration: `/etc/nginx/sites-available/exchange.kraken892.rest`, linked from `sites-enabled`. Templates are in `deploy/nginx.exchange.http.conf` and `deploy/nginx.exchange.https.conf`. Validate with `nginx -t` before reloading nginx. Do not replace the existing site's vhost.

TLS: Let's Encrypt certificate `exchange.kraken892.rest`, using HTTP webroot `/var/www/letsencrypt`. Existing `certbot.timer` renews certificates automatically; this certificate's deploy hook validates and gracefully reloads nginx. Its renewal file is `/etc/letsencrypt/renewal/exchange.kraken892.rest.conf`.

To enable Telegram later, configure a fresh bot token and chat IDs in the operator settings or server environment, set `TELEGRAM_ENABLED=true` and recreate this project's backend. Public links already use the HTTPS subdomain through `PUBLIC_URL`.
