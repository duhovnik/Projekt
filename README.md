Postup nasadenia a technologie pouzite v projekte:

- Github workflow - actions: https://github.com/duhovnik/Projekt/blob/main/.github/workflows/deploy.yml
   - Github workflow sa pusti automaticky po vytvoreni hore uvedeneho suboru a spusti sa bud po kazdom commite alebo ked sa triggerne rucne na stranke https://github.com/duhovnik/Projekt/actions 
   - Na githube sa vytvori virtualny ubuntu stroj, na ktorom sa nainstaluje checkout a packer balicek.
   - Na skryvanie tajomstiev/secrets pouzivam interny system Githubu na secrets, nepouzivam ansible vault ani hashicorp vault. https://github.com/duhovnik/Projekt/settings/secrets/actions. Pri odhalenom token api digital ocean tento token automaticky revokol.
   - Packer potom doinstaluje digital ocean plugin na spolupracu s API digital ocean: packer plugins install github.com/digitalocean/digitalocean
   - Nasledne sa spusti prikaz, ktory najskor zvaliduje a potom deployne template.json -->>> packer validate/build -var 'api_token=${{ secrets.DIGITAL_OCEAN_API_TOKEN }}' template.json

- Packer template spusteny z githubu deployne na Ubuntu virtualny stroj - digital ocean droplet - nasledovne akcie: https://github.com/duhovnik/Projekt/blob/main/template.json
  - stiahne website.zip do /tmp, zavola scripts/unpack_website.sh, ktory obsahuje instalaciu prikazu unzip, a vzapati rozbali archiv a zmaze ho
  - stiahne subory potrebne na spustenie dockeru -> 2x docker templaty, jedna pre web a druha pre databazu, docker compose.yaml subor, .env subor a inicializacny subor pre databazu, ktory sa nakopiruje do db kontajneru
  - potom sa spusti scripts/configureserver.sh, ktory obsahuje instalaciu docker a docker compose, a spusti prikazy docker compose build, docker compose up, ktore nastartuje oba kontajnery s aplikaciou
