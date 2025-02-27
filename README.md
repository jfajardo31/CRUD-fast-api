## Documentación IADRES
### Instalación y Configuración Local
Luego de clonar el proyecto desde git hub:
1. **Crear entorno**  
    **Windows**

        python -m venv env

    **Linux** 
    
        python3 -m venv env

2. **Activar entorno**  
    **Windows**
    
        env\Scripts\activate.bat  

    **Linux**
    
        source env/bin/activate

3. **Instalar paquetes desde requirements**

    **Windows**
        
            python -m pip install -r requirements.txt
            
    **Linux**
        
            python3 -m pip install -r requirements.txt

4. **Crear archivo .env** 

5. **Ejecutar proyecto**


        - Correr el servidor de fast-api
            uvicorn main:app --port 8000 --reload
        - Acceder al servidor local
            http://127.0.0.1:8000/docs (Cambiar puerto según necesidad)


### Instalación y Configuración (Servidor)
Verificar que cambios estén al día antes de dockerizar  
**Nota:** Se recomienda actualizar el requirements del proyecto por si hay cambios no guardados  
    **Windows**
    
        python -m pip freeze > requirements.txt

 
   **Linux**
        
        python3 -m pip freeze > requirements.txt

1. **Listar contenedores**  
    
        docker ps

2. **Doble compresión de archivos proyecto a cargar: .tar y luego .gzip** 
    
        tar -cvf paquete.tar iadres
        gzip -9 paquete.tar

        tar -czvf paquete.tar.gz iadres

3. **Enviar a servidor**  
    Se recomienda crear en el servidor una carpeta llamada Adres  
    **Nota:** Revisar usuario e IP del servidor a cargar
    
        scp paquete.tar.gz root@xx.x.x.xxx:Adres

3. **Descomprimir en el servidor**  
    Acceder al directorio Adres  
    **Verificar que haya subido el archivo**
    
        ls -l
    **Descomprimir el archivo .gzip**  
    
        tar -xf paquete.tar.gz

    **Nota:** Verificar previamente si hay archivos previos y borrar

        rm -r directorio

4. **Crear contenedor con balancedor nginx**  
    Acceder al directorio del proyecto (donde se encuentra el docker-compose) y ejecutar

        docker compose up --build --scale appiadres=5 -d
    
    **Nota:** Para comprobar los logs de algún contenedor

        docker logs nombrecontenedor

### Instalación y Configuración (Docker local)
Verificar que cambios estén al día antes de dockerizar  
**Nota:** Se recomienda actualizar el requirements del proyecto por si hay cambios no guardados  
    **Windows**
    
        python -m pip freeze > requirements.txt

   **Linux**
        
        python3 -m pip freeze > requirements.txt

1. **Listar contenedores**  
    
        docker ps 

2. **Listar imágenes**  
    
        docker image ls 

3. **Listar volúmenes**  
    
        docker volumen ls 

4. **Levantar contenedor**  
    Para levantar un contenedor se debe estar en la carpeta del proyecto (donde está el docker-compose)
    
        docker-compose up -d
        docker-compose up --build -d

5. **Destruir contenedor**  
    
        docker-compose down 

6. **Iniciar/detener contenedor**  
    
        docker-compose start
        docker-compose stop

7.  **Montaje recursos compartidos**

        sudo apt-get update
        sudo apt-get install cifs-utils
        sudo mkdir /mnt/IMG_Orion
        sudo mount -t cifs //10.0.4.53/IMG_Orion /IMG_Orion -o username=youruser,password=yourpassword


