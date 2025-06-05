# Programación LS94.1FM

Este es un sistema de programación para la emisora **Lanceros Stereo 94.1 FM**, desarrollado en Python con una arquitectura **MVC** (Modelo-Vista-Controlador). Permite gestionar, visualizar y exportar la programación de cuñas radiales asignadas a bloques de 30 minutos entre las 5:30AM y las 8:30PM.

---

## 🎯 Funcionalidades principales

- ✅ Registro de cuñas por horario
- ✅ Visualización superpuesta de la programación próxima (HUD)
- ✅ Exportación de programación (`.txt` / `.csv`)
- ✅ Eliminación de cuñas por número
- ✅ Actualización automática del horario actual (cada 30s)
- ✅ Guardado automático y respaldo diario

---

## 🗂 Estructura del proyecto

```
.
├── controller.py          # Lógica del controlador (intermediario Vista ↔ Modelo)
├── model.py               # Capa de datos (horarios y almacenamiento)
├── view.py                # Interfaz gráfica con Tkinter
├── main.py                # Punto de entrada principal
├── data/                  # Carpeta de datos y respaldos
│   └── ads_data.json
├── dist/                  # Archivos compilados (por PyInstaller)
├── build/                 # Archivos de construcción
├── LS94_1.ico             # Ícono para ejecutable
└── ProgramaciónLS94.1FM.exe  # Ejecutable generado
```

---

## ▶ Cómo ejecutar

**Desde código fuente:**

```bash
python main.py
```

**Como ejecutable (Windows):**

Ejecuta el archivo `ProgramaciónLS94.1FM.exe` directamente.

---

## 🛠 Requisitos

- Python 3.10+
- Paquetes estándar (`tkinter`, `json`, `os`, `datetime`)
- Recomendado: crear entorno virtual

---

## 🖥 Generar el ejecutable

```bash
pyinstaller --onefile --noconsole --icon=LS94_1.ico --name "ProgramaciónLS94.1FM" main.py
```

---

## 📦 Autores y licencia

Desarrollado por **@juanitomanoplateada**  
Distribución cerrada para uso interno de **Lanceros Stereo 94.1 FM**.
