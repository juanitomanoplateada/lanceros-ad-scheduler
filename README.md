# Programador de Cuñas - Lanceros Stereo 94.1 FM

## Descripción general

El **Programador de Cuñas de Lanceros Stereo** es una aplicación de escritorio diseñada para gestionar la programación de cuñas radiales (anuncios) en los bloques de programación diarios de la emisora **Lanceros Stereo 94.1 FM**.

La aplicación combina una interfaz de escritorio desarrollada con **Python y Tkinter**, junto con un microservicio en **Flask** que permite integraciones externas en tiempo real, como con software de transmisión.

---

## Visión general del sistema

La aplicación opera entre las **5:30 a.m. y las 8:30 p.m.**, dividiendo la jornada en bloques de **30 minutos**. En cada bloque, los operadores pueden asignar cuñas numeradas del **0 al 99** mediante una interfaz visual de casillas.

---

## Arquitectura general del sistema

### 🗂️ Capa de datos
- `ads_data.json`: Guarda la programación en formato JSON.
- `data/backups/`: Contiene copias de seguridad diarias.
- `C:/OtsLabs/Logs/`: Lectura de logs para detectar canciones en reproducción (OtsAV).

### 🔄 Servicios en segundo plano
- **Auto-guardado**: Guarda automáticamente cada 60 segundos.
- **PeriodicBackupService**: Copia el archivo `.oml` cada 30 minutos.

### 🧠 Núcleo de la aplicación

| Componente           | Descripción                                |
|----------------------|--------------------------------------------|
| `main.py`            | Punto de entrada de la aplicación          |
| `model.py`           | Lógica de datos y exportación              |
| `view.py`            | Interfaz gráfica con Tkinter               |
| `controller.py`      | Coordinador de lógica y eventos            |
| `song_service.py`    | Servidor Flask para integración externa    |

---

## Componentes principales de la aplicación

### 🔧 Patrón MVC

- **Modelo**:
  - Maneja `ads_data.json`
  - Valida programación
  - Exporta a `.txt` y `.csv`

- **Vista**:
  - Interfaz gráfica con Tkinter
  - Cuadro de casillas para cuñas
  - HUD flotante con los siguientes bloques

- **Controlador**:
  - Captura eventos del usuario
  - Coordina vista y modelo

### 🌐 Microservicio Flask

- Ruta: `http://localhost:8080/current_song.txt`
- Lee los logs de OtsAV
- Proporciona metadatos de la canción actual

### 🛡️ Copias de seguridad

- Guardado automático cada 60 segundos
- Respaldo periódico del archivo `.oml`
- Copias diarias en `data/backups/`

---

## Funcionalidades clave

| Funcionalidad             | Implementación / Referencia                 |
|---------------------------|---------------------------------------------|
| Asignación visual de cuñas| Cuadro de casillas – `view.py`              |
| Persistencia de datos     | JSON + auto-guardado – `model.py`           |
| HUD en tiempo real        | Ventana flotante – `view.py`                |
| Exportación               | `.txt` y `.csv` – `model.py`                |
| Integración externa       | API HTTP con Flask – `song_service.py`      |
| Copias de seguridad       | Automáticas y periódicas – `main.py`, `model.py` |

---

## Modelo de concurrencia

La aplicación usa hilos para mantener la interacción fluida:

- **Hilo principal**: Ejecuta `main.py` y lanza los servicios
- **Hilo de GUI**: `root.mainloop()` (interfaz gráfica)
- **Hilo Flask**: Servidor de canciones actuales
- **Hilo de backups**: Copias del archivo `.oml` cada 30 minutos

---

## Ecosistema de integración

La aplicación se integra con el ecosistema de transmisión:

- **OtsAV DJ**: Lectura de logs desde `C:/OtsLabs/Logs/`
- **OBS Studio**: Consume datos actuales vía API para superposiciones
- **Paneles web**: Acceden a la canción actual desde el endpoint Flask
- **Archivos exportados**: En `.txt` y `.csv` para otros sistemas

### API principal:

```
GET http://localhost:8080/current_song.txt
```

---

## Archivos fuente

- `main.py`
- `model.py`
- `view.py`
- `controller.py`
- `song_service.py`
- `README.md`

---

© Lanceros Stereo 94.1 FM · Todos los derechos reservados.
