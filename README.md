# Deployment of GDI starter kit at DE Node Notes 

## Set up at denbi cloud Heidelberg

- Created denbi.medium instance with Ubuntu 22.04 image with 100GB root filesystem volume.
- Installed official Docker following the [manual](https://docs.docker.com/engine/install/ubuntu/).
- Added the `ubuntu` user to the `docker` group (for running containers without being root):
```
sudo usermod -a -G docker ubuntu
```
- Add user public key on the denbi cloud OpenStack admin interface.
- Configure local `~/.ssh/config` following Denbi [documentation](https://cloud.denbi.de/wiki/Compute_Center/Heidelberg-DKFZ/), for example for user `luiz.gadelha` (user name can be found on denbi cloud admin interface on the profile section):
```
# Access to the de.NBI jumphost
Host denbi-jumphost-01.denbi.dkfz-heidelberg.de
  # Use your Elixir login name
  User luiz.gadelha
  # Use your ssh-key file
  IdentityFile /Users/lgadelha/.ssh/id_rsa
  # Open a SOCKS proxy locally to tunnel traffic into the cloud environment
  DynamicForward localhost:7777
  # Forward locally managed keys to the VMs which are behind the jumphosts
  ForwardAgent yes
  # Send a keep-alive packet to prevent the connection from beeing terminated
  ServerAliveInterval 120
# Access to de.NBI cloud floating IP networks via SOCKS Proxy
Host 10.133.24* 10.133.25*
  # Tunnel all requests through dynamic SOCKS proxy
  ProxyJump denbi-jumphost-01.denbi.dkfz-heidelberg.de
  # Use your ssh-key file
  IdentityFile /Users/lgadelha/.ssh/id_rsa
  # Forward locally managed keys
  ForwardAgent yes
  # Send a keep-alive packet to prevent the connection from beeing terminated
  ServerAliveInterval 120
```

## traefik proxy install

cd into the `traefik` directory
```
cp -r certs_example certs
```
copy your certificate file to the folder.
if the filenames are different than "fullchain.pem" and "privkey.pem" update the `dynamic_conf.yml` file

* Don't forget to set up a cronjob to update the certificate files when they are renewed

update the following line "traefik.http.routers.traefik.rule=Host(`traefik.gdi.dkfz.de`)" in `docker-compose.yml` with your hostname url  

```
docker compose up -d
```  
check the logs and the traefik dashboard to confirm the container is running as expected.

## Beacon install

The GDI Starter Kit Beacon is now using the official EGA Beacon v2 Reference Implementation repository instead of the [previous GDI fork](https://github.com/GenomicDataInfrastructure/starter-kit-beacon2-ri-api):

```
git clone https://github.com/EGA-archive/beacon2-ri-api.git
```

Follow instructions on Github repository: https://github.com/EGA-archive/beacon2-ri-api/blob/master/deploy/README.md.

### Data Beaconization

Followed instructions from the Beacon RI Tools v2 repository:

https://github.com/EGA-archive/beacon2-ri-tools-v2/blob/main/README.md

## LS AAI

First connect to jumphost 

```
ssh denbi-jumphost-01.denbi.dkfz-heidelberg.de
```

ssh to GDI SK VM:

```
ssh ubuntu@194.94.113.12
```

Add private key to ssh-agent:

```
ssh-add ~/.ssh/id_rsa
ssh-add -l
```

## Traefik

Start:

```
cd traefik_test
docker compose up -d
```

Can be accessed via browser in https://gdi.ghga.dev/



## LSAAI mock


Needs configuration on section "labels:" on docker-compose.yaml

```
cd starter-kit-lsaai-mock/

docker compose up -d
cp configuration/aai-mock/clients/sample-client.yaml configuration/aai-mock/clients/my-client.yaml
vi configuration/aai-mock/clients/my-client.yaml
# edit line -> client-id
# edit line -> redirect-uris
docker compose restart
vi configuration/aai-mock/application.properties
-main.oidc.issuer.url=http://localhost:8080/oidc/
-web.baseURL=https://localhost:8080/oidc
+main.oidc.issuer.url=http://194.94.113.12:80/oidc/
+web.baseURL=https://194.94.113.12:80/oidc
docker compose restart

#get code from the mock lsaai url
http://194.94.113.12/oidc/auth/authorize?response_type=code&client_id=juju_id
export code=CH2eTUralW6uyBDrpNAT1D

curl --location --request POST 'http://194.94.113.12:80/oidc/token' \--header 'Content-Type: application/x-www-form-urlencoded' \--data-urlencode 'grant_type=authorization_code' \--data-urlencode "code=$code" \--data-urlencode 'client_id=juju_id' \--data-urlencode 'client_secret=secret_value' \--data-urlencode 'scope=openid profile ga4gh_passport_v1 email'
to get the access token ^^^
```

## REMS

```
https://lsaai.gdi.ghga.dev/oidc/auth/authorize?response_type=code&client_id=rems_id&redirect_uri=https://rems.gdi.ghga.dev/oidc-callback
ME_CONFIG_BASICAUTH_USERNAME: ${MONGO_EXPRESS_USERNAME}
      ME_CONFIG_BASICAUTH_PASSWORD: ${MONGO_EXPRESS_PASSWD}

-h "Authorization: $token"

cd starter-kit-rems/
conda activate beaconV2
pip install "Authlib>=1.2.0"
python generate_jwks.py
docker compose up -d db
docker compose run --rm -e CMD="migrate" rems-app
docker compose up -d rems-app
export REMS_OWNER=jd123@lifescience-ri.eu # this is from starter-kit-lsaai-mock/configuration/aai-mock/userinfos/sample-user.yaml sub:
```

Create a rems client in lsaai client dir:

```
cat ../starter-kit-lsaai-mock/configuration/aai-mock/clients/rems-client.yaml

client-name: "rems client"
client-id: "rems_id"
client-secret: "secret_value"
  #redirect-uris: ["http://lsaai.gdi.ghga.dev:9009"]
redirect-uris: ["https://rems.gdi.ghga.dev/oidc-callback"]
token-endpoint-auth-method: "client_secret_basic"
scope: ["openid", "profile", "email", "ga4gh_passport_v1"]
grant-types: ["authorization_code"]
  #post-logout-redirect-uris: ["http://lsaai.gdi.ghga.dev:9009/post-logout"]
post-logout-redirect-uris: ["https://rems.gdi.ghga.dev"]
```

Edit config.edn
```
- :public-url "http://localhost:3000/"
+ :public-url "https://rems.gdi.ghga.dev/"

- :oidc-metadata-url "https://login.elixir-czech.org/oidc/.well-known/openid-configuration"
- :oidc-client-id ""
- :oidc-client-secret ""
+ :oidc-metadata-url "https://lsaai.gdi.ghga.dev/oidc/.well-known/openid-configuration"
+ :oidc-client-id "rems_id"
+ :oidc-client-secret "secret_value"
```


```
docker compose restart rems-app  # both lsaai and rems containers
check the logs to make sure it is running
docker compose logs rems-app
```

connect to rems db to check users and roles:
```
docker compose exec db psql -h localhost -U rems
```

Get admin access
```
export REMS_OWNER=jd123@lifescience-ri.eu
docker exec rems-app java -Drems.config=/rems/config/config.edn -jar rems.jar grant-role owner $REMS_OWNER
```

Go to the web interface administration page and create the following:
- organisation
- license
- forms
- workflow
- resources
- catalogue item

Create an api key

```
export API_KEY=rems_api_key
docker exec rems-app java -Drems.config=/rems/config/config.edn -jar rems.jar api-key add $API_KEY this is a test key
```

## Beacon

create a beacon client in lsaai mock

```
vi starter-kit-lsaai-mock/configuration/aai-mock/clients/beacon-client.yaml

#add the following lines
client-name: "Sample client"
client-id: "beacon_juju_id"
client-secret: "secret_value"
  #redirect-uris: ["http://lsaai.gdi.ghga.dev:9009"]
redirect-uris: ["https://beacon.gdi.ghga.dev"]
token-endpoint-auth-method: "client_secret_basic"
scope: ["openid", "profile", "email", "ga4gh_passport_v1"]
grant-types: ["authorization_code"]
  #post-logout-redirect-uris: ["http://lsaai.gdi.ghga.dev:9009/post-logout"]
post-logout-redirect-uris: ["https://beacon.gdi.ghga.dev/post-logout"]

cd beacon2-ri-api/

cd permissions

vi .env
# the following line
CLIENT_SECRET='secret_value'
cLIENT_ID='beacon_juju_id'
```

https://beacon.gdi.ghga.dev/api/datasets
