# Lanceros Stereo Cuñas Scheduler

Aplicación de escritorio para la emisora **Lanceros Stereo 94.1 FM** que permite programar y visualizar cuñas radiales en franjas horarias de 30 minutos. Incluye una visualización HUD flotante y un microservidor Flask que expone en tiempo real la canción actual en reproducción.

---

## 🎯 Características principales

- Asignación visual y sencilla de cuñas numeradas (0–99) a franjas horarias entre **5:30AM y 8:30PM**.
- Edición de franjas individuales con casillas de verificación (checkboxes).
- HUD flotante sobrepuesto con los próximos 3 bloques de programación.
- Auto-guardado cada 60 segundos.
- Exportación de la programación a archivo `.txt` o `.csv`.
- Backup automático diario.
- Microservicio Flask para emitir la canción actual desde los logs de OtsAV.

---

## 🚀 Cómo ejecutar

1. Instalar dependencias:
```bash
pip install flask
```

2. Ejecutar el programa principal:
```bash
python main.py
```

Esto abrirá la interfaz gráfica y un servidor Flask en segundo plano accesible en: [http://localhost:8080/current_song.txt](http://localhost:8080/current_song.txt)

---

## 📁 Estructura del proyecto

```
├── main.py                 # Punto de entrada de la app
├── model.py               # Lógica de persistencia y manejo de horarios
├── view.py                # Interfaz gráfica (Tkinter)
├── controller.py          # Lógica de interacción entre vista y modelo
├── song_service.py        # Servidor Flask para mostrar canción actual
├── data/
│   ├── ads_data.json      # Datos persistentes de cuñas
│   └── backups/           # Respaldos diarios automáticos
```

---

## 📡 Servicio Flask

El archivo `song_service.py` accede al log generado por OtsAV (`C:/OtsLabs/Logs/YYYY-MM-DD-playlog.txt`), parsea la última entrada y entrega el nombre del artista y canción actual.

Ideal para integraciones con OBS, paneles web, entre otros.

---

## ✅ Para compilar a .exe

```bash
pyinstaller --onefile --icon=icon.ico main.py
```

---

## 📌 Autor

Desarrollado por el equipo de **Lanceros Stereo 94.1 FM** con ❤️ y Python.