# Despliegue del Cluster de Kubernetes

## Nodos del cluster
Todos los nodos siguientes son maquinas independientes entre ellas, es decir, cada una de ellas está instalada por separado. Además, es importante que los nodos tengan conexion entre ellos para que los servicios funcionen de forma correcta. 
Esto se consigue mediante la red interna  _10.0.2.0/24_

De la interconexion interna de nuestro cluster de kubernetes no hay que preocuparse ya que eso está ya configurado en los archivos yml que se usan para el despliegue

* Nodo ```ansible```: Desde aquí es desde donde vamos a aprovisionar los demas nodos. El unico requisito de esta maquina es que tenga conexión con los demas nodos, y por su puesto, tener Ansible instalado. La IP de este nodo es la _10.0.2.9_
* Nodo ```master```: Este nodo va a ser el ques e va a encargar de lanzar todos los pods y los sertvicios correspondiente a nuestro despliegue. Desde aqui, vamos a poder ver log de los distintos servicios para entender que esta pasando. La IP de este nodo es la _10.0.2.7_
* Nodo ```agente```: Aquí es donde van a estar corriendo nuestros pods, los cuales en cada uno de ellos, va a estar un servicio distinto en ejecución. La IP de este nodo es la _10.0.2.8_
* Nodo ```NFS```: Este nodo es el que va a almacenar las persistencia de todo nuestro cluster, ya que va a tener tres exports diferentes. Uno para el servicio de Auth, otro para el de Blob, y otro para NGINX. La IP de este nodo es la _10.0.2.6_
* Nodo ```NGINX```: Último nodo de nuestro cluster. Va a ser el encargado de redirigir las peticiones a los distintos servicios internos de nuestro cluster.  La IP de este nodo es la _10.0.2.5_

## Ansible
El Cluster se configura de manera automática mediante Ansible, pero antes es preciso hacer algunas configuraciones en cada uno de los nodos anteriores. Son las siguientes.
* Copiar la clave SSH de la maquina desde donde se lanzará Ansible a los nodos que queremos aprovisionar. Para ello usamos ```ssh-copy-id <user>@<IP_Destino>```
* Dar permisos __sudo__ al user que va a usar Ansible para entrar en las maquinas, que en este caso es _ubuntu_. Para ello usamos el comando ```sudo usermod -aG sudo <user>```
* Hacer que no se requiera la contraseña al ejecutar _sudo_ desde el user que usará Ansible. Para ello ejecutamos ```sudo visudo```y añadimos ```<user> ALL=(ALL) NOPASSWD: ALL``` al final del archivo.

### Archivos de Ansible
Dentro del directorio de Ansible podemos ver que hay varios archivos y directorios, los cuales vamos a ir comentando uno a uno.
* Archivo ```ansible.cfg```: Este archivo es un pequeño archivo de configuración de Ansible. Nos especifica cual va a ser el archivo de inventario que se va a usar.
* Archivo ```inventory.yml```: Aquí es donde especificamos los nodos que se quieren aprovisionar junto a sus IPs. Tambien se especifica el user que se va a usar para que Ansible entre en cada nodo
* Archivo ```playbook.yml```: Mediante este archivo especificamos las tareas que se van a lanzar para cada nodo. En este caso se van a lanzar tareas para las maquinas con el rol __k3s__
* Directorio ```roles```: Aqui es donde se crean los directorios con los archivos de los diferentes roles de los nodos
* Directorio ```k3s```: Directorio donde están los archivos necesarios para los nodos con el rol __k3s__
* Directorio ```manifests```: Donde están presenten los archivos yml usados para el despligue de kuberentes
* Directorio ```nfs_files```: Directorio para almacenar los archivos necesarios para aprovisionar el nodo NFS
* Directorio ```nginx_files```: Donde está presente el archivo de configuracion de NGINX
* Directorio ```tasks```: Directorio donde esta las distintas tareas que tiene que ejecutar cada nodo
* Directorio ```vars```: Donde se almacena el archivo para variables globales que puede usar Ansible

De esta manera ya tenemos Ansible configurado para que pueda hacer todo lo necesario para desplegar las distintas herramientas de nuestro cluster en los distintos nodos, con lo que para iniciar el despliegue solo nos tenemos que colocarnos en el
directorio raiz de la carpeta _Ansible_ y ejecutar el comando ```ansible-playbook playbook.yml```

## Comprobación del correcto despliegue de nuestro cluster
Para comprobar que nuestro cluster de kubernetes se a lanzado de manera correcta, solo tenemos que entrar a la maquina __master__ y ejectar el comando ```kubectl get all```. De esta manera podemos ver todo el despliegue y verificar que todo está
corriendo de forma correcta.

### TrafficMix
Para verificar de forma mas completa el despliegue y los servicios se dispone de un trafficmix que efectúa varias peticiones predeterminadas. El trafficmix se puede ejecutar con el comando ```python3 trafficmix.py```, se puede lanzar desde el nodo ```ansible``` pero también es accesible desde fuera de la maquina virtual usando la ip de la maquina ```NGINX```