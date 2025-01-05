Primero se ejecuta el script build_all.sh para construir las imagenes de los servicios y almacenarlas en docker.

Luego hay que pasarlas a k3s con el comando:
docker save tokensrv | sudo k3s ctr images import -

otra forma es creando primero un archivo tar

docker save -o tokensrv.tar tokensrv

para cargar las imagenes tar en k3s

sudo k3s ctr images import tokensrv.tar o usando el script import_images.sh si ya tienes creadas los tar de las imagenes.


Si fuera necesiario importar las imagenes a otros nodos usar send_images.sh

A mi me daba un problema y es que k3s me eliminaba las imagenes que importaba, por lo que al final hice un repositorio local en docker y accedia a las imagenes ahi. Luego resultaba que era porque se quedaba sin espacio y k3s me eliminaba las imagenes para liberar espacio. Si teneis suficiente espacio no deberia de daros problemas, pero en el archivo repoDocker.txt explico como hacer un repositorio local en docker para acceder a las imagenes desde ahi. 

Lo ideal seria en el futuro tener las imagenes subidas a un repositorio publico.
