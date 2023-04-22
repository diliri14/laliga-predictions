## Instalación

1. Crear el ambiente en cada proyecto. Entrar en la carpeta del proyecto.
   `env` es el nombre que le quieres dar a ese ambiente
   `py -m venv env`

   Esto crea una nueva carpeta con el nombre del ambiente

2. Activar el ambiente
   `.\env\Scripts\activate.bat` en Windows

   Esto crea una nueva etiqueta en la terminal con el nombre del ambiente.

3. Salir del ambiente virtual
   `.\env\Scripts\deactivate.bat` en Windows

4. Podemos instalar las librerias necesarias en el ambiente virtual como por ejemplo
   `pip3 install flask`

5. Verificar las instalaciones
   `pip3 freeze`

6. Opcional: Crear el archivo requirements.txt para agregar todas las dependencias del proyecto y ejecutarlo desde allí.

- Escribir `touch requirements.txt` en la terminal
- `pip freeze > requirements.txt` (para guardar un nuevo archivo)

Próximos proyectos

- En consola ejecutarlo como `pip install - r requirements.txt`

## Código

- Crear un archivo main.py para activar flask
- Crear la variable de ambiente flask para poder ejecutarlo desde la terminal
  `> set FLASK_APP=main.py`
  `> flask run`
